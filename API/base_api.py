from typing import Any
from urllib.parse import urlparse

import requests
from requests.auth import HTTPBasicAuth

from Utils import config


class BaseAPI:
    """Small HTTP client shared by the endpoint-specific API classes."""

    def __init__(
        self,
        base_url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: float | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = (base_url if base_url is not None else config.BASE_URL).rstrip(
            "/"
        )
        if not self.base_url:
            raise ValueError("Base URL is not configured. Set BRAINYGO_BASE_URL.")
        parsed_url = urlparse(self.base_url)
        url_scheme = parsed_url.scheme
        if url_scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("Base URL must be a complete http or https URL.")

        self.timeout = timeout if timeout is not None else config.REQUEST_TIMEOUT
        if self.timeout <= 0:
            raise ValueError("Request timeout must be greater than zero.")
        self.session = session if session is not None else requests.Session()

        resolved_username = username if username is not None else config.USERNAME
        resolved_password = password if password is not None else config.PASSWORD
        if bool(resolved_username) != bool(resolved_password):
            raise ValueError("Username and password must be configured together.")
        if resolved_username and resolved_password:
            if url_scheme != "https":
                raise ValueError("Basic Auth credentials require an HTTPS base URL.")
            self.session.auth = HTTPBasicAuth(resolved_username, resolved_password)

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        if not endpoint.startswith("/"):
            raise ValueError("API endpoint must start with '/'.")

        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{endpoint}", **kwargs)

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> requests.Response:
        return self.request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> requests.Response:
        return self.request("POST", endpoint, json=data)

    def put(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> requests.Response:
        return self.request("PUT", endpoint, json=data)

    def patch(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> requests.Response:
        return self.request("PATCH", endpoint, json=data)

    def delete(
        self, endpoint: str, data: dict[str, Any] | None = None
    ) -> requests.Response:
        return self.request("DELETE", endpoint, json=data)
