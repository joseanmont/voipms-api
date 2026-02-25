"""VoIP.ms call forwarding management."""

import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class Forwarding(VoipMsClient):
    """
    Call forwarding operations for the VoIP.ms API.

    Methods:
        create_forwarding(phone_number, ...): Create a forwarding and return the result.
        delete_forwarding(forwarding): Delete a forwarding by ID.
        get_forwardings(forwarding): List all forwardings or one by ID.
        update_forwarding(id, ...): Update an existing forwarding.
    """

    def create_forwarding(
        self,
        phone_number: Union[str, int],
        cid_override: Optional[Union[str, int]] = None,
        description: Optional[str] = None,
        dtmf_digits: Optional[Union[str, int]] = None,
        pause: Optional[Union[str, float]] = None,
    ) -> dict:
        """
        Create a new call forwarding (VoIP.ms setForwarding).

        Args:
            phone_number: Destination phone number (e.g. 2052550000).
            cid_override: Optional caller ID override number (e.g. 4042820000).
            description: Optional description for this forwarding.
            dtmf_digits: Optional DTMF digits to send when forwarding (e.g. '101').
            pause: Optional pause in seconds before DTMF (0–10, steps of 0.5, e.g. 1.5).

        Returns:
            API response with the created forwarding data.
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
            
            data = self.get(mtd, params)
            data["forwarding"] = phone_number
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
        

    def delete_forwarding(self, forwarding: Union[str, int]) -> dict:
        """
        Delete a call forwarding by ID (VoIP.ms delForwarding).

        Args:
            forwarding: Forwarding ID to delete (e.g. 18635). Use get_forwardings to list IDs.

        Returns:
            API response with result and the forwarding phone number.
        """
        
        mtd = "delForwarding"

        try:
            params = {
                "forwarding": forwarding,
            }

            # Code to get the phone number of the forwarding that is deleted.
            fwd_info = self.get_forwardings(forwarding)
            fwd_pn = fwd_info["forwardings"][0]["phone_number"]

            data = self.get(mtd, params)
            data["phone_number"] = fwd_pn
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
        
    
    def get_forwardings(self, forwarding: Optional[Union[str, int]] = None) -> dict:
        """
        List call forwardings or get one by ID (VoIP.ms getForwardings).

        Args:
            forwarding: Optional forwarding ID (e.g. 18635). If omitted, all forwardings are returned.

        Returns:
            API response with all forwardings or the requested one.
        """
        
        mtd = "getForwardings"

        try:
            params = {}

            # Optional in this package.
            if forwarding:
                params["forwarding"] = forwarding
            
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
        

    def update_forwarding(
        self,
        id: Union[str, int],
        phone_number: Optional[Union[str, int]] = None,
        cid_override: Optional[Union[str, int]] = None,
        description: Optional[str] = None,
        dtmf_digits: Optional[Union[str, int]] = None,
        pause: Optional[Union[str, float]] = None,
    ) -> dict:
        """
        Update an existing call forwarding (VoIP.ms setForwarding).

        Args:
            id: Forwarding ID to update. Use get_forwardings to list IDs.
            phone_number: New destination number (e.g. 2052550000).
            cid_override: Caller ID override number (e.g. 4042820000).
            description: Description for the forwarding.
            dtmf_digits: DTMF digits to send when forwarding (e.g. '101').
            pause: Pause in seconds before DTMF (0–10, steps of 0.5, e.g. 1.5).

        Returns:
            API response with the updated forwarding data.
        """
        
        mtd = "setForwarding"


        try:
            # Code to get the settings of the forwarding that will be edited.
            fwd_config = self.get_forwardings(id)
            # Saving the current settings in the parameters.
            params = fwd_config["forwardings"][0]

            # Optional in this package.
            if phone_number:
                params["phone_number"] = phone_number
            if cid_override:
                params["callerid_override"] = cid_override
            if description:
                params["description"] = description
            if dtmf_digits:
                params["dtmf_digits"] = dtmf_digits
            if pause is not None:
                params["pause"] = pause
            
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