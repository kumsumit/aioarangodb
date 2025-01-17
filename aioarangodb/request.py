__all__ = ["Request"]

from typing import Any, MutableMapping, Optional

from .typings import Fields, Headers, Params


def normalize_headers(headers: Optional[Headers]) -> Headers:
    normalized_headers: Headers = {
        "charset": "utf-8",
        "content-type": "application/json",
    }
    if headers is not None:
        for key, value in headers.items():
            normalized_headers[key.lower()] = value

    return normalized_headers


def normalize_params(params: Optional[Params]) -> MutableMapping[str, str]:
    normalized_params: MutableMapping[str, str] = {}

    if params is not None:
        for key, value in params.items():
            if isinstance(value, bool):
                value = int(value)

            normalized_params[key] = str(value)

    return normalized_params


class Request:
    """HTTP request.

    :param method: HTTP method in lowercase (e.g. "post").
    :type method: str
    :param endpoint: API endpoint.
    :type endpoint: str
    :param headers: Request headers.
    :type headers: dict | None
    :param params: URL parameters.
    :type params: dict | None
    :param data: Request payload.
    :type data: str | bool | int | float | list | dict | None | MultipartEncoder
    :param read: Names of collections read during transaction.
    :type read: str | [str] | None
    :param write: Name(s) of collections written to during transaction with
        shared access.
    :type write: str | [str] | None
    :param exclusive: Name(s) of collections written to during transaction
        with exclusive access.
    :type exclusive: str | [str] | None
    :param deserialize: Whether the response body can be deserialized.
    :type deserialize: bool

    :ivar method: HTTP method in lowercase (e.g. "post").
    :vartype method: str
    :ivar endpoint: API endpoint.
    :vartype endpoint: str
    :ivar headers: Request headers.
    :vartype headers: dict | None
    :ivar params: URL (query) parameters.
    :vartype params: dict | None
    :ivar data: Request payload.
    :vartype data: str | bool | int | float | list | dict | None
    :ivar read: Names of collections read during transaction.
    :vartype read: str | [str] | None
    :ivar write: Name(s) of collections written to during transaction with
        shared access.
    :vartype write: str | [str] | None
    :ivar exclusive: Name(s) of collections written to during transaction
        with exclusive access.
    :vartype exclusive: str | [str] | None
    :ivar deserialize: Whether the response body can be deserialized.
    :vartype deserialize: bool
    """

    __slots__ = (
        "method",
        "endpoint",
        "headers",
        "params",
        "data",
        "read",
        "write",
        "exclusive",
        "deserialize",
    )

    def __init__(
        self,
        method: str,
        endpoint: str,
        headers: Optional[Headers] = None,
        params: Optional[Params] = None,
        data: Any = None,
        read: Optional[Fields] = None,
        write: Optional[Fields] = None,
        exclusive: Optional[Fields] = None,
        deserialize: bool = True,
    ) -> None:
        self.method = method
        self.endpoint = endpoint
        self.headers: Headers = normalize_headers(headers)
        self.params: MutableMapping[str, str] = normalize_params(params)
        self.data = data
        self.read = read
        self.write = write
        self.exclusive = exclusive
        self.deserialize = deserialize
