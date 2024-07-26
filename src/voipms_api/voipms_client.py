import requests, os
from typing import Optional

class VoipMsClient:

    """
    A class to connect to the VoIP.ms API.

    Attributes:
        username (str): Your VoIP.ms account email address.
        password (str): Your VoIP.ms API password

        IMPORTANT: The VoIP.ms API must be enabled and the IP address that will consume the API must be allowed in the VoIP.ms Customer Portal.

    Methods:
        make_request():
            Establishes the connection with VoIP.ms API and takes care of sending the request.
    """


    def __init__(self, username:Optional[str]=None, password:Optional[str]=None) -> None:
        """
        Constructs the necessary attributes to connect to the VoIP.ms API.

        Args:
            username (str, optional): Loads the username from the .env file or can be provided when calling the class.
            password (str, optional): Pulls the password from the .env file or can be provided when calling the class.
        """

        # Create a .env file to load your credentials using the enviroment variables below.
        # Otherwise the credentials must be provided when creating the VoipMsClient object.
        self.voipms_url = "https://voip.ms/api/v1/rest.php"
        self.username = username if username else os.environ.get("VOIPMS_API_USER")
        self.password = password if password else os.environ.get("VOIPMS_API_PASSWORD")

    
    def make_request(self, method:str, params:Optional[dict]=None) -> dict:
        """
        Establishes the connection with the VoIP.ms API and takes care of sending the request.

        Returns:
            dict: A dictionary containing the status and data returned from the VoIP.ms API.
        """

        if params is None:
            params = {}
        # Include authentication details in the parameters
        params.update({
            'api_username': self.username,
            'api_password': self.password,
            'method': method
        })
        
        response = requests.get(self.voipms_url, params=params)
        # print(f"Request URL: {response.request.url}\n") # Uncomment to print the full URL
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response = response.json()
        return response
    
    def test_connection(self):
        """
        Tests the connection with the VoIP.ms API.

        Returns:
            dict: A dictionary containing the status and the IP address that is consuming the API.
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