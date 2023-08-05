"""Connection module"""

import logging
import aiohttp
import base64
import json
import urllib.parse
import ssl
import asyncio
from pathlib import Path

from asusrouter import helpers, AsusRouterError, AsusRouterConnectionError, AsusRouterConnectionTimeoutError, AsusRouterServerDisconnectedError, AsusRouterLoginError, AsusRouterLoginBlockError, AsusRouterResponseError, AsusRouterValueError, AsusRouterSSLError
from .const import(
    AR_API,
    AR_ERROR,
    AR_USER_AGENT,
    AR_PATH,
    DEFAULT_PORT,
    DEFAULT_SLEEP_RECONNECT,
    MSG_ERROR,
    MSG_INFO,
    MSG_SUCCESS,
    MSG_WARNING,
)

_LOGGER = logging.getLogger(__name__)


class Connection:
    """Create connection"""

    def __init__(
        self,
        host : str,
        username : str,
        password : str,
        port : int | None = None,
        use_ssl: bool = False,
        cert_check : bool = True,
        cert_path : str = ""
    ):
        """Properties for connection"""

        self._host : str | None = host
        self._port : int | None = port
        self._username : str | None = username
        self._password : str | None = password
        self._token : str | None = None
        self._headers : dict | None = None
        self._session : str | None = None

        self._device : dict | None = dict()
        self._error : bool = False

        self._http = "https" if use_ssl else "http"

        if self._port is None or self._port == 0:
            self._port = DEFAULT_PORT[self._http]

        if cert_check:
            if cert_path != "":
                path = Path(cert_path)
                if path.is_file():
                    self._ssl = ssl.create_default_context(cafile = cert_path)
                    _LOGGER.debug(MSG_SUCCESS["cert_found"])
                else:
                    _LOGGER.error(MSG_ERROR["cert_missing"])
                    self._ssl = True
            else:
                _LOGGER.debug(MSG_INFO["no_cert"])
                self._ssl = True
        else:
            _LOGGER.debug(MSG_INFO["no_cert_check"])
            self._ssl = False

        self._connected: bool = None


    async def async_run_command(self, command : str, endpoint : str = AR_PATH["get"], retry : bool = False) -> dict:
        """Run command. Use the existing connection token, otherwise create new one"""

        if self._token is None and not retry:
            await self.async_connect()
            return await self.async_run_command(command, endpoint, retry = True)
        else:
            if self._token is not None:
                try:
                    result = await self.async_request(command, endpoint, self._headers)
                    return result
                except Exception as ex:
                    if not retry:
                        await self.async_connect()
                        return await self.async_run_command(command, endpoint, retry = True)
                    else:
                        _LOGGER.error(MSG_ERROR["command"])
                        return {}
            else:
                _LOGGER.error(MSG_ERROR["command"])
                return {}


    async def async_request(self, payload : str, endpoint : str, headers : dict, retry : bool = False) -> dict:
        """Send a request"""

        if retry:
            await asyncio.sleep(DEFAULT_SLEEP_RECONNECT)

        json_body = {}

        try:
            async with self._session.post(url="{}://{}:{}/{}".format(self._http, self._host, self._port, endpoint), data = urllib.parse.quote(payload), headers = headers, ssl = self._ssl) as r:
                string_body = await r.text()
                json_body = await r.json()

                # Check for errors
                if "error_status" in json_body:
                    error_code = int(json_body['error_status'])

                    # Not authorised
                    if error_code == AR_ERROR["authorisation"]:
                        _LOGGER.error(MSG_ERROR["authorisation"])
                    # Wrong crerdentials
                    elif error_code == AR_ERROR["credentials"]:
                        raise AsusRouterLoginError(MSG_ERROR["credentials"])
                    # Too many attempts
                    elif error_code == AR_ERROR["try_again"]:
                        raise AsusRouterLoginBlockError(MSG_ERROR["try_again"])
                    # Loged out
                    elif error_code == AR_ERROR["logout"]:
                        _LOGGER.info(MSG_SUCCESS["logout"])
                        return {"success": True}
                    # Unknown error code
                    else:
                        _LOGGER.error("{}: {}".format(MSG_ERROR["unknown"], error_code))

            # If loged in, save the device API data
            if endpoint == AR_PATH["login"]:
                r_headers = r.headers
                for item in AR_API:
                    if item in r_headers:
                        self._device[item] = r_headers[item]

            return json_body

        # Handle non-JSON replies
        except json.JSONDecodeError:
            if ".xml" in endpoint:
                _LOGGER.debug(MSG_INFO["xml"])
                json_body = await helpers.async_convert_xml(text = string_body)
            else:
                _LOGGER.debug(MSG_INFO["json_fix"])
                json_body = await helpers.async_convert_to_json(text = string_body)
            return json_body

        except (aiohttp.ClientConnectorSSLError, aiohttp.ClientConnectorCertificateError) as ex:
            raise AsusRouterSSLError(str(ex)) from ex
        except (aiohttp.ServerTimeoutError, asyncio.TimeoutError) as ex:
            raise AsusRouterConnectionTimeoutError(str(ex)) from ex
        except aiohttp.ServerDisconnectedError as ex:
            raise AsusRouterServerDisconnectedError(str(ex)) from ex

        # Connection refused -> will repeat
        except aiohttp.ClientConnectorError as ex:
            if endpoint == AR_PATH["login"]:
                raise AsusRouterLoginError(str(ex)) from ex
            if not retry:
                _LOGGER.warning("{}. Endpoint: {}. Payload: {}.\nException summary:{}".format(MSG_WARNING["refused"], endpoint, payload, str(ex)))

        # If it got here, something is wrong. Reconnect and retry
        if not retry:
            self._error = True
            _LOGGER.info(MSG_INFO["reconnect"])
            await self.async_cleanup()
            await self.async_connect(retry = True)
        return await self.async_request(payload = payload, endpoint = endpoint, headers = headers, retry = True)


    async def async_connect(self, retry : bool = False) -> bool:
        """Start new connection to and get new auth token"""

        _success = False

        self._session = aiohttp.ClientSession()

        auth = "{}:{}".format(self._username, self._password).encode('ascii')
        logintoken = base64.b64encode(auth).decode('ascii')
        payload = "login_authorization={}".format(logintoken)
        headers = {
            'user-agent': AR_USER_AGENT
        }

        response = await self.async_request(payload = payload, endpoint = AR_PATH["login"], headers = headers, retry = retry)
        if "asus_token" in response:
            self._token = response['asus_token']
            self._headers = {
                'user-agent': AR_USER_AGENT,
                'cookie': 'asus_token={}'.format(self._token)
            }
            _LOGGER.info("{} on port {}: {}".format(MSG_SUCCESS["login"], self._port, self._device))

            self._connected = True
            _success = True
        else:
            _LOGGER.error(MSG_ERROR["token"])

        return _success


    async def async_disconnect(self) -> bool:
        """Close the connection"""

        # Not connected
        if not self._connected:
            _LOGGER.warning(MSG_WARNING["not_connected"])
        # Connected
        else:
            result = await self.async_request("", AR_PATH["logout"], self._headers)
            if not "success" in result:
                return False

        # Clean up
        await self.async_cleanup()

        return True


    async def async_cleanup(self) -> None:
        """Cleanup after logout"""

        self._token = None
        self._headers = None
        if self._session is not None:
            await self._session.close()
        self._session = None


    async def async_reset_error(self) -> None:
        """Reset error flag"""

        self._error = False
        return


    @property
    def connected(self) -> bool:
        """Connection status"""

        return self._connected


    @property
    def device(self) -> dict:
        """Device model and API support levels"""

        return self._device


    @property
    def error(self) -> bool:
        """Report errors"""

        return self._error

