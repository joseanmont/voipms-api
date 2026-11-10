"""Exceptions raised by the voipms_api package."""

from typing import Optional


class VoipMsError(Exception):
    """Base class for all errors raised when calling the VoIP.ms API."""


class VoipMsConnectionError(VoipMsError):
    """
    The API could not be reached or did not return a valid response
    (network error, timeout, HTTP error, invalid JSON).

    The message never includes the request URL, which carries the API password.
    """


class VoipMsApiError(VoipMsError):
    """
    The API answered with a status other than 'success' (e.g. 'invalid_did', 'ip_not_enabled').

    Attributes:
        method (str): API method that was called (e.g. 'cancelDID').
        status (str or None): Status returned by the API.
        response (dict): Full parsed response from the API.
    """

    def __init__(self, method: str, status: Optional[str], response: dict) -> None:
        self.method = method
        self.status = status
        self.response = response
        super().__init__(f"{method} failed with status '{status}'")
