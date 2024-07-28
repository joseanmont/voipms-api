import requests
from voipms_client import VoipMsClient
from typing import Optional, Union
from accounts import Accounts


class RingGroups():
    '''
    A class to call the Ring Groups functions of the VoIP.ms API.

    Methods:
        create_ring_group:
            Creates a new Ring Group and returns the result of the request.
        delete_ring_group:
            Deletes a specific Ring Group and returns the result of the request.
        get_ring_groups:
            Returns all the existing Ring Groups, or a specific Ring Group if a Ring Group ID is provided.
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


    def create_ring_group(self, 
            name:str,
            voicemail:Union[str, int],
            members:Optional[str]=None,
        ) -> dict:
        """
        Calls the VoIP.ms setRingGroup function to create a new Ring Group.

        Args:
            name (str, required): A name for the new Ring Group.
            voicemail (str or int, required): ID of the Voicemail to assign. Value from get_voicemails.
            members (srt, optional): A string of members separated by semicolons. Default is Main Account as only member. (Example: 'account:100001;fwd:16006'). See VoIP.ms API documentation for more details.

        Returns:
            dict: A dictionary containing the status of the request and the name of the Ring Group that was created.
        """
        
        mtd = "setRingGroup"
        main_account = "account:" + self.acc_number

        try:
            params = {
                # Required by this package
                "name": name,
                "voicemail": voicemail,

                # Required by VoIP.ms API
                "members": main_account,
            }

            # Optional in this package.
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
        

    def delete_ring_group(self, 
            ring_group:Union[str, int],
        ) -> dict:
        """
        Calls the VoIP.ms delRingGroup function.

        Args:
            ring_group (str or int, required): ID of the ring group that will be deleted (Example: 18635). Value from get_ring_groups.

        Returns:
            dict: A dictionary containing the status of the request and the ID of the ring group that was deleted.
        """
        
        mtd = "delRingGroup"

        try:
            params = {
                "ringgroup": ring_group,
            }

            # Code to get the name of the ring group that is deleted.
            rg_info = self.get_ring_groups(ring_group)
            rg_name = rg_info["ring_groups"][0]["name"]

            data = self.vms_client.make_request(mtd, params)
            data["ring_group"] = rg_name
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
        

    def get_ring_groups(self, 
            ring_group:Optional[Union[str, int]]=None,
        ) -> dict:
        """
        Calls the VoIP.ms getRingGroups function.

        Args:
            ring_group (str or int, optional): ID of a specific ring group (Example: 18635).

        Returns:
            dict: A dictionary containing the status of the request and the data of all the ring groups, or the data of a specific ring group if an ID is provided.
        """
        
        mtd = "getRingGroups"

        try:
            params = {}

            # Optional in this package.
            if ring_group:
                params["ring_group"] = ring_group
            
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