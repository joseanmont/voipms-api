"""VoIP.ms call hunting (ring group / find-me) management."""

import requests
from voipms_client import VoipMsClient
from accounts import Accounts
from typing import Optional, Union


class CallHunting(VoipMsClient):
    """
    Call hunting operations for the VoIP.ms API.

    Methods:
        create_call_hunting(name, ...): Create a call hunting and return the result.
        delete_call_hunting(call_hunting): Delete a call hunting by ID.
        get_call_huntings(call_hunting): List all call huntings or one by ID.
        update_call_hunting(id, ...): Update an existing call hunting.
    """

    def create_call_hunting(
        self,
        name: str,
        music: Optional[Union[str, int]] = None,
        recording: Optional[Union[str, int]] = None,
        language: Optional[str] = None,
        order: Optional[str] = None,
        members: Optional[str] = None,
        ring_time: Optional[Union[str, int]] = None,
        press_one: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        Create a new call hunting (VoIP.ms setCallHunting).

        Args:
            name: Display name for the call hunting.
            music: Music on hold while waiting. See get_music_on_hold. Default 'default'.
            recording: Recording ID. See get_recordings. Default 'none:'.
            language: Language code (e.g. 'en'). See get_languages. Default 'en'.
            order: Ring order: 'follow' (member order) or 'random'. Default 'follow'.
            members: Semicolon-separated member list (e.g. 'account:100001;fwd:16006'). See API docs. Default is main account only.
            ring_time: Ring time per member in seconds (multiples of 5). Default 25.
            press_one: 1 = press 1 to accept, 2 = disabled. Default 0.

        Returns:
            API response with the created call hunting data.
        """
        
        mtd = "setCallHunting"

        # Code to get the Account number to set the Main Account as the default member if no members are provided.
        accounts = Accounts(self.username, self.password)
        get_accounts = accounts.get_subaccounts()
        acc_number = get_accounts['accounts'][0]['account']
        acc_number = acc_number[0:6]
        default_member = "account:" + acc_number

        try:
            params = {
                # Required by this package
                "description": name,

                # Required by VoIP.ms API but set with default values so it is not required in this package.
                "music": "default",
                "recording": "none:",
                "language": "en",
                "order": "follow",
                "members": default_member,
                "ring_time": 25,
                "press": 0
            }

            # Optional in this package.
            if music:
                params["music"] = music
            if recording:
                params["recording"] = recording
            if language:
                params["language"] = language
            if order:
                params["order"] = order
            if members:
                params["members"] = members
            if ring_time is not None:
                params["ring_time"] = ring_time
            if press_one is not None:
                params["press"] = press_one
            
            data = self.get(mtd, params)
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
        

    def delete_call_hunting(self, call_hunting: Union[str, int]) -> dict:
        """
        Delete a call hunting by ID (VoIP.ms delCallHunting).

        Args:
            call_hunting: Call hunting ID to delete (e.g. 18635). Use get_call_huntings to list IDs.

        Returns:
            API response with result and call hunting name.
        """
        
        mtd = "delCallHunting"

        try:
            params = {
                "callhunting": call_hunting,
            }

            # Code to get the name of the call hunting that is deleted.
            ch_info = self.get_call_huntings(call_hunting)
            ch_name = ch_info["call_hunting"][0]["description"]

            data = self.get(mtd, params)
            data["call_hunting"] = ch_name
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
        

    def get_call_huntings(self, call_hunting: Optional[Union[str, int]] = None) -> dict:
        """
        List call huntings or get one by ID (VoIP.ms getCallHuntings).

        Args:
            call_hunting: Optional call hunting ID (e.g. 323). If omitted, all are returned.

        Returns:
            API response with all call huntings or the requested one.
        """
        
        mtd = "getCallHuntings"

        try:
            params = {}

            # Optional in this package.
            if call_hunting:
                params["callhunting"] = call_hunting
            
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
        

    def update_call_hunting(
        self,
        id: Union[str, int],
        name: Optional[str] = None,
        music: Optional[Union[str, int]] = None,
        recording: Optional[Union[str, int]] = None,
        language: Optional[str] = None,
        order: Optional[str] = None,
        members: Optional[str] = None,
        ring_time: Optional[Union[str, int]] = None,
        press_one: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        Update an existing call hunting (VoIP.ms setCallHunting).

        Args:
            id: Call hunting ID to update. Use get_call_huntings to list IDs.
            name: Display name for the call hunting.
            music: Music on hold. See get_music_on_hold.
            recording: Recording ID. See get_recordings.
            language: Language code. See get_languages.
            order: 'follow' or 'random'.
            members: Semicolon-separated member list (e.g. 'account:100001;fwd:16006'). Multiple ring times: '20;20;20'.
            ring_time: Ring time in seconds (multiples of 5). For multiple members use '20;20;20'.
            press_one: 1 = enabled, 2 = disabled. For multiple members use '0;0;0'.

        Returns:
            API response with status and updated data.
        """
        
        mtd = "setCallHunting"
        # main_account = "account:" + self.acc_number

        try:
            # Code to get the settings of the call hunting that will be edited.
            ch_config = self.get_call_huntings(id)
            # Saving the current settings in the parameters.
            params = ch_config["call_hunting"][0]

            # Optional in this package.
            if name:
                params["description"] = name
            if music:
                params["music"] = music
            if recording:
                params["recording"] = recording
            if language:
                params["language"] = language
            if order:
                params["order"] = order
            if members:
                params["members"] = members
            if ring_time:
                params["ring_time"] = ring_time
            if press_one is not None:
                params["press"] = press_one
            
            data = self.get(mtd, params)
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