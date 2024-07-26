'''
VoIP.ms SMS/MMS functions
'''

import requests
from datetime import datetime
from voipms_client import VoipMsClient
from typing import Optional, Union

class SMS():
    '''
    A class to call the SMS functions of the VoIP.ms API.

    Methods:
        send_sms:
            Sends a SMS message from a specific DID to a specific number.
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
    
    def send_sms(self, 
            did: Union[str, int], 
            dst:Union[str, int],
            message:str
        ) -> dict:
        """
        Calls the VoIP.ms sendSMS function.

        Args:
            did (str or int, required): DID the SMS will be send from.
            dst (str or int, required): Phone number that will receive the SMS message.
            message (str, required): The content of the message   

        Returns:
            dict: A dictionary containing the status of the request.
        """
        
        mtd = "sendSMS"

        try:
            params = {
                "did": did,
                "dst": dst,
                "message": message
            }
            data = self.vms_client.make_request(mtd, params)
            data = dict(data)
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