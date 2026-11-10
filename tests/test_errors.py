import pytest
import requests

from voipms_api import DIDs, SMS, Accounts, VoipMsClient
from voipms_api import VoipMsApiError, VoipMsConnectionError, VoipMsError


def test_success_returns_response(mock_requests):
    assert VoipMsClient("u", "p").get("getIP") == {"status": "success"}


def test_error_status_raises_api_error(mock_requests):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "invalid_did"}
    with pytest.raises(VoipMsApiError) as exc:
        DIDs("u", "p").cancel_did(5551234567)
    assert exc.value.status == "invalid_did"
    assert exc.value.method == "cancelDID"
    assert exc.value.response == {"status": "invalid_did"}
    assert isinstance(exc.value, VoipMsError)


def test_no_results_on_a_query_is_not_an_error(mock_requests):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "no_sms"}
    assert SMS("u", "p").get_sms() == {"status": "no_sms"}


def test_no_status_on_a_change_is_an_error(mock_requests):
    _, post = mock_requests
    post.return_value.json.return_value = {"status": "no_did"}
    with pytest.raises(VoipMsApiError):
        VoipMsClient("u", "p").post("setDIDRouting", {"did": 1})


def test_http_error_raises_connection_error_without_password(mock_requests):
    get, _ = mock_requests
    get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error for url: https://voip.ms/api/v1/rest.php?api_username=u&api_password=s3cr%26t&method=getIP"
    )
    with pytest.raises(VoipMsConnectionError) as exc:
        VoipMsClient("u", "s3cr&t").get("getIP")
    assert "s3cr" not in str(exc.value)
    assert exc.value.__cause__ is None and exc.value.__suppress_context__


def test_network_error_raises_connection_error(mock_requests):
    get, _ = mock_requests
    get.side_effect = requests.exceptions.ConnectTimeout("timed out")
    with pytest.raises(VoipMsConnectionError):
        VoipMsClient("u", "p").get("getIP")


def test_non_json_response_raises_connection_error(mock_requests):
    get, _ = mock_requests
    get.return_value.json.side_effect = requests.exceptions.JSONDecodeError("bad", "<html>", 0)
    with pytest.raises(VoipMsConnectionError):
        VoipMsClient("u", "p").get("getIP")


def test_params_dict_is_not_modified(mock_requests):
    params = {"did": 1}
    VoipMsClient("u", "p").get("getDIDsInfo", params)
    assert params == {"did": 1}


def test_validation_errors_raise_value_error(mock_requests):
    get, _ = mock_requests
    with pytest.raises(ValueError):
        Accounts("u", "p").create_subaccount("user", auth_type=1)
    get.assert_not_called()
