"""VoIP.ms sub-account management."""

import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class Accounts(VoipMsClient):
    """
    Sub-account operations for the VoIP.ms API.

    Methods:
        create_subaccount(username, ...): Create a sub-account and return the result.
        delete_subaccount(id): Delete a sub-account by ID.
        get_subaccounts(subaccount): List all sub-accounts or one by ID/username.
        update_subaccount(subaccount, ...): Update a sub-account's configuration.
    """

    def create_subaccount(
        self,
        username: str,
        auth_type: Optional[Union[str, int]] = 1,
        password: Optional[str] = None,
        ip: Optional[str] = None,
        protocol: Optional[Union[str, int]] = 1,
        device_type: Optional[Union[str, int]] = 2,
        callerid_number: Optional[Union[str, int]] = None,
        internal_extension: Optional[Union[str, int]] = None,
        internal_voicemail: Optional[Union[str, int]] = None,
        internal_cnam: Optional[str] = None,
        enable_internal_cnam: Optional[Union[str, int]] = 0,
        description: Optional[str] = None,
        lock_international: Optional[Union[str, int]] = 1,
        codecs: Optional[str] = "g722",
    ) -> dict:
        """
        Create a new sub-account (VoIP.ms createSubAccount).

        Args:
            username: Sub-account username (e.g. 'VoIP'). Max 12 characters.
            auth_type: Authentication type. 1 = User/Password, 2 = IP (see get_auth_types). Default 1.
            password: Password for auth_type 1. Required when auth_type is 1.
            ip: IP or FQDN for auth_type 2. Required when auth_type is 2.
            protocol: Protocol (e.g. 1 = SIP). Default 1. See get_Protocols.
            device_type: Device type (e.g. 2 = ATA/IP phone/softphone). Default 2. See get_device_types.
            callerid_number: Caller ID number (e.g. 4052550000).
            internal_extension: Internal extension (e.g. 1 creates 101).
            internal_voicemail: Voicemail ID for internal voicemail (e.g. 101).
            internal_cnam: Caller ID name for internal calls.
            enable_internal_cnam: 0 = disabled, 1 = enabled. Default 0.
            description: Description or label for the sub-account.
            lock_international: 1 = international disabled. Default 1. See get_lock_international.
            codecs: Audio codecs (e.g. 'g722'). Default 'g722'. See get_allowed_codecs.

        Returns:
            API response with the created sub-account data.

        Raises:
            ValueError: If auth_type is 1 and password is missing, or auth_type is 2 and ip is missing.
        """
        
        mtd = "createSubAccount"

        try:
            if len(username) > 12:
                raise ValueError("Username characters exceeded.")
            if (auth_type == 1 or auth_type == '1') and not password:
                raise ValueError("Password must be provided for User/Password authentication.")
            if (auth_type == 2 or auth_type == '2') and not ip:
                raise ValueError("IP address must be provided for IP authentication.")
            if (enable_internal_cnam == 0 or auth_type == '0') and internal_cnam:
                raise ValueError("The cnam cannot be set because you did not enable the internal cnam. To fix this error send 'enable_internal_cnam = 1'")

            params = {

                # Required by this package.
                "username": username,

                # Required by the VoIP.ms API but set with default values in this package so they are optional.
                "international_route": 1,
                "music_on_hold": "default",
                "dtmf_mode": "auto",
                "nat": "yes",
            }

            # Optional parameters in this package.
            if auth_type:
                params["auth_type"] = auth_type
            if password:
                params["password"] =  password
            if ip:
                params["ip"] = ip
            if protocol:
                params["protocol"] = protocol
            if device_type is not None:
                params["device_type"] = device_type
            if callerid_number:
                params["callerid_number"] = callerid_number
            if internal_extension:
                params["internal_extension"] = internal_extension
            if internal_voicemail:
                params["internal_voicemail"] = internal_voicemail
            if internal_cnam:
                params["internal_cnam"] = internal_cnam
            if enable_internal_cnam:
                params["enable_internal_cnam"] = enable_internal_cnam
            if description:
                params["description"] = description
            if lock_international is not None:
                params["lock_international"] = lock_international
            if codecs:
                params["allowed_codecs"] = codecs
            
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

    def delete_subaccount(self, id: Union[str, int]) -> dict:
        """
        Delete a sub-account by ID (VoIP.ms delSubAccount).

        Args:
            id: Sub-account ID to delete (e.g. '99785' or 99785). Use get_subaccounts to list IDs.

        Returns:
            API response with result and id.
        """
        
        mtd = "delSubAccount"

        try:
            params = {
                "id": id,
            }
            
            data = self.get(mtd, params)
            data["result"] = "Sub Account deleted"
            data["id"] = id
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

    def get_subaccounts(self, subaccount: Optional[Union[str, int]] = None) -> dict:
        """
        List sub-accounts or get one by ID/username (VoIP.ms getSubAccounts).

        Args:
            subaccount: Optional sub-account ID or username (e.g. '100000_SubAccount' or 99785).

        Returns:
            API response with all sub-accounts or the requested sub-account data.
        """
        
        mtd = "getSubAccounts"

        try:
            params = {}

            if subaccount:
                params["account"] = subaccount
            
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

    def update_subaccount(
        self,
        subaccount: Union[str, int],
        auth_type: Optional[Union[str, int]] = None,
        password: Optional[str] = None,
        ip: Optional[str] = None,
        protocol: Optional[Union[str, int]] = None,
        device_type: Optional[Union[str, int]] = None,
        callerid_number: Optional[Union[str, int]] = None,
        internal_extension: Optional[Union[str, int]] = None,
        internal_voicemail: Optional[Union[str, int]] = None,
        internal_cnam: Optional[str] = None,
        enable_internal_cnam: Optional[str] = None,
        description: Optional[str] = None,
        canada_route: Optional[Union[str, int]] = None,
        lock_international: Optional[Union[str, int]] = None,
        international_route: Optional[Union[str, int]] = None,
        record_calls: Optional[Union[str, int]] = None,
        music_on_hold: Optional[str] = None,
        codecs: Optional[str] = None,
        dtmf_mode: Optional[str] = None,
    ) -> dict:
        """
        Update an existing sub-account (VoIP.ms setSubAccount).

        Args:
            subaccount: Full sub-account name (e.g. '100000_SubAccount'). Must contain '_'.
            auth_type: Authentication type. See get_auth_types.
            password: Password for auth_type 1. Required when auth_type is 1.
            ip: IP or FQDN for auth_type 2. Required when auth_type is 2.
            protocol: Protocol. See get_Protocols.
            device_type: Device type. See get_device_types.
            callerid_number: Caller ID number.
            internal_extension: Internal extension (e.g. 1 creates 101).
            internal_voicemail: Voicemail ID for internal voicemail.
            internal_cnam: Caller ID name for internal calls.
            enable_internal_cnam: '0' = disabled, '1' = enabled.
            description: Description or name for the sub-account.
            canada_route: Route for Canada calls. See get_routes.
            lock_international: International call lock. See get_lock_international.
            international_route: Route for international calls. See get_routes.
            record_calls: Call recording: 1 = on, 0 = off.
            music_on_hold: Music on hold. See get_music_on_hold.
            codecs: Audio codecs. See get_allowed_codecs.
            dtmf_mode: DTMF mode. See get_dtmf_modes.

        Returns:
            API response with status and sub-account identifier.

        Raises:
            ValueError: If subaccount format is invalid, not found, or auth_type requires missing password/ip.
        """
        
        mtd = "setSubAccount"

        try:
            if "_" not in subaccount:
                raise ValueError("This method expects the full sub account name.")

            # Code to get the settings of the sub account that will be edited.
            sa_config = self.get_subaccounts(subaccount)

            if sa_config['status'] == "no_subaccount":
                raise ValueError("Sub Account not found.")
            
            # Saving the current settings in the parameters
            params = sa_config["accounts"][0]

            # Validation to ensure there's no missing parameters based on the authentication type.
            if (auth_type == 1 or auth_type == '1') and not password:
                raise ValueError("Password must be provided for User/Password authentication.")
            if (auth_type == 2 or auth_type == '2') and not ip:
                raise ValueError("IP address must be provided for IP authentication.")
            if (enable_internal_cnam == 0 or auth_type == '0') and internal_cnam:
                raise ValueError("The cnam cannot be set because you did not enable the internal cnam. To fix this error send 'enable_internal_cnam = 1'")
            
            # If the authentication type is changed this validation ensures the password or ip is removed from the parameters to avoid error responses from the VoIP.ms API.
            if params["auth_type"] == '1' and (auth_type == 2 or auth_type == '2'):
                params.pop('password', None)
            if params["auth_type"] == '2' and (auth_type == 1 or auth_type == '1'):
                params.pop('ip', None)

            # Optional parameters in this method.
            if auth_type is not None:
                params["auth_type"] = auth_type
            if password:
                params["password"] =  password
            if ip:
                params["ip"] = ip
            if protocol:
                params["protocol"] = protocol
            if device_type is not None:
                params["device_type"] = device_type
            if callerid_number:
                params["callerid_number"] = callerid_number
            if description:
                params["description"] = description
            if canada_route:
                params["canada_routing"] = canada_route
            if lock_international is not None:
                params["lock_international"] = lock_international
            if international_route:
                params["international_route"] = international_route
            if record_calls is not None:
                params["record_calls"] = record_calls
            if music_on_hold:
                params["music_on_hold"] = music_on_hold
            if internal_extension:
                params["internal_extension"] = internal_extension
            if internal_voicemail:
                params["internal_voicemail"] = internal_voicemail
            if internal_cnam:
                params["internal_cnam"] = internal_cnam
            if enable_internal_cnam:
                params["enable_internal_cnam"] = enable_internal_cnam
            if codecs:
                params["allowed_codecs"] = codecs
            if dtmf_mode:
                params["dtmf_mode"] = dtmf_mode
            
            data = self.get(mtd, params)
            data["subacc"] = subaccount
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