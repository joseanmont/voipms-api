import requests
from typing import Optional, Union


class Accounts():
    '''
    A class to call the Sub Accounts functions of the VoIP.ms API.

    Methods:
        create_subaccount:
            Creates a Sub Account and returns the result of the request.
        delete_subaccount:
            Deletes a specific Sub Account and returns the result of the request.
        get_subaccounts:
            Returns all the Sub Accounts or a specific Sub Account if an ID is provided.
        update_subaccount:
            Updates the configuration of a Sub Account and returns the result of the request.
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

    
    def create_subaccount(self, 
            username:str,
            auth_type:Optional[Union[str, int]]=1,
            password:Optional[str]=None,
            ip:Optional[str]=None,
            protocol:Optional[Union[str, int]]=1,
            device_type:Optional[Union[str, int]]=2,
            callerid_number:Optional[Union[str, int]]=None,
            internal_extension:Optional[Union[str, int]]=None,
            internal_voicemail:Optional[Union[str, int]]=None,
            internal_cnam:Optional[str]=None,
            enable_internal_cnam:Optional[Union[str, int]]=0,
            description:Optional[str]=None,
            lock_international:Optional[Union[str, int]]=1,
            codecs:Optional[str]="g722"
        ) -> dict:
        """
        Calls the VoIP.ms createSubAccount function.

        Args:
            username (str, required): Username to set to the sub account (Example: 'VoIP').
            auth_type (str or int, optional): The authentication type the sub account will use. Default is '1' for User/Password (value from get_auth_types).
            password (str, optional): Password to set for password authentication.
            ip (str, optional): IP address or Fully Qualified Domain Name for IP authentication.
            protocol (str or int, optional): The protocol the sub account will use. Default is '1' for SIP (value from get_Protocols).
            device_type (str or int, optional): Device type that will be used. Default is '2' for ATA device, IP Phone or Softphone (value from get_device_types).
            callerid_number (str or int, optional): Caller ID number of the sub account (Example: 4052550000).
            extension (str or int, optional): Sub Account Internal Extension (Example: 1 -> Creates 101).
            internal_extension (str or int, optional): Sub Account Internal Extension (Example: 1 -> Creates 101).
            internal_voicemail (str or int, optional): ID of a voicemail to set as the Sub Account Internal Voicemail (Example: 101).
            internal_cnam (str, optional): Caller ID name for internal calls.
            enable_internal_cnam (str, optional): Enables/Disables the internal caller ID name for internal calls. Default is '0' for disabled (send '1' to enable it).
            description (str, optional): A description or name for the Sub Account.
            lock_international (str or int, optional): Enables/Disables International calls. Default is '1' for disabled. (values from get_lock_international).
            codecs (str, optional): Audio codecs for calls. Default is 'g722' (values from get_allowed_codecs).

        Returns:
            dict: A dictionary containing the status of the request and the Sub Account that was created.

        Raises:
                ValueError: If auth_type is 1 and password is not provided.
                            If auth_type is 2 and ip is not provided.
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
            print(f'An error occurred: {err}')
            return None
        

    def get_subaccounts(self, 
            subaccount:Optional[Union[str, int]]=None
        ) -> dict:
        """
        Calls the VoIP.ms getSubAccounts function.

        Args:
            subaccount (str or int, optional): Sub Account ID or username (Example: '100000_SubAccount' or 99785).

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
            print(f'An error occurred: {err}')
            return None
        

    def update_subaccount(self, 
            subaccount:Union[str, int],
            auth_type:Optional[Union[str, int]]=None,
            password:Optional[str]=None,
            ip:Optional[str]=None,
            protocol:Optional[Union[str, int]]=None,
            device_type:Optional[Union[str, int]]=None,
            callerid_number:Optional[Union[str, int]]=None,
            internal_extension:Optional[Union[str, int]]=None,
            internal_voicemail:Optional[Union[str, int]]=None,
            internal_cnam:Optional[str]=None,
            enable_internal_cnam:Optional[str]=None,
            description:Optional[str]=None,
            canada_route:Optional[Union[str, int]]=None,
            lock_international:Optional[Union[str, int]]=None,
            international_route:Optional[Union[str, int]]=None,
            record_calls:Optional[Union[str, int]]=None,
            music_on_hold:Optional[str]=None,
            codecs:Optional[str]=None,
            dtmf_mode:Optional[str]=None
        ) -> dict:
        """
        Calls the VoIP.ms setSubAccount function.

        Args:
            subaccount (str, required): Full mame of the sub account that will be updated (Example: '100000_SubAccount').
            auth_type (str or int, optional): The authentication type the sub account will use (value from get_auth_types).
            password (str, optional): Password to set for password authentication.
            ip (str, optional): IP address or Fully Qualified Domain Name for IP authentication.
            protocol (str or int, optional): The protocol the sub account will use. (value from get_Protocols).
            device_type (str or int, optional): Device type that will be used (value from get_device_types).
            callerid_number (str or int, optional): Caller ID number of the sub account.
            internal_extension (str or int, optional): Sub Account Internal Extension (Example: 1 -> Creates 101).
            internal_voicemail (str or int, optional): ID of a voicemail to set as the Sub Account Internal Voicemail (Example: 101).
            internal_cnam (str, optional): Caller ID name for internal calls.
            enable_internal_cnam (str, optional): Enables/Disables the internal caller ID name for internal calls (values '0' for disabled,'1' for enabled).
            description (str, optional): Description or name of the Sub Account.
            canada_route (str or int, optional): Defines the route for calls to Canada (values from get_routes).
            lock_international (str or int, optional): Enables/Disables International calls (values from get_lock_international).
            international_route (str or int, optional): Defines the route for International calls (values from get_routes).
            music_on_hold (str, optional): Music on hold for the sub account (values from get_music_on_hold).
            record_calls (str or int, optional): Enables/Disables call recording (values 1/0).
            codecs (str, optional): Audio codecs for calls (values from get_allowed_codecs).
            dtmf_mode (str, optional): DTMF mode for the sub account (values from get_dtmf_modes).

        Returns:
            dict: A dictionary containing the status of the request.

        Raises:
                ValueError: If auth_type is 1 and password is not provided.
                            If auth_type is 2 and ip is not provided.
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
            
            data = self.vms_client.make_request(mtd, params)
            data["subacc"] = subaccount
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