"""VoIP.ms CDR (call detail records), call recordings and call transcriptions."""

import base64
from .voipms_client import VoipMsClient
from datetime import datetime
from typing import Optional, Union


class CDR(VoipMsClient):
    """
    CDR, call recording and call transcription operations for the VoIP.ms API.

    Methods:
        get_cdr(date_from, date_to, timezone, ...): Get the call detail records for a date range.
        get_call_accounts(): List the accounts that can be used to filter CDR and recordings.
        get_call_billing(): List the call billing values that can be used to filter CDR.
        get_call_types(): List the call types that can be used to filter CDR and transcriptions.
        get_call_recordings(account, date_from, date_to, ...): List the call recordings of an account.
        get_call_recording(account, call_recording, file_path): Get a call recording, optionally saving the audio.
        delete_call_recording(account, call_recording): Delete a call recording.
        send_call_recording_email(account, call_recording, email): Email a call recording.
        get_call_transcriptions(account, date_from, date_to, ...): Get call transcriptions, optionally saving them as text.
    """

    def get_cdr(
        self,
        date_from: str,
        date_to: str,
        timezone: Union[int, float],
        answered: bool = True,
        noanswer: bool = True,
        busy: bool = True,
        failed: bool = True,
        call_type: Optional[str] = None,
        call_billing: Optional[str] = None,
        account: Optional[str] = None,
    ) -> dict:
        """
        Get the call detail records for a date range (VoIP.ms getCDR).

        Args:
            date_from: Start date (e.g. '2026-11-01').
            date_to: End date (e.g. '2026-11-09'). Must be >= date_from.
            timezone: Offset applied to the call times, from -12 to 13 (e.g. -6).
            answered: Include answered calls. Default True.
            noanswer: Include unanswered calls. Default True.
            busy: Include busy calls. Default True.
            failed: Include failed calls. Default True.
            call_type: Filter by call type. See get_call_types.
            call_billing: Filter by call billing. See get_call_billing.
            account: Filter by account (e.g. '100000_VoIP'). See get_call_accounts.

        Returns:
            API response with the records in 'cdr'. Status 'no_cdr' means there are no records.

        Raises:
            ValueError: If a date is not in YYYY-MM-DD format, date_to is before date_from, or timezone is out of range.
        """

        mtd = "getCDR"

        _check_date_range(date_from, date_to)
        if not -12 <= timezone <= 13:
            raise ValueError("The timezone must be between -12 and 13.")

        params = {
            "date_from": date_from,
            "date_to": date_to,
            "timezone": timezone,
            "answered": int(answered),
            "noanswer": int(noanswer),
            "busy": int(busy),
            "failed": int(failed),
        }

        # Optional in this package.
        if call_type:
            params["calltype"] = call_type
        if call_billing:
            params["callbilling"] = call_billing
        if account:
            params["account"] = account

        data = self.get(mtd, params)
        return data

    def get_call_accounts(self) -> dict:
        """
        List the accounts that can be used to filter CDR and call recordings (VoIP.ms getCallAccounts).

        Returns:
            API response with the accounts.
        """
        mtd = "getCallAccounts"

        data = self.get(mtd)
        return data

    def get_call_billing(self) -> dict:
        """
        List the call billing values that can be used to filter CDR (VoIP.ms getCallBilling).

        Returns:
            API response with the call billing values.
        """
        mtd = "getCallBilling"

        data = self.get(mtd)
        return data

    def get_call_types(self) -> dict:
        """
        List the call types that can be used to filter CDR and call transcriptions (VoIP.ms getCallTypes).

        Returns:
            API response with the call types.
        """
        mtd = "getCallTypes"

        data = self.get(mtd)
        return data

    def get_call_recordings(
        self,
        account: str,
        date_from: str,
        date_to: str,
        call_type: Optional[str] = None,
        start: Optional[int] = None,
        length: Optional[int] = None,
    ) -> dict:
        """
        List the call recordings of an account (VoIP.ms getCallRecordings).

        Args:
            account: Account to get the recordings from (e.g. '100000_VoIP'). See get_call_accounts.
            date_from: Start date (e.g. '2026-11-01').
            date_to: End date (e.g. '2026-11-09'). Must be >= date_from.
            call_type: 'all', 'incoming' or 'outgoing'.
            start: Number of records to skip, for pages (e.g. 50).
            length: Number of records to return (e.g. 25).

        Returns:
            API response with the recordings in 'recordings'. Use their 'callrecording' value with
            get_call_recording, delete_call_recording and send_call_recording_email.

        Raises:
            ValueError: If a date is invalid, date_to is before date_from, or call_type is not accepted.
        """

        mtd = "getCallRecordings"

        _check_date_range(date_from, date_to)
        if call_type and call_type not in ("all", "incoming", "outgoing"):
            raise ValueError("call_type must be 'all', 'incoming' or 'outgoing'.")

        params = {
            "account": account,
            "date_from": date_from,
            "date_to": date_to,
        }

        # Optional in this package.
        if call_type:
            params["call_type"] = call_type
        if start is not None:
            params["start"] = start
        if length is not None:
            params["length"] = length

        data = self.get(mtd, params)
        return data

    def get_call_recording(
        self,
        account: str,
        call_recording: str,
        file_path: Optional[str] = None,
    ) -> dict:
        """
        Get a call recording, optionally saving the audio to a file (VoIP.ms getCallRecording).

        Args:
            account: Main account or sub account of the recording (e.g. '100000_VoIP').
            call_recording: Recording ID ('callrecording' value from get_call_recordings).
            file_path: Optional path to save the audio to (e.g. 'call.mp3').

        Returns:
            API response with the recording details and the audio in base64 ('base64file').

        Raises:
            ValueError: If file_path is given and the recording was not found.
        """

        mtd = "getCallRecording"

        params = {
            "account": account,
            "callrecording": call_recording,
        }

        data = self.get(mtd, params)

        if file_path:
            if not data.get("base64file"):
                raise ValueError("Call recording not found.")
            # b64decode drops the characters outside base64, like the quotes and '\' that the API may add.
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(data["base64file"]))

        return data

    def delete_call_recording(self, account: str, call_recording: str) -> dict:
        """
        Delete a call recording (VoIP.ms delCallRecording).

        Args:
            account: Account of the recording (e.g. '100000_VoIP').
            call_recording: Recording ID ('callrecording' value from get_call_recordings).

        Returns:
            API response with status.
        """

        mtd = "delCallRecording"

        params = {
            "account": account,
            "callrecording": call_recording,
        }

        data = self.get(mtd, params)
        return data

    def send_call_recording_email(self, account: str, call_recording: str, email: str) -> dict:
        """
        Email a call recording (VoIP.ms sendCallRecordingEmail).

        Args:
            account: Account of the recording (e.g. '100000_VoIP').
            call_recording: Recording ID ('callrecording' value from get_call_recordings).
            email: Email address to send the recording to.

        Returns:
            API response with status and a confirmation message ('msg').
        """

        mtd = "sendCallRecordingEmail"

        params = {
            "account": account,
            "callrecording": call_recording,
            "email": email,
        }

        data = self.get(mtd, params)
        return data

    def get_call_transcriptions(
        self,
        account: str,
        date_from: str,
        date_to: str,
        call_type: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> dict:
        """
        Get the call transcriptions of an account, optionally saving them as text (VoIP.ms getCallTranscriptions).

        Args:
            account: Account to get the transcriptions from (e.g. '100001_VoIP').
            date_from: Start date (e.g. '2026-11-01').
            date_to: End date (e.g. '2026-11-09'). Must be >= date_from.
            call_type: Filter by call type. See get_call_types.
            file_path: Optional path to save the transcriptions as readable text (e.g. 'transcriptions.txt').
                Nothing is written when there are no transcriptions.

        Returns:
            API response with the transcriptions in 'transcriptions'.

        Raises:
            ValueError: If a date is invalid or date_to is before date_from.
        """

        mtd = "getCallTranscriptions"

        _check_date_range(date_from, date_to)

        params = {
            "account": account,
            "date_from": date_from,
            "date_to": date_to,
        }

        # Optional in this package.
        if call_type:
            params["call_type"] = call_type

        data = self.get(mtd, params)

        if file_path and data.get("transcriptions"):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("\n\n".join(_format_transcription(t) for t in data["transcriptions"]) + "\n")

        return data


def _check_date_range(date_from: str, date_to: str) -> None:
    """Raise ValueError if a date is not YYYY-MM-DD or date_to is before date_from."""
    try:
        df = datetime.strptime(date_from, '%Y-%m-%d')
        dt = datetime.strptime(date_to, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Dates must be in YYYY-MM-DD format (e.g. '2026-11-01').") from None
    if df > dt:
        raise ValueError("The TO date cannot be prior the FROM date")


def _format_transcription(transcription: dict) -> str:
    """Render one transcription as text: a header line, then one line per phrase with the speaker's number."""
    speakers = transcription.get("speakers") or {}
    # The API returns the speakers indexed from 1; JSON may turn that into a dict or a list.
    if isinstance(speakers, list):
        speakers = {str(i): number for i, number in enumerate(speakers, start=1)}

    header = (
        f"{transcription.get('date')} ({transcription.get('duration')}) - "
        f"{transcription.get('locale')}, confidence {transcription.get('confidence')}"
    )
    lines = [header]
    for phrase in transcription.get("recognized_phrases") or []:
        speaker = str(phrase.get("speaker"))
        lines.append(f"[{phrase.get('time')}] {speakers.get(speaker, 'Speaker ' + speaker)}: {phrase.get('phrase')}")
    return "\n".join(lines)
