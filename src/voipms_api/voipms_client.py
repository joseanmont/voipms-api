import requests, os
from typing import Optional

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
            Parsed JSON response from the API (typically includes 'status' and/or 'data').
        """

        if params is None:
            params = {}
        # Include authentication details in the parameters
        params.update({
            'api_username': self.username,
            'api_password': self.password,
            'method': method
        })
        
        # print(f"{params}/n") # Uncomment this to see username, password and method

        response = requests.get(self.voipms_url, params=params, verify=self.verify, timeout=self.timeout)

        # print(f"Request URL: {response.request.url}\n") # Uncomment to print the full URL
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response = response.json()
        return response
    

    def post(self, method: str, params: Optional[dict] = None) -> dict:
        """
        Send a POST request to the VoIP.ms API.

        Parameters are sent as multipart/form-data in the request body, so it is suitable for large payloads (e.g. fax files).

        Args:
            method: API method name (e.g. 'createSubAccount').
            params: Optional form parameters. Auth and method are added automatically.

        Returns:
            Parsed JSON response from the API (typically includes 'status' and/or 'data').
        """

        if params is None:
            params = {}
        # Include authentication details in the parameters
        params.update({
            'api_username': self.username,
            'api_password': self.password,
            'method': method
        })
        
        # The API only accepts POST as multipart/form-data (any other encoding returns HTTP 500).
        fields = {key: (None, str(value)) for key, value in params.items() if value is not None}
        response = requests.post(self.voipms_url, files=fields, verify=self.verify, timeout=self.timeout)

        response.raise_for_status()  # Raises an HTTPError for bad responses
        response = response.json()
        return response
    
    
    def test_connection(self) -> dict:
        """
        Verify that credentials work and the current IP is allowed to use the API.

        Returns:
            Parsed JSON response including status and the public IP address seen by the API.
        """
        return self.get("getIP")
