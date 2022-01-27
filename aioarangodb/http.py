__all__ = ['HTTPClient', 'DefaultHTTPClient']

from abc import ABCMeta, abstractmethod
from typing import MutableMapping, Optional, Tuple, Union

import aiohttp
from aiohttp import MultipartWriter, ClientSession
from aiohttp_retry import RetryClient, ExponentialRetry
from .response import Response
from .typings import Headers


class HTTPClient(object):  # pragma: no cover
    """Abstract base class for HTTP clients."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_session(self, host):
        """Return a new requests session given the host URL.

        This method must be overridden by the user.

        :param host: ArangoDB host URL.
        :type host: str | unicode
        :returns: Requests session object.
        :rtype: requests.Session
        """
        raise NotImplementedError

    @abstractmethod
    async def send_request(
            self,
            session: ClientSession,
            method: str,
            url: str,
            headers: Optional[Headers] = None,
            params: Optional[MutableMapping[str, str]] = None,
            data: Union[str, MultipartWriter, None] = None,
            auth: Optional[Tuple[str, str]] = None,
    ) -> Response:
        """Send an HTTP request.

        This method must be overridden by the user.

        :param session: Requests session object.
        :type session: requests.Session
        :param method: HTTP method in lowercase (e.g. "post").
        :type method: str | unicode
        :param url: Request URL.
        :type url: str | unicode
        :param headers: Request headers.
        :type headers: dict
        :param params: URL (query) parameters.
        :type params: dict
        :param data: Request payload.
        :type data: str | unicode | bool | int | list | dict
        :param auth: Username and password.
        :type auth: tuple
        :returns: HTTP response.
        :rtype: arango.response.Response
        """
        raise NotImplementedError


class DefaultHTTPClient(HTTPClient):
    """Default HTTP client implementation."""

    REQUEST_TIMEOUT = 60
    RETRY_ATTEMPTS = 3
    BACKOFF_FACTOR = 1

    def create_session(self, host: str):
        """Create and return a new session/connection.

        :param host: ArangoDB host URL.
        :type host: str | unicode
        :returns: requests session object
        :rtype: requests.Session
        """
        retry_options = ExponentialRetry(attempts=3, statuses={429, 500, 502, 503, 504})
        return RetryClient(raise_for_status=False, retry_options=retry_options)

    async def send_request(
            self,
            session: ClientSession,
            method: str,
            url: str,
            headers: Optional[Headers] = None,
            params: Optional[MutableMapping[str, str]] = None,
            data: Union[str, MultipartWriter, None] = None,
            auth: Optional[Tuple[str, str]] = None,
    ) -> Response:
        """Send an HTTP request.

        :param session: Requests session object.
        :type session: requests.Session
        :param method: HTTP method in lowercase (e.g. "post").
        :type method: str | unicode
        :param url: Request URL.
        :type url: str | unicode
        :param headers: Request headers.
        :type headers: dict
        :param params: URL (query) parameters.
        :type params: dict
        :param data: Request payload.
        :type data: str | unicode | bool | int | list | dict
        :param auth: Username and password.
        :type auth: tuple
        :returns: HTTP response.
        :rtype: arango.response.Response
        """
        request = getattr(session, method)
        if auth is not None:
            auth = aiohttp.BasicAuth(auth[0], auth[1])
        response = await request(
            url=url,
            params=params,
            data=data,
            headers=headers,
            auth=auth
        )
        return Response(
            method=method,
            url=url,
            headers=response.headers,
            status_code=response.status,
            status_text=response.reason,
            raw_body=await response.text(),
        )
