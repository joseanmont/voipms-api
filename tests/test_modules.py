import base64

from voipms_api import Accounts, Fax, General, SMS


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
    assert SMS("u", "p").get_sms(date_to="2026-01-01") is None
    get.assert_not_called()


def test_get_conference_recordings_rejects_date_to_without_date_from(mock_requests):
    get, _ = mock_requests
    result = General("u", "p").get_conference_recordings(1, date_to="2026-01-01")
    assert result is None
    get.assert_not_called()


def test_create_subaccount_internal_cnam_requires_enable_flag(mock_requests):
    get, _ = mock_requests
    Accounts("u", "p").create_subaccount(
        "user", password="x", internal_cnam="Front Desk", enable_internal_cnam=1
    )
    assert get.call_args.kwargs["params"]["internal_cnam"] == "Front Desk"

    # The flag given as a string ('0') must be rejected too.
    get.reset_mock()
    assert Accounts("u", "p").create_subaccount(
        "user", password="x", internal_cnam="Front Desk", enable_internal_cnam="0"
    ) is None
    get.assert_not_called()
