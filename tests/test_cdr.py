import base64
import os
from datetime import date

import pytest

from voipms_api import CDR

TRANSCRIPTIONS = {
    "status": "success",
    "transcriptions": [{
        "date": "2024-10-11 08:48:40",
        "duration": "00:07",
        "speakers": {"1": "3314315459", "2": "19283528012"},
        "locale": "en-US",
        "confidence": "94.18%",
        "recognized_phrases": [
            {"time": "2024-10-11 08:48:21", "duration": 2.84, "speaker": 2, "phrase": "That number has not yet been assigned."},
            {"time": "2024-10-11 08:48:24", "duration": 2.12, "speaker": 1, "phrase": "Please contact Technical Support."},
        ],
    }],
}


def sent_params(get):
    return get.call_args.kwargs["params"]


def test_get_cdr_sends_dates_timezone_and_includes_all_dispositions(mock_requests):
    get, _ = mock_requests
    CDR("u", "p").get_cdr("2026-11-01", "2026-11-09", timezone=-6)
    params = sent_params(get)
    assert params["method"] == "getCDR"
    assert (params["date_from"], params["date_to"], params["timezone"]) == ("2026-11-01", "2026-11-09", -6)
    assert (params["answered"], params["noanswer"], params["busy"], params["failed"]) == (1, 1, 1, 1)
    assert "calltype" not in params and "account" not in params


def test_get_cdr_filters(mock_requests):
    get, _ = mock_requests
    CDR("u", "p").get_cdr(
        "2026-11-01", "2026-11-09", timezone=0, answered=True, noanswer=False, busy=False, failed=False,
        call_type="all", call_billing="all", account="100000_VoIP",
    )
    params = sent_params(get)
    assert (params["answered"], params["noanswer"], params["busy"], params["failed"]) == (1, 0, 0, 0)
    assert (params["calltype"], params["callbilling"], params["account"]) == ("all", "all", "100000_VoIP")


@pytest.mark.parametrize("date_from, date_to", [("2026-11-09", "2026-11-01"), ("11/01/2026", "2026-11-09")])
def test_get_cdr_rejects_invalid_dates(mock_requests, date_from, date_to):
    get, _ = mock_requests
    with pytest.raises(ValueError):
        CDR("u", "p").get_cdr(date_from, date_to, timezone=0)
    get.assert_not_called()


def test_get_cdr_rejects_timezone_out_of_range(mock_requests):
    with pytest.raises(ValueError):
        CDR("u", "p").get_cdr("2026-11-01", "2026-11-09", timezone=14)


def test_get_call_recordings(mock_requests):
    get, _ = mock_requests
    CDR("u", "p").get_call_recordings("100000_VoIP", "2026-11-01", "2026-11-09", call_type="incoming", start=50, length=25)
    params = sent_params(get)
    assert params["method"] == "getCallRecordings"
    assert (params["account"], params["call_type"], params["start"], params["length"]) == ("100000_VoIP", "incoming", 50, 25)


def test_get_call_recordings_rejects_unknown_call_type(mock_requests):
    with pytest.raises(ValueError):
        CDR("u", "p").get_call_recordings("100000_VoIP", "2026-11-01", "2026-11-09", call_type="inbound")


def test_get_call_recording_saves_audio(mock_requests, tmp_path):
    get, _ = mock_requests
    audio = b"\xff\xe38\xc4fake-mp3"
    # The API escapes '/' as '\/' and may wrap the value in quotes.
    encoded = '"' + base64.b64encode(audio).decode().replace("/", "\\/") + '"'
    get.return_value.json.return_value = {"status": "success", "callrecording": "abc", "base64file": encoded}
    target = tmp_path / "call.mp3"

    data = CDR("u", "p").get_call_recording("100000_VoIP", "abc", file_path=str(target))

    assert target.read_bytes() == audio
    assert data["callrecording"] == "abc"
    assert sent_params(get)["callrecording"] == "abc"


def test_delete_call_recording(mock_requests):
    get, _ = mock_requests
    CDR("u", "p").delete_call_recording("100000_VoIP", "abc")
    assert sent_params(get)["method"] == "delCallRecording"
    assert sent_params(get)["callrecording"] == "abc"


def test_send_call_recording_email(mock_requests):
    get, _ = mock_requests
    CDR("u", "p").send_call_recording_email("100000_VoIP", "abc", "me@example.com")
    params = sent_params(get)
    assert params["method"] == "sendCallRecordingEmail"
    assert (params["account"], params["callrecording"], params["email"]) == ("100000_VoIP", "abc", "me@example.com")


def test_get_call_transcriptions_saves_text(mock_requests, tmp_path):
    get, _ = mock_requests
    get.return_value.json.return_value = TRANSCRIPTIONS
    target = tmp_path / "transcriptions.txt"

    data = CDR("u", "p").get_call_transcriptions("100001_VoIP", "2024-10-11", "2024-10-11", file_path=str(target))

    assert data == TRANSCRIPTIONS
    assert sent_params(get)["method"] == "getCallTranscriptions"
    text = target.read_text()
    assert "2024-10-11 08:48:40" in text
    assert "[2024-10-11 08:48:21] 19283528012: That number has not yet been assigned." in text
    assert "[2024-10-11 08:48:24] 3314315459: Please contact Technical Support." in text


def test_get_call_transcriptions_without_results_writes_nothing(mock_requests, tmp_path):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "no_transcriptions"}
    target = tmp_path / "transcriptions.txt"
    data = CDR("u", "p").get_call_transcriptions("100001_VoIP", "2024-10-11", "2024-10-11", file_path=str(target))
    assert data == {"status": "no_transcriptions"}
    assert not target.exists()


@pytest.mark.parametrize("name, method", [
    ("get_call_accounts", "getCallAccounts"),
    ("get_call_types", "getCallTypes"),
    ("get_call_billing", "getCallBilling"),
])
def test_value_lists(mock_requests, name, method):
    get, _ = mock_requests
    getattr(CDR("u", "p"), name)()
    assert sent_params(get)["method"] == method


def test_get_call_recording_not_found_with_file_path_raises(mock_requests, tmp_path):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "no_recording"}
    target = tmp_path / "call.mp3"
    with pytest.raises(ValueError):
        CDR("u", "p").get_call_recording("100000_VoIP", "abc", file_path=str(target))
    assert not target.exists()


live = pytest.mark.skipif(not os.environ.get("VOIPMS_LIVE_TESTS"), reason="set VOIPMS_LIVE_TESTS=1 to call the real API")


@live
@pytest.mark.parametrize("name", ["get_call_accounts", "get_call_types", "get_call_billing"])
def test_live_value_lists(name):
    assert getattr(CDR(), name)()["status"] == "success"


@live
def test_live_get_cdr():
    today = date.today().isoformat()
    assert CDR().get_cdr(today, today, timezone=0)["status"] in ("success", "no_cdr")
