"""Backwards compatibility with the API published in 1.1.5b11."""

import pytest
import requests

from voipms_api import LNP, General, VoipMsClient


def test_make_request_is_a_deprecated_alias_of_get(mock_requests):
    get, _ = mock_requests
    client = VoipMsClient("u", "p")
    with pytest.deprecated_call():
        result = client.make_request("getIP", {"x": 1})
    assert result == {"status": "success"}
    assert get.call_args.kwargs["params"]["method"] == "getIP"


def test_vms_client_attribute_points_to_the_client(mock_requests):
    lnp = LNP("u", "p")
    with pytest.deprecated_call():
        inner = lnp.vms_client
    assert inner.voipms_url == "https://voip.ms/api/v1/rest.php"
    assert inner.username == "u"
    assert inner.password == "p"
    with pytest.deprecated_call():
        assert inner.make_request("getPortability", {"did": 1}) == {"status": "success"}


@pytest.mark.parametrize("call", [
    lambda g: g.get_conference(),
    lambda g: g.get_conference_members(),
    lambda g: g.get_conference_recordings(1),
    lambda g: g.get_conference_recording_file(1, 2),
    lambda g: g.get_transactions("2026-01-01", "2026-01-02"),
])
def test_general_returns_none_on_error(mock_requests, call):
    get, _ = mock_requests
    get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("500")
    assert call(General("u", "p")) is None
