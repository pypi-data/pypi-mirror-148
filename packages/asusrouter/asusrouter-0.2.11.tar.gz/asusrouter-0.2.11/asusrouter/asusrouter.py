"""AsusRouter module"""

from __future__ import annotations

import logging
import asyncio
from datetime import datetime

from asusrouter import AsusRouterError, Connection, helpers
from .const import(
    AR_PATH,
    DEFAULT_SLEEP_TIME,
    INTERFACE_TYPE,
    KEY_NVRAM_GET,
    MONITOR_MAIN,
    MSG_ERROR,
    MSG_INFO,
    MSG_SUCCESS,
    MSG_WARNING,
    NETWORK_DATA,
    NVRAM_LIST,
    PORT_TYPE,
    TRAFFIC_GROUPS,
    TRAFFIC_GROUPS_REPLACE,
)

_LOGGER = logging.getLogger(__name__)

class AsusRouter:
    """The interface class"""

    def __init__(
        self,
        host : str,
        username : str | None = None,
        password : str | None = None,
        port : int | None = None,
        use_ssl : bool = False,
        cert_check : bool = True,
        cert_path : str = "",
        cache_time : int = 5,
        enable_monitor : bool = True,
        enable_control : bool = False):
        """Init"""

        self._enable_monitor : bool = enable_monitor
        self._enable_control : bool = enable_control

        self._cache_time : int = cache_time


        self._device_cpu_cores : list | None = None
        self._device_ports : dict | None = None
        self._device_boottime : datetime | None = None


        self._monitor_main : dict | None = None
        self._monitor_main_time : datetime | None = None
        self._monitor_main_running : bool = False
        self._monitor_nvram : dict | None = None
        self._monitor_nvram_time : datetime | None = None
        self._monitor_nvram_running : bool = False
        self._monitor_misc : dict | None = None
        self._monitor_misc_time : datetime | None = None
        self._monitor_misc_running : bool = False
        self._monitor_devices : dict | None = None
        self._monitor_devices_time : datetime | None = None
        self._monitor_devices_running : bool = False


        """Connect"""
        self.connection = Connection(host = host, username = username, password = password, port = port, use_ssl = use_ssl, cert_check = cert_check, cert_path = cert_path)


    async def async_compile_hook(self, commands : dict[str, str] | None = None) -> str:
        """"Compile all the components of the hook message into one string"""

        data = ""
        if commands is not None:
            for item in commands:
                data += "{}({});".format(item, commands[item])

        return data


    async def async_compile_nvram(self, values : list[str] | str | None = None) -> str:
        """Compile all the values to ask from nvram"""

        if values is None:
            return ""

        if type(values) == str:
            return "{}({});".format(KEY_NVRAM_GET, values)

        request = ""
        for value in values:
            request += "{}({});".format(KEY_NVRAM_GET, value)
        return request


    async def async_hook(self, hook : str) -> dict:
        """Hook data from device"""

        result = {}

        if not self._enable_monitor:
            _LOGGER.error(MSG_ERROR["disabled_monitor"])
            return result

        if hook is None:
            return result

        try:
            result = await self.connection.async_run_command(command = "hook={}".format(hook))
            _LOGGER.debug("{}: {}".format(MSG_SUCCESS["hook"], hook))
        except Exception as ex:
            _LOGGER.error(ex)

        # Check for errors during hook
        if self.connection.error:
            _LOGGER.debug("Error flag found")
            await self.async_handle_error()

        return result


    async def async_command(self, commands : dict[str, str], action_mode : str = "apply") -> dict:
        """Command device to run a service or set parameter"""

        result = {}

        if not self._enable_control:
            _LOGGER.error(MSG_ERROR["disabled_control"])
            return result

        request : dict = {
            "action_mode": action_mode,
        }
        for command in commands:
            request[command] = commands[command]

        try:
            result = await self.connection.async_run_command(command = str(request), endpoint = AR_PATH["command"])
            _LOGGER.debug("{}: {}".format(MSG_SUCCESS["command"], request))
        except Exception as ex:
            _LOGGER.error(ex)

        return result


    async def async_load(self, page : str | None = None) -> dict:
        """Return the data from the page"""

        result = {}

        if not self._enable_monitor:
            _LOGGER.error(MSG_ERROR["disabled_monitor"])
            return result

        if page is None:
            return result

        try:
            result = await self.connection.async_run_command(command = "", endpoint = page)
            _LOGGER.debug(MSG_SUCCESS["load"])
        except Exception as ex:
            _LOGGER.error(ex)

        return result


    async def async_monitor_main(self) -> None:
        """Get all the main monitor values. Non-cacheable"""

        while self._monitor_main_running:
            await asyncio.sleep(DEFAULT_SLEEP_TIME)
            return

        self._monitor_main_running = True

        monitor_main = dict()

        hook = await self.async_compile_hook(MONITOR_MAIN)
        data = await self.async_hook(hook)

        now = datetime.utcnow()

        ### CPU ###
        ## Not yet known what exactly is type of data. But this is the correct way to calculate usage from it

        # Keep safe
        if "cpu_usage" in data:
            # Check which cores CPU has or find it out and save for later
            if self._device_cpu_cores is None:
                cpu_cores = []
                for i in range(1,8):
                    if "cpu{}_total".format(i) in data["cpu_usage"]:
                        cpu_cores.append(i)
                    else:
                        break
                self._device_cpu_cores = cpu_cores

            # Create CPU dict in monitor_main and populate its total for the whole CPU data
            monitor_main["CPU"] = dict()
            monitor_main["CPU"]["total"] = dict()
            monitor_main["CPU"]["total"]["total"] = 0
            monitor_main["CPU"]["total"]["used"] = 0
            # Store CPU data per core. "cpu{X}_total" stays "total", "cpu{X}_usage" becomes "used". This is done to free up "usage" for the actual usage in percents
            for core in self._device_cpu_cores:
                monitor_main["CPU"][core] = dict()
                if "cpu{}_total".format(core) in data["cpu_usage"]:
                    monitor_main["CPU"][core]["total"] = int(data["cpu_usage"]["cpu{}_total".format(core)])
                    monitor_main["CPU"]["total"]["total"] += monitor_main["CPU"][core]["total"]
                if "cpu{}_usage".format(core) in data["cpu_usage"]:
                    monitor_main["CPU"][core]["used"] = int(data["cpu_usage"]["cpu{}_usage".format(core)])
                    monitor_main["CPU"]["total"]["used"] += monitor_main["CPU"][core]["used"]
            # Calculate actual usage in percents and save it. Only if there was old data for CPU
            if (self._monitor_main is not None
                and "CPU" in self._monitor_main
            ):
                for item in monitor_main["CPU"]:
                    monitor_main["CPU"][item]["usage"] = round(100 * (monitor_main["CPU"][item]["used"] - self._monitor_main["CPU"][item]["used"]) / (monitor_main["CPU"][item]["total"] - self._monitor_main["CPU"][item]["total"]), 2)
        # Keep last data
        elif (self._monitor_main is not None
            and "CPU" in self._monitor_main
        ):
            monitor_main["CPU"] = self._monitor_main["CPU"]


        ### RAM ###
        ## Data is in KiB. To get MB as they are shown in the device Web-GUI, should be devided by 1024 (yes, those will be MiB)

        if "memory_usage" in data:
            # Populate RAM with known values
            monitor_main["RAM"] = dict()
            if "mem_total" in data["memory_usage"]:
                monitor_main["RAM"]["total"] = int(data["memory_usage"]["mem_total"])
            if "mem_free" in data["memory_usage"]:
                monitor_main["RAM"]["free"] = int(data["memory_usage"]["mem_free"])
            if "mem_used" in data["memory_usage"]:
                monitor_main["RAM"]["used"] = int(data["memory_usage"]["mem_used"])

            # Calculate usage in percents
            if "used" in monitor_main["RAM"] and "total" in monitor_main["RAM"]:
                monitor_main["RAM"]["usage"] = round(100 * monitor_main["RAM"]["used"] / monitor_main["RAM"]["total"], 2)
        # Keep last data
        elif (self._monitor_main is not None
            and "RAM" in self._monitor_main
        ):
            monitor_main["RAM"] = self._monitor_main["RAM"]


        ### NETWORK ###
        ## Data in Bytes for traffic and bits/s for speeds

        if "netdev" in data:
            # Calculate RX and TX from the HEX values. If there is no current value, but there was one before, get it from storage. Traffic resets only on device reboot or when above the limit. Device disconnect / reconnect does NOT reset it
            monitor_main["NETWORK"] = dict()
            for el in TRAFFIC_GROUPS:
                for nd in NETWORK_DATA:
                    if "{}_{}".format(el, nd) in data["netdev"]:
                        if not TRAFFIC_GROUPS[el] in monitor_main["NETWORK"]:
                            monitor_main["NETWORK"][TRAFFIC_GROUPS[el]] = dict()
                        monitor_main["NETWORK"][TRAFFIC_GROUPS[el]][nd] = int(data["netdev"]["{}_{}".format(el, nd)], base = 16)
                    elif (self._monitor_main is not None
                        and "NETWORK" in self._monitor_main
                        and el in self._monitor_main["NETWORK"]
                        and self._monitor_main["NETWORK"][TRAFFIC_GROUPS[el]][nd] is not None
                    ):
                        monitor_main["NETWORK"][TRAFFIC_GROUPS[el]][nd] = self._monitor_main["NETWORK"][TRAFFIC_GROUPS[el]][nd]

            if (self._monitor_main is not None
                and "NETWORK" in self._monitor_main
            ):
                # Calculate speeds
                for el in monitor_main["NETWORK"]:
                    for nd in NETWORK_DATA:
                        if el in self._monitor_main["NETWORK"]:
                            traffic_diff = monitor_main["NETWORK"][el][nd] - self._monitor_main["NETWORK"][el][nd]
                            # Handle overflow in the traffic stats, so there will not be a negative speed once per 0xFFFFFFFF + 1 bytes of data
                            if (traffic_diff < 0):
                                traffic_diff += 4294967296
                            monitor_main["NETWORK"][el]["{}_speed".format(nd)] = traffic_diff * 8 / (now - self._monitor_main_time).total_seconds()
                        else:
                            monitor_main["NETWORK"][el]["{}_speed".format(nd)] = 0

                # For devices not reporting INTERNET, only BRIDGE values
                for group in TRAFFIC_GROUPS_REPLACE:
                    if not group in monitor_main["NETWORK"]:
                        monitor_main["NETWORK"][group] = monitor_main["NETWORK"][TRAFFIC_GROUPS_REPLACE[group]]

        # Keep last data
        elif (self._monitor_main is not None
            and "NETWORK" in self._monitor_main
        ):
            monitor_main["NETWORK"] = self._monitor_main["NETWORK"]

        self._monitor_main = monitor_main

        self._monitor_main_time = now
        self._monitor_main_running = False

        return


    async def async_monitor_nvram(self, groups : list[str] | str | None = None) -> None:
        """Get the NVRAM values for the specified group list"""

        while self._monitor_nvram_running:
            await asyncio.sleep(DEFAULT_SLEEP_TIME)
            return

        self._monitor_nvram_running = True

        monitor_nvram = {}

        # If none groups were sent, will return all the known NVRAM values
        if groups is None:
            groups = [*NVRAM_LIST]

        # If only one group is sent
        if type(groups) is not list:
            groups = [groups.upper()]

        requests = []
        for group in groups:
            group = group.upper()
            if group in NVRAM_LIST:
                for value in NVRAM_LIST[group]:
                    requests.append(value)
            else:
                _LOGGER.warning("There is no {} in known NVRAM groups".format(group))

        message = await self.async_compile_nvram(requests)
        result = await self.async_hook(message)

        now = datetime.utcnow()

        for item in result:
            monitor_nvram[item] = result[item]

        if self._monitor_nvram is None:
            self._monitor_nvram = dict()

        for group in monitor_nvram:
            for element in monitor_nvram:
                self._monitor_nvram[element] = monitor_nvram[element]

        self._monitor_nvram_time = now
        self._monitor_nvram_running = False

        return


    async def async_monitor_misc(self) -> None:
        """Get all other useful values"""

        while self._monitor_misc_running:
            await asyncio.sleep(DEFAULT_SLEEP_TIME)
            return

        self._monitor_misc_running = True

        if self._monitor_misc is None:
            self._monitor_misc = dict()

        monitor_misc = {}

        ### PORTS

        # Receive ports number and status (disconnected, 100 Mb/s, 1 Gb/s)
        data = await self.async_load(page = AR_PATH["ports"])

        now = datetime.utcnow()

        if "portSpeed" in data:
            monitor_misc["PORTS"] = dict()
            for type in PORT_TYPE:
                monitor_misc["PORTS"][type] = dict()
            for value in data["portSpeed"]:
                for type in PORT_TYPE:
                    if type in value:
                        number = value.replace(type, "")
                        monitor_misc["PORTS"][type][number] = await helpers.async_transform_port_speed(data["portSpeed"][value])
                        break

        # Load devicemap
        data = await self.async_load(page = AR_PATH["devicemap"])
        monitor_misc["DEVICEMAP"] = data

        # Calculate boot time. Since precision is 1 second, could be that old and new are 1 sec different. In this case, we should not change the boot time, but keep the previous value to avoid regular changes
        if "SYS" in monitor_misc["DEVICEMAP"]:
            if "uptimeStr" in monitor_misc["DEVICEMAP"]["SYS"]:
                time = await helpers.async_parse_uptime(monitor_misc["DEVICEMAP"]["SYS"]["uptimeStr"])
                timestamp = int(time.timestamp())
                if not "BOOTTIME" in monitor_misc:
                    monitor_misc["BOOTTIME"] = dict()

                if "BOOTTIME" in self._monitor_misc:
                    _timestamp = self._monitor_misc["BOOTTIME"]["timestamp"]
                    _time = datetime.fromtimestamp(_timestamp)
                    if (time == _time
                        or abs(timestamp - _timestamp) < 2
                    ):
                        monitor_misc["BOOTTIME"] = self._monitor_misc["BOOTTIME"]
                    # This happens on reboots if data is checked before the device got correct time from NTP
                    elif timestamp - _timestamp < 0:
                        # Leave the same boot time, since we don't know the new correct time
                        monitor_misc["BOOTTIME"] = self._monitor_misc["BOOTTIME"]
                    else:
                        monitor_misc["BOOTTIME"]["timestamp"] = timestamp
                        monitor_misc["BOOTTIME"]["ISO"] = time.isoformat()
                else:
                    monitor_misc["BOOTTIME"]["timestamp"] = timestamp
                    monitor_misc["BOOTTIME"]["ISO"] = time.isoformat()

                if self._device_boottime != monitor_misc["BOOTTIME"]["ISO"]:
                    self._device_boottime = monitor_misc["BOOTTIME"]["ISO"]

        self._monitor_misc = monitor_misc

        self._monitor_misc_time = now
        self._monitor_misc_running = False

        return


    async def async_monitor_devices(self) -> None:
        """Monitor connected devices"""

        while self._monitor_devices_running:
            await asyncio.sleep(DEFAULT_SLEEP_TIME)
            return

        self._monitor_devices_running = True

        if self._monitor_devices is None:
            self._monitor_devices = dict()

        monitor_devices = {}

        data = await self.async_hook("get_clientlist()")

        now = datetime.utcnow()

        if "get_clientlist" in data:
            data = data["get_clientlist"]

            if "maclist" in data:
                for mac in data["maclist"]:
                    monitor_devices[mac] = dict()

                    # Name the device properly. If user has selected nickName manualy - it is the expected value. Else - name device set by itself or MAC address
                    if (data[mac]["nickName"] is not None
                        and data[mac]["nickName"] != ""):
                        monitor_devices[mac]["name"] = data[mac]["nickName"]
                    elif (data[mac]["name"] is not None
                        and data[mac]["name"] != ""):
                        monitor_devices[mac]["name"] = data[mac]["name"]
                    else:
                        monitor_devices[mac]["name"] = mac

                    # Let's still include MAC address
                    monitor_devices[mac]["MAC"] = mac

                    # IP address
                    monitor_devices[mac]["IP"] = data[mac]["ip"]
                    # IP type
                    monitor_devices[mac]["IPMethod"] = data[mac]["ipMethod"]

                    # Internet info map
                    monitor_devices[mac]["internet"] = dict()
                    # Connected
                    if data[mac]["internetState"] is not None:
                        monitor_devices[mac]["internet"]["online"] = data[mac]["internetState"]
                    # Mode
                    if data[mac]["internetMode"] is not None:
                        monitor_devices[mac]["internet"]["mode"] = data[mac]["internetMode"]

                    # Connection info map
                    monitor_devices[mac]["connection"] = dict()

                    # Type of the connection
                    if data[mac]["isWL"] is not None:
                        value = int(data[mac]["isWL"])
                        if value == 1:
                            monitor_devices[mac]["connection"]["type"] = "WLAN0"
                        elif value == 2:
                            monitor_devices[mac]["connection"]["type"] = "WLAN1"
                        else:
                            monitor_devices[mac]["connection"]["type"] = "LAN"
                    # Connected
                    if data[mac]["isOnline"] is not None:
                        monitor_devices[mac]["connection"]["online"] = data[mac]["isOnline"]
                        
                    # Only for wireless
                    if monitor_devices[mac]["connection"]["type"] != "LAN":
                        # RSSI
                        if data[mac]["rssi"] is not None:
                            monitor_devices[mac]["connection"]["RSSI"] = data[mac]["rssi"]
                        # Connection time
                        if data[mac]["wlConnectTime"] is not None:
                            value = await helpers.async_transform_connection_time(data[mac]["wlConnectTime"])
                            timestamp = value.timestamp()
                            iso = value.isoformat()

                            if (mac in self._monitor_devices
                                and "connection" in self._monitor_devices[mac]
                                and "timestamp" in self._monitor_devices[mac]["connection"]
                            ):
                                _timestamp = self._monitor_devices[mac]["connection"]["timestamp"]
                                if (timestamp == _timestamp
                                    or abs(timestamp - _timestamp) < 2
                                ):
                                    monitor_devices[mac]["connection"]["timestamp"] = self._monitor_devices[mac]["connection"]["timestamp"]
                                    monitor_devices[mac]["connection"]["ISO"] = self._monitor_devices[mac]["connection"]["ISO"]
                                else:
                                    monitor_devices[mac]["connection"]["timestamp"] = timestamp
                                    monitor_devices[mac]["connection"]["ISO"] = iso
                            else:
                                monitor_devices[mac]["connection"]["timestamp"] = timestamp
                                monitor_devices[mac]["connection"]["ISO"] = iso

                        # Connection speeds
                        monitor_devices[mac]["connection"]["speed"] = dict()
                        raw = data[mac]["curRx"].strip()
                        value = float(raw) if raw != "" else 0.0
                        monitor_devices[mac]["connection"]["speed"]["Rx"] = value
                        raw = data[mac]["curTx"].strip()
                        value = float(raw) if raw != "" else 0.0
                        monitor_devices[mac]["connection"]["speed"]["Tx"] = value
                    
                    # Other info
                    if (data[mac]["vendor"] is not None
                        and data[mac]["vendor"] != ""):
                        monitor_devices[mac]["vendor"] = data[mac]["vendor"]
        # Keep last data
        elif self._monitor_devices is not None:
            monitor_devices = self._monitor_devices

        self._monitor_devices = monitor_devices

        self._monitor_devices_time = now
        self._monitor_devices_running = False

        return


    async def async_handle_error(self) -> None:
        """Actions to be taken on connection errors"""

        # Most of errors come from device reboots. Handle it
        await self.async_handle_reboot()

        # Clear error
        await self.connection.async_reset_error()

        return


    async def async_handle_reboot(self) -> None:
        """Actions to be taken on reboot"""

        # Clear main monitor to prevent calculation errors in it
        if self._monitor_main:
            self._monitor_main = None
            self._monitor_main_time = None

        return


    async def async_find_interfaces(self, use_cache : bool = True) -> None:
        """Find available interfaces/type dictionary"""
        
        if self._monitor_nvram is None:
            await self.async_monitor_nvram()
        elif use_cache == False:
            await self.async_monitor_nvram()

        ports = {}

        data = self._monitor_nvram
        
        for if_type in INTERFACE_TYPE:
            if if_type in data:
                values = data[if_type].split(" ")
                for item in values:
                    ports[item] = INTERFACE_TYPE[if_type]

        self._device_ports = ports


    async def async_initialize(self):
        """Get all the data needed at the startup"""

        await self.async_monitor_main()
        await self.async_monitor_nvram()
        await self.async_find_interfaces()
        await self.async_monitor_misc()
        await self.async_monitor_devices()


#### RETURN DATA

    async def async_get_devices(self, use_cache : bool = True) -> dict:
        """Return device list"""
        
        now = datetime.utcnow()
        if (self._monitor_devices is None
            or self._monitor_devices_time is None
            or use_cache == False
            or (use_cache == True and self._monitor_devices_time and self._cache_time < (now - self._monitor_devices_time).total_seconds())
        ):
            await self.async_monitor_devices()

        return self._monitor_devices


    async def async_get_cpu(self, use_cache : bool = True) -> dict:
        """Return CPU usage"""
        
        now = datetime.utcnow()
        if (self._monitor_main is None
            or self._monitor_main_time is None
            or use_cache == False
            or (use_cache == True and self._monitor_main_time and self._cache_time < (now - self._monitor_main_time).total_seconds())
            or self._device_cpu_cores is None
        ):
            await self.async_monitor_main()

        result = {}

        # Check if CPU was monitored
        if (self._monitor_main is None
            or not "CPU" in self._monitor_main
        ):
            return result

        for core in self._device_cpu_cores:
            if "usage" in self._monitor_main["CPU"][core]:
                result["core_{}".format(core)] = self._monitor_main["CPU"][core]["usage"]
        if "usage" in self._monitor_main["CPU"]["total"]:
            result["total"] = self._monitor_main["CPU"]["total"]["usage"]

        return result


    async def async_get_cpu_labels(self) -> list:
        """Return list of CPU cores"""

        if self._device_cpu_cores is None:
            await self.async_monitor_main()

        result = list()
        result.append("total")
        for el in self._device_cpu_cores:
            result.append("core_{}".format(el))

        return result


    async def async_get_ram(self, use_cache : bool = True) -> dict:
        """Return RAM and its usage"""
        
        now = datetime.utcnow()
        if (self._monitor_main is None
            or use_cache == False
            or (use_cache == True
            and self._monitor_main_time
            and self._cache_time < (now - self._monitor_main_time).total_seconds())
        ):
            await self.async_monitor_main()

        result = {}

        # Check if RAM was monitored
        if (self._monitor_main is None
            or not "RAM" in self._monitor_main
        ):
            return result

        for value in self._monitor_main["RAM"]:
            result[value] = self._monitor_main["RAM"][value]
        return result


    async def async_get_ram_labels(self) -> list:
        """Return list of CPU cores"""

        if self._device_cpu_cores is None:
            await self.async_monitor_main()

        result = list()
        for value in self._monitor_main["RAM"]:
            result.append(value)

        return result


    async def async_get_network(self, use_cache : bool = True) -> dict:
        """Return traffic and speed for all interfaces"""
        
        now = datetime.utcnow()
        if (self._monitor_main is None
            or use_cache == False
            or (use_cache == True
            and self._monitor_main_time
            and self._cache_time < (now - self._monitor_main_time).total_seconds())
        ):
            await self.async_monitor_main()

        result = {}

        # Check if network was monitored
        if (self._monitor_main is None
            or not "NETWORK" in self._monitor_main
        ):
            return result

        for interface in self._monitor_main["NETWORK"]:
            for value in self._monitor_main["NETWORK"][interface]:
                result["{}_{}".format(interface, value)] = self._monitor_main["NETWORK"][interface][value]

        return result


    async def async_get_network_labels(self) -> list:
        """Return list of network interfaces"""

        if self._monitor_main is None:
            await self.async_monitor_main()
        if self._monitor_nvram is None:
            await self.async_monitor_nvram()

        result = list()

        for interface in self._monitor_main["NETWORK"]:
            result.append(interface)

        if (not "USB" in result
            and "dualwan" in self._monitor_nvram["rc_support"]
        ):
            result.append("USB")

        return result


    async def async_get_ports(self, use_cache : bool = True) -> dict:
        """Return WAN/LAN ports status"""
        
        now = datetime.utcnow()
        if (self._monitor_misc is None
            or use_cache == False
            or (use_cache == True
            and self._monitor_misc_time
            and self._cache_time < (now - self._monitor_misc_time).total_seconds())
        ):
            await self.async_monitor_misc()

        return self._monitor_misc["PORTS"]


    @property
    def connected(self) -> bool:
        return self.connection.connected

    @property
    def boottime(self) -> datetime:
        return self._device_boottime

