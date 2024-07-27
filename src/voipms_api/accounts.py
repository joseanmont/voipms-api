import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class Accounts():
    '''
    A class to call the Sub Accounts functions of the VoIP.ms API.

    Methods:
        create_subaccount:
            Creates a Sub Account and returns the result of the request.
    '''

    def __init__(self, username=None, password=None) -> None:
        
        if (username and not password) or (password and not username):
            raise ValueError("Both username and password must be provided together")
        elif(username and password):
            self.username = username
            self.password = password
            self.vms_client = VoipMsClient(self.username, self.password)
        else:
            self.vms_client = VoipMsClient()

    
    def create_subaccount(self, 
            username:str,
            password:str,
            extension:Optional[Union[str, int]]=None,
            protocol:Optional[Union[str, int]]=1,
            auth_type:Optional[Union[str, int]]=1,
            device_type:Optional[Union[str, int]]=2,
        ) -> dict:
        """
        Calls the VoIP.ms createSubAccount function.

        Args:
            username (str, required): Username to set to the sub account (Example: 'VoIP').
            password (str, required): Password to set for the authentication.
            extension str or int, optional): Sub Account Internal Extension (Example: 1 -> Creates 101).
            protocol (str or int, optional): The protocol the sub account will use. Default is '1' for SIP (value from get_Protocols).
            auth_type (str or int, optional): The authentication type the sub account will use. Default is '1' for User/Password (value from get_auth_types).
            device_type (str or int, optional): Device type that will be used. Default is '2' for ATA device, IP Phone or Softphone (value from get_device_types).

        Returns:
            dict: A dictionary containing the status of the request and the Sub Account that was created.
        """
        
        mtd = "createSubAccount"

        try:
            params = {

                # Required by this package.
                "username": username,
                "password": password,

                # Required by the VoIP.ms API but set with default values in this package.
                "lock_international": 1,
                "international_route": 1,
                "music_on_hold": "default",
                "allowed_codecs": "g722",
                "dtmf_mode": "auto",
                "nat": "yes",
            }

            # Optional parameters in this package.
            if protocol:
                params["protocol"] = protocol
            if auth_type:
                params["auth_type"] = auth_type
            if device_type:
                params["device_type"] = device_type
            if extension:
                params["internal_extension"] = extension
            
            data = self.vms_client.make_request(mtd, params)
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        

    def delete_subaccount(self, 
            id:Union[str, int],
        ) -> dict:
        """
        Calls the VoIP.ms delSubAccount function.

        Args:
            id (str or int, required): ID of the Sub Account that will be deleted(Example: '99785' or 99785). Value from get_subaccounts.

        Returns:
            dict: A dictionary containing the status of the request and the Sub Account that was canceled.
        """
        
        mtd = "delSubAccount"

        try:
            params = {
                "id": id,
            }
            
            data = self.vms_client.make_request(mtd, params)
            data["result"] = "Sub Account deleted"
            data["id"] = id
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        

    def get_subaccounts(self, 
            subaccount:Optional[Union[str, int]]=None
        ) -> dict:
        """
        Calls the VoIP.ms getSubAccounts function.

        Args:
            subaccount str or int, optional): Sub Account ID or username (Example: '100000_SubAccount' or 99785).

        Returns:
            dict: A dictionary containing the status of the request and the Sub Accounts and their data, or a specific Sub Account data if an ID or username is provided.
        """
        
        mtd = "getSubAccounts"

        try:
            params = {}

            if subaccount:
                params["account"] = subaccount
            
            data = self.vms_client.make_request(mtd, params)
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None