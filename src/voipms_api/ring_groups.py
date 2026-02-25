"""VoIP.ms ring groups management."""

import requests
from voipms_client import VoipMsClient
from accounts import Accounts
from typing import Optional, Union


class RingGroups(VoipMsClient):
    """
    Ring group operations for the VoIP.ms API.

    Methods:
        create_ring_group(name, voicemail, ...): Create a ring group.
        delete_ring_group(ring_group): Delete a ring group by ID.
        get_ring_groups(ring_group): List ring groups or get one by ID.
        update_ring_group(id, ...): Update an existing ring group.
    """

    def create_ring_group(
        self,
        name: str,
        voicemail: Union[str, int],
        members: Optional[str] = None,
        announcement: Optional[str] = None,
        music_on_hold: Optional[str] = None,
        language: Optional[str] = None,
    ) -> dict:
        """
        Create a new ring group (VoIP.ms setRingGroup).

        Args:
            name: Display name for the ring group.
            voicemail: Voicemail ID to assign. See get_voicemails.
            members: Semicolon-separated members (e.g. 'account:100001;fwd:16006'). Default is main account only.
            announcement: Caller announcement.
            music_on_hold: Music on hold. See get_music_on_hold.
            language: Language code. See get_languages.

        Returns:
            API response with the created ring group data.
        """
        
        mtd = "setRingGroup"

        # Code to get the Account number to set the Main Account as the default member so it is not required.
        accounts = Accounts(self.username, self.password)
        get_accounts = accounts.get_subaccounts()
        acc_number = get_accounts['accounts'][0]['account']
        acc_number = acc_number[0:6]
        default_member = "account:" + acc_number

        try:
            params = {
                # Required by this package
                "name": name,
                "voicemail": voicemail,

                # Required by VoIP.ms API but set with a default value so it is not required.
                "members": default_member,
            }

            # Optional in this package.
            if members:
                params["members"] = members
            if announcement:
                params["caller_announcement"] = announcement
            if music_on_hold:
                params["music_on_hold"] = music_on_hold
            if language:
                params["language"] = language
            
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
        

    def delete_ring_group(self, ring_group: Union[str, int]) -> dict:
        """
        Delete a ring group by ID (VoIP.ms delRingGroup).

        Args:
            ring_group: Ring group ID to delete (e.g. 18635). Use get_ring_groups to list IDs.

        Returns:
            API response with result and ring group name.
        """
        
        mtd = "delRingGroup"

        try:
            params = {
                "ringgroup": ring_group,
            }

            # Code to get the name of the ring group that is deleted.
            rg_info = self.get_ring_groups(ring_group)
            rg_name = rg_info["ring_groups"][0]["name"]

            data = self.get(mtd, params)
            data["ring_group"] = rg_name
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
        

    def get_ring_groups(self, ring_group: Optional[Union[str, int]] = None) -> dict:
        """
        List ring groups or get one by ID (VoIP.ms getRingGroups).

        Args:
            ring_group: Optional ring group ID (e.g. 18635). If omitted, all are returned.

        Returns:
            API response with all ring groups or the requested one.
        """
        
        mtd = "getRingGroups"

        try:
            params = {}

            # Optional in this package.
            if ring_group:
                params["ring_group"] = ring_group
            
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
        

    def update_ring_group(
        self,
        id: Union[str, int],
        name: Optional[str] = None,
        voicemail: Optional[Union[str, int]] = None,
        members: Optional[str] = None,
        announcement: Optional[str] = None,
        music_on_hold: Optional[str] = None,
        language: Optional[str] = None,
    ) -> dict:
        """
        Update an existing ring group (VoIP.ms setRingGroup).

        Args:
            id: Ring group ID to update. Use get_ring_groups to list IDs.
            name: Display name for the ring group.
            voicemail: Voicemail ID. See get_voicemails.
            members: Semicolon-separated members (e.g. 'account:100001;fwd:16006').
            announcement: Caller announcement.
            music_on_hold: Music on hold. See get_music_on_hold.
            language: Language code. See get_languages.

        Returns:
            API response with updated ring group data.
        """
        
        mtd = "setRingGroup"

        try:
            # Code to get the settings of the ring group that will be updated.
            rg_config = self.get_ring_groups(id)
            # Saving the current settings in the parameters.
            params = rg_config["ring_groups"][0]

            # Optional in this package.
            if name:
                params["name"] = name
            if voicemail:
                params["voicemail"] = voicemail
            if members:
                params["members"] = members
            if announcement:
                params["caller_announcement"] = announcement
            if music_on_hold:
                params["music_on_hold"] = music_on_hold
            if language:
                params["language"] = language
            
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