import os
import subprocess
import sys
import unittest

import pytest

from voipms_api import VoipMsClient


def test_package_imports_in_clean_interpreter():
    """All modules must be importable as a package, without extra PYTHONPATH tweaks."""
    result = subprocess.run(
        [sys.executable, "-c", "import voipms_api; print(voipms_api.__all__)"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


def test_credentials_from_env(monkeypatch):
    monkeypatch.setenv("VOIPMS_API_USER", "env@example.com")
    monkeypatch.setenv("VOIPMS_API_PASSWORD", "env-pass")
    client = VoipMsClient()
    assert client.username == "env@example.com"
    assert client.password == "env-pass"


def test_credentials_from_args_override_env(monkeypatch):
    monkeypatch.setenv("VOIPMS_API_USER", "env@example.com")
    monkeypatch.setenv("VOIPMS_API_PASSWORD", "env-pass")
    client = VoipMsClient("arg@example.com", "arg-pass")
    assert client.username == "arg@example.com"
    assert client.password == "arg-pass"


def test_only_one_credential_raises():
    with pytest.raises(ValueError):
        VoipMsClient(username="arg@example.com")


def test_get_sends_auth_and_timeout(mock_requests):
    get, _ = mock_requests
    VoipMsClient("u", "p").get("getBalance")
    params = get.call_args.kwargs["params"]
    assert params["api_username"] == "u"
    assert params["method"] == "getBalance"
    assert get.call_args.kwargs["timeout"] is not None


def test_post_sends_params_as_multipart(mock_requests):
    """The API only accepts POST as multipart/form-data; any other encoding returns HTTP 500."""
    _, post = mock_requests
    VoipMsClient("u", "p").post("sendFaxMessage", {"file": "QUJD", "test": 1, "station_id": None})
    kwargs = post.call_args.kwargs
    assert kwargs["files"]["file"] == (None, "QUJD")
    assert kwargs["files"]["test"] == (None, "1")
    assert kwargs["files"]["api_password"] == (None, "p")
    assert "station_id" not in kwargs["files"]
    assert "params" not in kwargs and "data" not in kwargs
    assert kwargs["timeout"] is not None


def test_test_connection_respects_verify(mock_requests):
    get, _ = mock_requests
    VoipMsClient("u", "p", verify=False).test_connection()
    assert get.call_args.kwargs["verify"] is False
    assert get.call_args.kwargs["params"]["method"] == "getIP"


class TestLiveConnection(unittest.TestCase):

    @unittest.skipUnless(os.environ.get("VOIPMS_LIVE_TESTS"), "set VOIPMS_LIVE_TESTS=1 to call the real API")
    def test_connection(self):
        """
        Tests if the credentials and IP address are correct.
        """
        client = VoipMsClient()
        result = client.test_connection()
        self.assertEqual(result["status"], "success")

    @unittest.skipUnless(os.environ.get("VOIPMS_LIVE_TESTS"), "set VOIPMS_LIVE_TESTS=1 to call the real API")
    def test_post_connection(self):
        """
        Tests that the API accepts parameters sent in the POST body.
        """
        client = VoipMsClient()
        result = client.post("getIP")
        self.assertEqual(result["status"], "success")
