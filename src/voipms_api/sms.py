'''
VoIP.ms SMS/MMS functions
'''

import requests
from datetime import datetime
from typing import Optional, Union

class SMS():
    '''
    A class to call the SMS functions of the VoIP.ms API.

    Methods:
        send_sms:
            Sends a SMS message from a specific DID to a specific number.
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
    

    def get_sms(
            self,
            id:Optional[Union[str, int]]=None,
            date_from:Optional[str]=None, 
            date_to:Optional[str]=None,
            type:Optional[Union[str, int]]=None,
            did:Optional[Union[str, int]]=None,
            contact:Optional[Union[str, int]]=None,
            limit:Optional[Union[str, int]]=None,
            timezone:Optional[Union[str, int]]=None,
        ) -> dict :
        """
        Calls the VoIP.ms getSMS function.

        Args:
            id (str or int, optional): ID of a specific SMS message.
            from date (str, optional): start date to retrieve transactions. (Example: '2016-06-03').
            to date (str, optional): end date to search transactions. (Example: '2016-07-03').
            type (str or int, optional): Filters the messages by type ('0' for sent | '1' for received).
            did (str or int, optional): Filters the messages of a specific DID number (Example: 2052550000).
            contact (str or int, optional): Filters the messages of a specific contact phone number (Example: 4042550000).
            limit (str or int, optional): Number of records to display (Example: 20 | Default is 50).
            timezone (str or int, optional): Adjust time of the messages according to Timezome (values from -12 to 13).

        Returns:
            dict: A dictionary containing the status and the data of the requested messages.
        """

        mtd = "getSMS"

        try:    
            params = {
                    "sms": id
                }
            
            if (date_from and not date_to) or (date_from and not date_to):
                raise ValueError("A date is missing")
            elif date_from and date_to:
                df = datetime.strptime(date_from, '%Y-%m-%d')
                dt = datetime.strptime(date_to, '%Y-%m-%d')

                if df > dt:
                    raise ValueError("The TO date cannot be prior the FROM date")
                
                params.update({
                    'from': date_from,
                    'to': date_to,
                })
            
            if type is not None:
                params["type"] =  type
            if did is not None:
                params["did"] =  did
            if contact is not None:
                params["contact"] =  contact
            if limit is not None:
                params["limit"] =  limit
            if timezone is not None:
                params["timezone"] =  timezone

            data = self.vms_client.make_request(mtd, params)
            return data
                    
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error ocurred: {err}')
            return None


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