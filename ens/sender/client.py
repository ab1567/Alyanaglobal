import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class ENSClient:
    """Simple client for sending ENS filings to a remote service.

    The client performs a login to obtain an authentication token and then
    posts signed XML documents to the ENS endpoint. Credentials can be
    supplied directly or via the ``ENS_USERNAME`` and ``ENS_PASSWORD``
    environment variables.
    """

    base_url: str
    username: Optional[str] = None
    password: Optional[str] = None
    login_path: str = "/login"
    submit_path: str = "/ens"

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.username = self.username or os.getenv("ENS_USERNAME")
        self.password = self.password or os.getenv("ENS_PASSWORD")
        if not (self.username and self.password):
            raise ValueError("ENS credentials not provided")
        self._token: Optional[str] = None

    def login(self) -> str:
        """Authenticate with the ENS service and store the access token."""
        resp = self.session.post(
            self.base_url.rstrip("/") + self.login_path,
            json={"username": self.username, "password": self.password},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        token = data.get("token")
        if not token:
            raise ValueError("No token returned from ENS login")
        self._token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    def submit(self, xml_payload: str) -> requests.Response:
        """Submit a signed ENS XML document to the ENS endpoint."""
        if self._token is None:
            self.login()
        resp = self.session.post(
            self.base_url.rstrip("/") + self.submit_path,
            data=xml_payload.encode("utf-8"),
            headers={"Content-Type": "application/xml"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp
