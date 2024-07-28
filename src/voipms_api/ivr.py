import requests
from voipms_client import VoipMsClient
from typing import Optional, Union
from accounts import Accounts


class IVR():
    '''
    A class to call the IVR functions of the VoIP.ms API.

    Methods:
        create_ivr:
            Creates a new IVR and returns the result of the request.
        delete_ivr:
            Deletes a specific IVR and returns the result of the request.
        get_ivr:
            Returns all the existing IVRs, or a specific IVR if an IVR ID is provided.
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

        # Code to get the Account number to set the Main Account as the routing for the options so it is not required.
        accounts = Accounts()
        get_accounts = accounts.get_subaccounts()
        self.acc_number = get_accounts['accounts'][0]['account']
        self.acc_number = self.acc_number[0:6]


    def create_ivr(self, 
            name:str,
            recording:Union[str, int],
            time_out:Optional[Union[str, int]]=None,
            language:Optional[str]=None,
            voicemail:Optional[str]=None,
            options:Optional[str]=None,
        ) -> dict:
        """
        Calls the VoIP.ms setIVR function to create a new IVR.

        Args:
            name (str, required): A name for the new IVR.
            recording (str or int, required): ID of the recording to set to the IVR. Values from get_recordings.
            time_out (str or int, optional): Maximum time to dial in an option after recording. Values from 1 to 10. Default is 5.
            language (str, optional): Language of the IVR. Default  is 'en' for English. Values from get_languages.
            voicemail (str, optional): Voicemail Setup for the IVR. Default  is '1' for use Default DID voicemail. Alternative is '2' for account voicemail.
            options (srt, optional): A string of options separated by semicolons. Default is Main Account for 1 as only choice. (Example: '1=account:100001;2=fwd:16006'). See VoIP.ms API documentation for more details.

        Returns:
            dict: A dictionary containing the status of the request and the name of the IVR that was created.
        """
        
        mtd = "setIVR"
        main_account = "1=account:" + self.acc_number

        try:
            params = {
                # Required by this package
                "name": name,
                "recording": recording,

                # Required by VoIP.ms API but set with default values so it is not required in this package.
                "timeout": 5,
                "language": "en",
                "voicemailsetup": 1,
                "choices": main_account
            }

            # Optional in this package.
            if recording:
                params["recording"] = recording
            if time_out:
                params["timeout"] = time_out
            if language:
                params["language"] = language
            if voicemail:
                params["voicemailsetup"] = voicemail
            if options:
                params["choices"] = options
            
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