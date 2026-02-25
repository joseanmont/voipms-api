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
    ) -> None:
        """
        Initialize the API client.

        Args:
            username: Account email. If omitted, read from environment variable VOIPMS_API_USER.
            password: API password. If omitted, read from environment variable VOIPMS_API_PASSWORD.
            verify: If False, disable SSL certificate verification. Do not use in production.
        """
        # Create a .env file to load your credentials using the environment variables below.
        # Otherwise the credentials must be provided when creating the VoipMsClient object.
        self.voipms_url = "https://voip.ms/api/v1/rest.php"
        
        if (username and not password) or (password and not username):
            raise ValueError("Both username and password must be provided together")

        self.username = username if username or username != None else os.environ.get("VOIPMS_API_USER")
        self.password = password if password or password != None else os.environ.get("VOIPMS_API_PASSWORD")
        self.verify = verify

    
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

        if not self.verify:
            response = requests.get(self.voipms_url, params=params, verify=False) # Certificate won't be verified
        else:
            response = requests.get(self.voipms_url, params=params)

        # print(f"Request URL: {response.request.url}\n") # Uncomment to print the full URL
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response = response.json()
        return response
    

    def post(self, method: str, params: Optional[dict] = None) -> dict:
        """
        Send a POST request to the VoIP.ms API.

        Args:
            method: API method name (e.g. 'createSubAccount').
            params: Optional form/query parameters. Auth and method are added automatically.

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
        
        if not self.verify:
            response = requests.post(self.voipms_url, params=params, verify=False) # Certificate won't be verified
        else:
            response = requests.post(self.voipms_url, params=params)

        response.raise_for_status()  # Raises an HTTPError for bad responses
        response = response.json()
        return response
    
    
    def test_connection(self) -> dict:
        """
        Verify that credentials work and the current IP is allowed to use the API.

        Returns:
            Parsed JSON response including status and the public IP address seen by the API.
        """
        params = {
            'api_username': self.username,
            'api_password': self.password,
            'method': 'getIP'
        }

        response = requests.get(self.voipms_url, params=params)
        # print(f"Request URL: {response.request.url}\n") # Uncomment to print the full URL
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response = response.json()
        return response