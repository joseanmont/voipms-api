import requests, os
from typing import Optional
from urllib.parse import quote, quote_plus

from .errors import VoipMsApiError, VoipMsConnectionError

class VoipMsClient:

    """
    Client for the VoIP.ms REST API.

    Attributes:
        username (str or None): Account email address. Set from argument or VOIPMS_API_USER.
        password (str or None): API password. Set from argument or VOIPMS_API_PASSWORD.
        voipms_url (str): Base URL for the API (default: https://voip.ms/api/v1/rest.php).
        verify (bool): Whether to verify SSL certificates for requests. Default True.
        timeout (float): Seconds to wait for the API before giving up. Default 30.

    Important:
        The VoIP.ms API must be enabled and the calling IP must be allowed in the VoIP.ms Customer Portal.

    Methods:
        get(method, params): Send a GET request to the API.
        post(method, params): Send a POST request to the API.
        test_connection(): Verify credentials and that the current IP is allowed to use the API.
    """


    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        verify: bool = True,
        timeout: float = 30,
    ) -> None:
        """
        Initialize the API client.

        Args:
            username: Account email. If omitted, read from environment variable VOIPMS_API_USER.
            password: API password. If omitted, read from environment variable VOIPMS_API_PASSWORD.
            verify: If False, disable SSL certificate verification. Do not use in production.
            timeout: Seconds to wait for the API before giving up. Default 30.
        """
        # Create a .env file to load your credentials using the environment variables below.
        # Otherwise the credentials must be provided when creating the VoipMsClient object.
        self.voipms_url = "https://voip.ms/api/v1/rest.php"
        
        if (username and not password) or (password and not username):
            raise ValueError("Both username and password must be provided together")

        self.username = username or os.environ.get("VOIPMS_API_USER")
        self.password = password or os.environ.get("VOIPMS_API_PASSWORD")
        self.verify = verify
        self.timeout = timeout

    
    def get(self, method: str, params: Optional[dict] = None) -> dict:
        """
        Send a GET request to the VoIP.ms API.

        Args:
            method: API method name (e.g. 'getBalance', 'getIP').
            params: Optional query parameters to send with the request. Auth and method are added automatically.

        Returns:
            Parsed JSON response from the API. For query methods ('get...') a 'no_...' status
            (e.g. 'no_sms') means there are no results and is returned as is.

        Raises:
            VoipMsApiError: The API returned an error status.
            VoipMsConnectionError: The API could not be reached or returned an invalid response.
        """
        return self._request("GET", method, params)


    def post(self, method: str, params: Optional[dict] = None) -> dict:
        """
        Send a POST request to the VoIP.ms API.

        Parameters are sent as multipart/form-data in the request body, so it is suitable for large payloads (e.g. fax files).

        Args:
            method: API method name (e.g. 'createSubAccount').
            params: Optional form parameters. Auth and method are added automatically.

        Returns:
            Parsed JSON response from the API. For query methods ('get...') a 'no_...' status
            (e.g. 'no_sms') means there are no results and is returned as is.

        Raises:
            VoipMsApiError: The API returned an error status.
            VoipMsConnectionError: The API could not be reached or returned an invalid response.
        """
        return self._request("POST", method, params)


    def _request(self, http_method: str, method: str, params: Optional[dict]) -> dict:
        # Copy so the caller's dict is not modified, then include authentication details.
        params = {
            **(params or {}),
            'api_username': self.username,
            'api_password': self.password,
            'method': method,
        }

        try:
            if http_method == "POST":
                # The API only accepts POST as multipart/form-data (any other encoding returns HTTP 500).
                fields = {key: (None, str(value)) for key, value in params.items() if value is not None}
                response = requests.post(self.voipms_url, files=fields, verify=self.verify, timeout=self.timeout)
            else:
                response = requests.get(self.voipms_url, params=params, verify=self.verify, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            # 'from None' drops the original exception, whose message includes the URL with the password.
            raise VoipMsConnectionError(f"{method}: {self._redact(str(err))}") from None

        try:
            data = response.json()
        except ValueError:
            raise VoipMsConnectionError(
                f"{method}: the API returned an invalid response (HTTP {response.status_code})"
            ) from None

        status = data.get("status") if isinstance(data, dict) else None
        if status == "success":
            return data
        # 'no_...' on a query only means there are no results (e.g. 'no_sms' on getSMS).
        if method.startswith("get") and str(status).startswith("no_"):
            return data
        raise VoipMsApiError(method, status, data)


    def _first(self, response: dict, key: str, what: str) -> dict:
        """Return the first item under 'key' of a query response, or raise ValueError if there is none."""
        items = response.get(key)
        if not items:
            raise ValueError(f"{what} not found.")
        return items[0]


    def _main_account(self) -> str:
        """Return the main account number (e.g. '100000'), taken from the first sub account."""
        subaccounts = self.get("getSubAccounts")
        account = self._first(subaccounts, "accounts", "Sub Account (needed to find the main account number)")
        return account["account"].split("_")[0]


    def _redact(self, text: str) -> str:
        """Remove the API password (plain and URL-encoded) from a text."""
        if self.password:
            for secret in {self.password, quote(self.password), quote_plus(self.password)}:
                text = text.replace(secret, "***")
        return text


    def test_connection(self) -> dict:
        """
        Verify that credentials work and the current IP is allowed to use the API.

        Returns:
            Parsed JSON response including status and the public IP address seen by the API.

        Raises:
            VoipMsApiError: The credentials are invalid or the IP is not allowed (e.g. 'ip_not_enabled').
        """
        return self.get("getIP")
