import requests
from typing import Optional, Union


class Voicemail():
    '''
    A class to call the Voicemail functions of the VoIP.ms API.

    Methods:
        create_voicemail:
            Creates a new voicemail and returns the result of the request.
        delete_voicemail:
            Deletes a specific voicemail and returns the result of the request.
        get_voicemails:
            Returns all the existing Voicemails, or a specific Voicemail if a Voicemail ID or Client ID is provided.
        update_voicemail:
            Updates the configuration of a voicemail and returns the result of the request.
    '''

    def __init__(self, username=None, password=None) -> None:
        
        from voipms_api import VoipMsClient

        if (username and not password) or (password and not username):
            raise ValueError("Both username and password must be provided together")
        elif(username and password):
            self.username = username
            self.password = password
            self.vms_client = VoipMsClient(self.username, self.password)
        else:
            self.vms_client = VoipMsClient()

    
    def create_voicemail(self, 
            id:Union[str, int],
            name:str,
            password:int,
            skip_password:Optional[str]='no',
            email:Optional[str]=None,
            attach_message:Optional[str]='yes',
            delete_message:Optional[str]='no',
            timezone:Optional[str]='US/Eastern',
            language:Optional[str]='en',
            client:Optional[Union[str, int]]=None,
        ) -> dict:
        """
        Calls the VoIP.ms createVoicemail function.

        Args:
            id (str or int, required): ID number of the Voicemail (Example: '1' or 101 | Minimum 1 digit, maximum 10).
            name (str, required): Name of the voicemail.
            password (int, required): Password to set for the authentication to access the voicemail (4 digits mandatory).
            skip_password (str, optional): Defines if the password will be skipped or not (Default is 'no').
            email (str, optional): Email address to receive the notifications and the messages. Accepts multiple voicemails separated by commas.
            attach_message (str, optional): Defines if the audio file will be attached to the email (Default is 'yes').
            delete_message (str, optional): Defines if the messages will be deleted from the portal after sent to the email (Default is 'no').
            timezone (str, optional): The Time Zone of the voicemail (Default is 'America/New York' | Values from get_time_zones).
            language (str, optional): The language of the voicemail (Default is 'en' for English | Values from get_languages).
            client (str or int, optional): The ID of a Reseller client's account.

        Returns:
            dict: A dictionary containing the status of the request and the voicemail that was created.
        """
        
        mtd = "createVoicemail"

        try:
            params = {
                # Required in this package.
                "digits": id,
                "name": name,
                "password": password,

                 # Required by VoIP.ms API but set with default values in this package so they're not required.
                "say_time": "yes",
                "say_callerid": "yes",
                "play_instructions": "u",
            }

            # Optional in this package.
            if skip_password:
                params["skip_password"] = skip_password
            if email:
                params["email"] = email
            if attach_message:
                params["attach_message"] = attach_message
            if delete_message:
                params["delete_message"] = delete_message
            if timezone:
                params["timezone"] = timezone
            if language:
                params["language"] = language
            if client:
                params["client"] = client
            
            data = self.vms_client.make_request(mtd, params)
            data["voicemail"] = id
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
        
        
    def delete_voicemail(self, 
            id:Union[str, int],
        ) -> dict:
        """
        Calls the VoIP.ms delVoicemail function.

        Args:
            id (str or int, required): ID number of the Voicemail that will be deleted(Example: '1' or 101).

        Returns:
            dict: A dictionary containing the status of the request and the Voicemail that was canceled.
        """
        
        mtd = "delVoicemail"

        try:
            params = {
                "mailbox": id,
            }
            
            data = self.vms_client.make_request(mtd, params)
            data["result"] = "Voicemail deleted"
            data["voicemail"] = id
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
        

    def get_voicemails(self, 
            voicemail:Optional[Union[str, int]]=None,
            client:Optional[Union[str, int]]=None
        ) -> dict:
        """
        Calls the VoIP.ms getVoicemails function.

        Args:
            voicemail (str or int, optional): ID number of a specific Voicemail (Example: '1001' or 1001).
            client (str or int, optional): ID of a specific Reseller client (Example: '561115' or 561115).

        Returns:
            dict: A dictionary containing the status of the request and the voicemails and their data, or a specific voicemail data if an ID is provided.
        """
        
        mtd = "getVoicemails"

        try:
            params = {}
            
            if voicemail:
                params["mailbox"] = voicemail
            if client:
                params["client"] = client
            
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
        

    def update_voicemail(self, 
            id:Union[str, int],
            name:str=None,
            password:Union[str, int]=None,
            skip_password:Optional[str]=None,
            email:Optional[str]=None,
            attach_message:Optional[str]=None,
            delete_message:Optional[str]=None,
            timezone:Optional[str]=None,
            language:Optional[str]=None,
            client:Optional[Union[str, int]]=None,
        ) -> dict:
        """
        Calls the VoIP.ms setVoicemail function.

        Args:
            id (str or int, required): ID number of the Voicemail (Example: '1' or 101 | Minimum 1 digit, maximum 10).
            name (str, optional): Name of the voicemail.
            password (str or int, optional): Password to set for the authentication to access the voicemail (4 digits mandatory).
            skip_password (str, optional): Defines if the password will be skipped or not.
            email (str, optional): Email address to receive the notifications and the messages. Accepts multiple voicemails separated by commas.
            attach_message (str, optional): Defines if the audio file will be attached to the email (Default is 'yes').
            delete_message (str, optional): Defines if the messages will be deleted from the portal after sent to the email (Default is 'no').
            timezone (str, optional): The Time Zone of the voicemail (Default is 'America/New York' | Values from get_time_zones).
            language (str, optional): The language of the voicemail (Default is 'en' for English | Values from get_languages).
            client (str or int, optional): The ID of a Reseller client's account.

        Returns:
            dict: A dictionary containing the status of the request and the voicemail that was updated.
        """
        
        mtd = "setVoicemail"

        try:
            # Code to get the settings of the ring group that will be updated.
            vm_config = self.get_voicemails(id)
            # Saving the current settings in the parameters.
            params = vm_config["voicemails"][0]

            # VoIP.ms Bug - This verification has been added because get_voicemails will return 'Y' or 'N' for 'transcription' but the VoIP.ms API will not accept these when creating or updating a Voicemail.
            if params["transcription"] == 'N':
                params["transcription"] = ''
            if params["transcription"] == 'Y':
                params["transcription"] = 'yes'

            # Optional in this package.
            if name:
                params["name"] = name
            if password is not None:
                params["password"] = password
            if skip_password:
                params["skip_password"] = skip_password
            if email:
                params["email"] = email
            if attach_message:
                params["attach_message"] = attach_message
            if delete_message:
                params["delete_message"] = delete_message
            if timezone:
                params["timezone"] = timezone
            if language:
                params["language"] = language
            if client:
                params["client"] = client
            
            data = self.vms_client.make_request(mtd, params)
            data["voicemail"] = id
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