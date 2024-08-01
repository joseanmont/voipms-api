'''
VoIP.ms LNP functions
'''

import requests
from datetime import datetime
from typing import Optional, Union


class LNP:
    '''
    A class to call the LNP functions of the VoIP.ms API.

    Methods:
        get_portability:
            Returns the result of verifying portability for a single number.
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

    def get_portability(
            self, 
            did:Union[str, int],
        ):
        """
        Calls the VoIP.ms getPortability function.

        Args:
            did (str or int, required): Specific DID number to be verified (Example: 5551234567).

        Returns:
            dict: A dictionary containing the DID and the result of the verification.
        """

        mtd = "getPortability"
        
        try:
            portability_result = {}    

            params = {
                "did": did
            }
            
            response = self.vms_client.make_request(mtd, params)
            portability_result["did"] = did
            portability_result["result"] = response

            return portability_result
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None