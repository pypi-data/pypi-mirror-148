# -*- coding: utf-8 -*-
"""async_upnp_client.aiohttp module."""

import asyncio
import logging
from asyncio.events import AbstractEventLoop, AbstractServer
from ipaddress import ip_address
from typing import Mapping, Optional, Tuple

import aiohttp
import aiohttp.web
import async_timeout

from async_upnp_client.client import UpnpRequester
from async_upnp_client.const import AddressTupleVXType, IPvXAddress
from async_upnp_client.event_handler import UpnpEventHandler, UpnpNotifyServer
from async_upnp_client.exceptions import (
    UpnpClientResponseError,
    UpnpCommunicationError,
    UpnpConnectionError,
    UpnpConnectionTimeoutError,
    UpnpServerOSError,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER_TRAFFIC_UPNP = logging.getLogger("async_upnp_client.traffic.upnp")


class AiohttpRequester(UpnpRequester):
    """Standard AioHttpUpnpRequester, to be used with UpnpFactory."""

    # pylint: disable=too-few-public-methods

    def __init__(
        self, timeout: int = 5, http_headers: Optional[Mapping[str, str]] = None
    ) -> None:
        """Initialize."""
        self._timeout = timeout
        self._http_headers = http_headers or {}

    async def async_http_request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]] = None,
        body: Optional[str] = None,
    ) -> Tuple[int, Mapping, str]:
        """Do a HTTP request."""
        req_headers = {**self._http_headers, **(headers or {})}

        _LOGGER_TRAFFIC_UPNP.debug(
            "Sending request:\n%s %s\n%s\n%s\n",
            method,
            url,
            "\n".join(
                [key + ": " + value for key, value in (req_headers or {}).items()]
            ),
            body or "",
        )

        try:
            async with async_timeout.timeout(self._timeout):
                async with aiohttp.ClientSession() as session:
                    async with session.request(
                        method, url, headers=req_headers, data=body
                    ) as response:
                        status = response.status
                        resp_headers: Mapping = response.headers or {}
                        resp_body = await response.read()

                        _LOGGER_TRAFFIC_UPNP.debug(
                            "Got response:\n%s\n%s\n\n%s",
                            status,
                            "\n".join(
                                [
                                    key + ": " + value
                                    for key, value in resp_headers.items()
                                ]
                            ),
                            resp_body,
                        )

                        resp_body_text = await response.text()
        except asyncio.TimeoutError as err:
            raise UpnpConnectionTimeoutError(str(err)) from err
        except aiohttp.ClientConnectionError as err:
            raise UpnpConnectionError(str(err)) from err
        except aiohttp.ClientResponseError as err:
            raise UpnpClientResponseError(
                request_info=err.request_info,
                history=err.history,
                status=err.status,
                message=err.message,
                headers=err.headers,
            ) from err
        except aiohttp.ClientError as err:
            raise UpnpCommunicationError(str(err)) from err
        except UnicodeDecodeError as err:
            raise UpnpCommunicationError(str(err)) from err

        return status, resp_headers, resp_body_text


class AiohttpSessionRequester(UpnpRequester):
    """
    Standard AiohttpSessionRequester, to be used with UpnpFactory.

    With pluggable session.
    """

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        session: aiohttp.ClientSession,
        with_sleep: bool = False,
        timeout: int = 5,
        http_headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        """Initialize."""
        self._session = session
        self._with_sleep = with_sleep
        self._timeout = timeout
        self._http_headers = http_headers or {}

    async def async_http_request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]] = None,
        body: Optional[str] = None,
    ) -> Tuple[int, Mapping[str, str], str]:
        """Do a HTTP request with a retry on ServerDisconnectedError.

        The HTTP/1.1 spec allows the server to disconnect at any time.
        We want to retry the request in this event.
        """
        for _ in range(2):
            try:
                return await self._async_http_request(method, url, headers, body)
            except aiohttp.ServerDisconnectedError as err:
                _LOGGER.debug("%r during request; retrying", err)
        try:
            return await self._async_http_request(method, url, headers, body)
        except aiohttp.ServerDisconnectedError as err:
            raise UpnpConnectionError(str(err)) from err

    async def _async_http_request(
        self,
        method: str,
        url: str,
        headers: Optional[Mapping[str, str]] = None,
        body: Optional[str] = None,
    ) -> Tuple[int, Mapping[str, str], str]:
        """Do a HTTP request."""
        # pylint: disable=too-many-arguments
        req_headers = {**self._http_headers, **(headers or {})}

        _LOGGER_TRAFFIC_UPNP.debug(
            "Sending request:\n%s %s\n%s\n%s\n",
            method,
            url,
            "\n".join(
                [key + ": " + value for key, value in (req_headers or {}).items()]
            ),
            body or "",
        )

        if self._with_sleep:
            await asyncio.sleep(0)

        try:
            async with async_timeout.timeout(self._timeout):
                async with self._session.request(
                    method, url, headers=req_headers, data=body
                ) as response:
                    status = response.status
                    resp_headers: Mapping = response.headers or {}
                    resp_body = await response.read()

                    _LOGGER_TRAFFIC_UPNP.debug(
                        "Got response:\n%s\n%s\n\n%s",
                        status,
                        "\n".join(
                            [key + ": " + value for key, value in resp_headers.items()]
                        ),
                        resp_body,
                    )

                    resp_body_text = await response.text()
        except asyncio.TimeoutError as err:
            raise UpnpConnectionTimeoutError(str(err)) from err
        except aiohttp.ServerDisconnectedError:
            raise
        except aiohttp.ClientConnectionError as err:
            raise UpnpConnectionError(str(err)) from err
        except aiohttp.ClientResponseError as err:
            raise UpnpClientResponseError(
                request_info=err.request_info,
                history=err.history,
                status=err.status,
                message=err.message,
                headers=err.headers,
            ) from err
        except aiohttp.ClientError as err:
            raise UpnpCommunicationError(str(err)) from err
        except UnicodeDecodeError as err:
            raise UpnpCommunicationError(str(err)) from err

        return status, resp_headers, resp_body_text


class AiohttpNotifyServer(UpnpNotifyServer):
    """
    Aio HTTP Server to handle incoming events.

    It is advisable to use one AiohttpNotifyServer per listening IP,
    UpnpDevices can share a AiohttpNotifyServer/UpnpEventHandler.
    """

    def __init__(
        self,
        requester: UpnpRequester,
        source: AddressTupleVXType,
        callback_url: Optional[str] = None,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        """Initialize."""
        self._source = source
        self._callback_url = callback_url
        self._loop = loop or asyncio.get_event_loop()

        self._aiohttp_server: Optional[aiohttp.web.Server] = None
        self._server: Optional[AbstractServer] = None

        self.event_handler = UpnpEventHandler(self, requester)

    async def async_start_server(self) -> None:
        """Start the HTTP server."""
        self._aiohttp_server = aiohttp.web.Server(self._handle_request)

        try:
            self._server = await self._loop.create_server(
                self._aiohttp_server, self._source[0], self._source[1]
            )
        except OSError as err:
            _LOGGER.error(
                "Failed to create HTTP server at %s:%d: %s",
                self._source[0],
                self._source[1],
                err,
            )
            raise UpnpServerOSError(
                errno=err.errno,
                strerror=err.strerror,
            ) from err

        # Get listening port.
        socks = self._server.sockets
        assert socks and len(socks) == 1
        sock = socks[0]
        self._source = sock.getsockname()
        _LOGGER.debug("New source for UpnpNotifyServer: %s", self._source)

    async def async_stop_server(self) -> None:
        """Stop the HTTP server."""
        await self.event_handler.async_unsubscribe_all()

        if self._aiohttp_server:
            await self._aiohttp_server.shutdown(10)
            self._aiohttp_server = None

        if self._server:
            self._server.close()
            self._server = None

    async def _handle_request(
        self, request: aiohttp.web.BaseRequest
    ) -> aiohttp.web.Response:
        """Handle incoming requests."""
        _LOGGER.debug("Received request: %s", request)

        headers = request.headers
        body = await request.text()
        _LOGGER_TRAFFIC_UPNP.debug(
            "Incoming request:\nNOTIFY\n%s\n\n%s",
            "\n".join([key + ": " + value for key, value in headers.items()]),
            body,
        )

        if request.method != "NOTIFY":
            _LOGGER.debug("Not notify")
            return aiohttp.web.Response(status=405)

        if not self.event_handler:
            _LOGGER.debug("Event handler not created yet")
            return aiohttp.web.Response(status=503, reason="Server not fully started")

        status = await self.event_handler.handle_notify(headers, body)
        _LOGGER.debug("NOTIFY response status: %s", status)
        _LOGGER_TRAFFIC_UPNP.debug("Sending response: %s", status)

        return aiohttp.web.Response(status=status)

    @property
    def listen_ip(self) -> IPvXAddress:
        """Get listenting IP Address."""
        return ip_address(self._source[0])

    @property
    def listen_host(self) -> str:
        """Get listening host."""
        return str(self.listen_ip)

    @property
    def listen_port(self) -> int:
        """Get the listening port."""
        return self._source[1]

    @property
    def callback_url(self) -> str:
        """Return callback URL on which we are callable."""
        listen_ip = self.listen_ip
        return self._callback_url or (
            self._callback_url or f"http://{self.listen_host}:{self.listen_port}/notify"
            if listen_ip.version == 4
            else f"http://[{self.listen_host}]:{self.listen_port}/notify"
        )
