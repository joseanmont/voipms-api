import requests
from voipms_client import VoipMsClient
from typing import Optional, Union
from accounts import Accounts


class CallHunting():
    '''
    A class to call the Call Hunting functions of the VoIP.ms API.

    Methods:
        create_call_hunting:
            Creates a new Call Hunting and returns the result of the request.
        delete_call_hunting:
            Deletes a specific Call Hunting and returns the result of the request.
        get_call_hunting:
            Returns all the existing Call Huntings, or a specific Call Hunting if a Call Hunting ID is provided.
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

        # Code to get the Account number to set the Main Account as the default member so it is not required.
        accounts = Accounts()
        get_accounts = accounts.get_subaccounts()
        self.acc_number = get_accounts['accounts'][0]['account']
        self.acc_number = self.acc_number[0:6]


    def create_call_hunting(self, 
            name:str,
            recording:Optional[Union[str, int]]=None,
            language:Optional[str]=None,
            order:Optional[str]=None,
            members:Optional[str]=None,
        ) -> dict:
        """
        Calls the VoIP.ms setCallHunting function to create a new Call Hunting.

        Args:
            name (str, required): A name for the new Call Hunting.
            recording (str or int, optional): ID of the recording to set to the Call Hunting. Values from get_recordings.
            language (str, optional): Language of the Call Hunting. Default  is 'en' for English. Values from get_languages.
            order (str, optional): Ring order of the Call Hunting. Default  is 'follow' to follow member's order. Alternative is 'random'.
            members (srt, optional): A string of members separated by semicolons. Default is Main Account as only member. (Example: 'account:100001;fwd:16006'). See VoIP.ms API documentation for more details.

        Returns:
            dict: A dictionary containing the status of the request and the name of the Call Hunting that was created.
        """
        
        mtd = "setCallHunting"
        main_account = "account:" + self.acc_number

        try:
            params = {
                # Required by this package
                "description": name,

                # Required by VoIP.ms API but set with default values so it is not required in this package.
                "music": "default",
                "recording": "default",
                "language": "en",
                "order": "follow",
                "members": main_account,
                "ring_time": 25,
                "press": 0
            }

            # Optional in this package.
            if recording:
                params["recording"] = recording
            if language:
                params["language"] = language
            if order:
                params["order"] = order
            if members:
                params["members"] = members
            
            data = self.vms_client.make_request(mtd, params)
            data["name"] = name
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None
        

    def delete_call_hunting(self, 
            call_hunting:Union[str, int],
        ) -> dict:
        """
        Calls the VoIP.ms delCallHunting function.

        Args:
            call_hunting (str or int, required): ID of the call hunting that will be deleted (Example: 18635). Value from get_call_huntings.

        Returns:
            dict: A dictionary containing the status of the request and the ID of the call hunting that was deleted.
        """
        
        mtd = "delCallHunting"

        try:
            params = {
                "callhunting": call_hunting,
            }

            # Code to get the name of the call hunting that is deleted.
            ch_info = self.get_call_huntings(call_hunting)
            ch_name = ch_info["call_hunting"][0]["description"]

            data = self.vms_client.make_request(mtd, params)
            data["call_hunting"] = ch_name
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None
        

    def get_call_huntings(self, 
            call_hunting:Optional[Union[str, int]]=None,
        ) -> dict:
        """
        Calls the VoIP.ms getCallHuntings function.

        Args:
            call_hunting (str or int, optional): ID of a specific call hunting (Example: 323).

        Returns:
            dict: A dictionary containing the status of the request and the data of all the call huntings, or the data of a specific call hunting if an ID is provided.
        """
        
        mtd = "getCallHuntings"

        try:
            params = {}

            # Optional in this package.
            if call_hunting:
                params["callhunting"] = call_hunting
            
            data = self.vms_client.make_request(mtd, params)
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None