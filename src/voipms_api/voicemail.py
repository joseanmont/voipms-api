"""VoIP.ms voicemail management."""

import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class Voicemail(VoipMsClient):
    """
    Voicemail operations for the VoIP.ms API.

    Methods:
        create_voicemail(id, name, password, ...): Create a voicemail.
        delete_voicemail(id): Delete a voicemail by ID.
        get_voicemails(voicemail, client): List voicemails or get one by ID/client.
        update_voicemail(id, ...): Update an existing voicemail.
    """

    def create_voicemail(
        self,
        id: Union[str, int],
        name: str,
        password: int,
        skip_password: Optional[str] = 'no',
        email: Optional[str] = None,
        attach_message: Optional[str] = 'yes',
        delete_message: Optional[str] = 'no',
        timezone: Optional[str] = 'US/Eastern',
        language: Optional[str] = 'en',
        client: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        Create a new voicemail (VoIP.ms createVoicemail).

        Args:
            id: Voicemail ID (1–10 digits, e.g. '1' or 101).
            name: Display name for the voicemail.
            password: 4-digit PIN for voicemail access.
            skip_password: 'no' (default) or 'yes' to skip password prompt.
            email: Email for notifications; multiple addresses comma-separated.
            attach_message: 'yes' (default) or 'no' to attach audio to email.
            delete_message: 'no' (default) or 'yes' to delete from portal after email.
            timezone: Timezone (e.g. 'US/Eastern'). See get_time_zones.
            language: Language code (e.g. 'en'). See get_languages.
            client: Reseller client account ID.

        Returns:
            API response with the created voicemail data.
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
            
            data = self.get(mtd, params)
            data["voicemail"] = id
            data["name"] = name
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None
        
        
    def delete_voicemail(self, id: Union[str, int]) -> dict:
        """
        Delete a voicemail by ID (VoIP.ms delVoicemail).

        Args:
            id: Voicemail ID to delete (e.g. '1' or 101).

        Returns:
            API response with result and voicemail id.
        """
        
        mtd = "delVoicemail"

        try:
            params = {
                "mailbox": id,
            }
            
            data = self.get(mtd, params)
            data["result"] = "Voicemail deleted"
            data["voicemail"] = id
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None
        

    def get_voicemails(
        self,
        voicemail: Optional[Union[str, int]] = None,
        client: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        List voicemails or get one by ID/client (VoIP.ms getVoicemails).

        Args:
            voicemail: Optional voicemail ID (e.g. '1001' or 1001).
            client: Optional reseller client ID (e.g. '561115' or 561115).

        Returns:
            API response with all voicemails or the requested one.
        """
        
        mtd = "getVoicemails"

        try:
            params = {}
            
            if voicemail:
                params["mailbox"] = voicemail
            if client:
                params["client"] = client
            
            data = self.get(mtd, params)
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None
        

    def update_voicemail(
        self,
        id: Union[str, int],
        name: Optional[str] = None,
        password: Optional[Union[str, int]] = None,
        skip_password: Optional[str] = None,
        email: Optional[str] = None,
        attach_message: Optional[str] = None,
        delete_message: Optional[str] = None,
        timezone: Optional[str] = None,
        language: Optional[str] = None,
        client: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        Update an existing voicemail (VoIP.ms setVoicemail).

        Args:
            id: Voicemail ID to update (1–10 digits, e.g. '1' or 101).
            name: Display name.
            password: 4-digit PIN for access.
            skip_password: 'no' or 'yes' to skip password prompt.
            email: Email for notifications; comma-separated for multiple.
            attach_message: 'yes' or 'no' to attach audio to email.
            delete_message: 'no' or 'yes' to delete from portal after email.
            timezone: Timezone. See get_time_zones.
            language: Language code. See get_languages.
            client: Reseller client account ID.

        Returns:
            API response with updated voicemail data.
        """
        
        mtd = "setVoicemail"

        try:
            # Code to get the settings of the voicemail that will be updated.
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
            
            data = self.get(mtd, params)
            data["voicemail"] = id
            data["name"] = name
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None