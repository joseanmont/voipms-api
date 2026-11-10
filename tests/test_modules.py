import base64

import pytest

from voipms_api import LNP, Accounts, Fax, General, RingGroups, SMS


def test_send_fax_encodes_file_and_posts(mock_requests, tmp_path):
    _, post = mock_requests
    pdf = tmp_path / "fax.pdf"
    pdf.write_bytes(b"%PDF-fake")

    result = Fax("u", "p").send_fax(5551234567, "Jose", 5557654321, str(pdf))

    assert result == {"status": "success"}
    sent = post.call_args.kwargs["files"]
    assert sent["method"] == (None, "sendFaxMessage")
    assert base64.b64decode(sent["file"][1]) == b"%PDF-fake"


def test_get_sms_rejects_date_to_without_date_from(mock_requests):
    get, _ = mock_requests
    with pytest.raises(ValueError):
        SMS("u", "p").get_sms(date_to="2026-01-01")
    get.assert_not_called()


def test_get_conference_recordings_rejects_date_to_without_date_from(mock_requests):
    get, _ = mock_requests
    with pytest.raises(ValueError):
        General("u", "p").get_conference_recordings(1, date_to="2026-01-01")
    get.assert_not_called()


def test_create_subaccount_internal_cnam_requires_enable_flag(mock_requests):
    get, _ = mock_requests
    Accounts("u", "p").create_subaccount(
        "user", password="x", internal_cnam="Front Desk", enable_internal_cnam=1
    )
    assert get.call_args.kwargs["params"]["internal_cnam"] == "Front Desk"

    # The flag given as a string ('0') must be rejected too.
    get.reset_mock()
    with pytest.raises(ValueError):
        Accounts("u", "p").create_subaccount(
            "user", password="x", internal_cnam="Front Desk", enable_internal_cnam="0"
        )
    get.assert_not_called()


def test_send_fax_missing_file_raises(mock_requests):
    _, post = mock_requests
    with pytest.raises(FileNotFoundError):
        Fax("u", "p").send_fax(5551234567, "Jose", 5557654321, "/nonexistent.pdf")
    post.assert_not_called()


def test_get_portability_keeps_1x_response_shape(mock_requests):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "success", "portable": "yes"}
    assert LNP("u", "p").get_portability(5551234567) == {
        "did": 5551234567, "result": {"status": "success", "portable": "yes"},
    }


def test_update_of_missing_item_raises(mock_requests):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "no_ringgroup"}
    with pytest.raises(ValueError):
        RingGroups("u", "p").update_ring_group(123, name="x")


def test_create_ring_group_only_looks_up_main_account_without_members(mock_requests):
    get, _ = mock_requests
    get.return_value.json.return_value = {"status": "success", "accounts": [{"account": "123456_office"}]}

    RingGroups("u", "p").create_ring_group("Sales", 1001, members="fwd:1")
    assert [c.kwargs["params"]["method"] for c in get.call_args_list] == ["setRingGroup"]
    assert get.call_args.kwargs["params"]["members"] == "fwd:1"

    get.reset_mock()
    RingGroups("u", "p").create_ring_group("Sales", 1001)
    assert [c.kwargs["params"]["method"] for c in get.call_args_list] == ["getSubAccounts", "setRingGroup"]
    assert get.call_args.kwargs["params"]["members"] == "account:123456"
