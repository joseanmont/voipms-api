import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class Forwarding():
    '''
    A class to call the Forwarding related functions of the VoIP.ms API.

    Methods:
        create_forwarding:
            Creates a new forwarding and returns the result of the request.
        delete_forwarding:
            Deletes a specific forwarding and returns the result of the request.
        get_forwardings:
            Returns all the existing forwardings, or a specific forwarding if a forwarding ID or Client ID is provided.
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


    def create_forwarding(self, 
            phone_number:Union[str, int],
            cid_override:Union[str, int]=None,
            description:Union[str, int]=None,
            dtmf_digits:Union[str, int]=None,
            pause:Union[str, float]=None,
        ) -> dict:
        """
        Calls the VoIP.ms setForwarding function to create a new forwarding.

        Args:
            phone_number (str or int, required): Phone number to add as Forwarding (Example: 2052550000).
            cid_override (str or int, optional): Phone number to override the caller's caller ID number (Example: 4042820000).
            description (str, optional): A description for the forwarding that will be created.
            dtmf_digits (str or int, optional): Digits to be sent as DTMF tones when forwarding the call (Example: 101).
            pause (str or float, optional): Pause in seconds before sending the DTMF digits. From 0 to 10 in increments of 0.5 (Example: 1.5).

        Returns:
            dict: A dictionary containing the status of the request and the forwarding's phone number that was created.
        """
        
        mtd = "setForwarding"

        try:
            params = {
                "phone_number": phone_number,
            }

            # Optional in this package.
            if cid_override:
                params["callerid_override"] = cid_override
            if description:
                params["description"] = description
            if dtmf_digits:
                params["dtmf_digits"] = dtmf_digits
            if pause:
                params["pause"] = pause
            
            data = self.vms_client.make_request(mtd, params)
            data["forwarding"] = phone_number
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
        

    def delete_forwarding(self, 
            forwarding:Optional[Union[str, int]]=None,
        ) -> dict:
        """
        Calls the VoIP.ms delForwarding function.

        Args:
            forwarding (str or int, optional): ID of the forwarding that will be deleted (Example: 18635). Value from get_forwardings.

        Returns:
            dict: A dictionary containing the status of the request and the ID of the forwarding that was deleted.
        """
        
        mtd = "delForwarding"

        try:
            params = {
                "forwarding": forwarding,
            }

            fwd_info = self.get_forwardings(forwarding)
            fwd_pn = fwd_info["forwardings"][0]["phone_number"]

            data = self.vms_client.make_request(mtd, params)
            data["phone_number"] = fwd_pn
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
        
    
    def get_forwardings(self, 
            forwarding:Optional[Union[str, int]]=None,
        ) -> dict:
        """
        Calls the VoIP.ms getForwardings function.

        Args:
            forwarding (str or int, optional): ID of a specific forwarding (Example: 18635).

        Returns:
            dict: A dictionary containing the status of the request and the data of all the forwardings, or the data of a specific forwarding an ID is provided.
        """
        
        mtd = "getForwardings"

        try:
            params = {}

            # Optional in this package.
            if forwarding:
                params["forwarding"] = forwarding
            
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