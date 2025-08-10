import types
from unittest.mock import MagicMock

import ens.sender
from ens.sender import ENSClient


def test_login_and_submit(monkeypatch):
    client = ENSClient("https://example.com", username="user", password="pass")

    login_resp = MagicMock()
    login_resp.json.return_value = {"token": "abc123"}
    login_resp.raise_for_status.return_value = None

    submit_resp = MagicMock()
    submit_resp.text = "ok"
    submit_resp.raise_for_status.return_value = None

    def fake_post(url, *args, **kwargs):
        if url.endswith("/login"):
            return login_resp
        return submit_resp

    monkeypatch.setattr(client.session, "post", fake_post)
    resp = client.submit("<xml/>")
    assert resp.text == "ok"
    assert client._token == "abc123"
