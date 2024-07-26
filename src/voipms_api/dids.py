'''
VoIP.ms DIDs functions
'''

import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class DIDs():
    '''
    A class to call the DID functions of the VoIP.ms API.

    Methods:
        cancel_did:
            Cancels a specific DID number and returns the result of the request.
        get_dids_info:
            Returns the current balance of the VoIP.ms account.
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

    
    def cancel_did(self, 
            did:Union[str, int],
            comment:Optional[str]=None,
            port_out:Optional[Union[str, bool]]=None,
            test:Optional[Union[str, bool]]=None
        ) -> dict:
        """
        Calls the VoIP.ms cancelDID function.

        Args:
            did (str or int, required): Specific DID number to be canceled (Example: 5551234567).
            comment (str, optional): Comment for DID cancellation.
            port out (str or bool, optional): Set True if the DID was ported out.
            test (str or bool, optional): Set True if testing the DID cancelation function.

        Returns:
            dict: A dictionary containing the status of the request and the DID that was canceled.
        """
        
        mtd = "cancelDID"

        try:
            params = {
                "did": did,
            }

            if comment:
                params["comment"] = comment
            if port_out:
                params["portout"] = port_out
            if test:
                params["test"] = test
            
            data = self.vms_client.make_request(mtd, params)
            data["result"] = "DID canceled"
            data["did"] = did
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None


    def get_dids_info(self, 
            client:Optional[Union[str, int]]=None, 
            did:Optional[Union[str, int]]=None
        ) -> dict:
        """
        Calls the VoIP.ms getDIDsInfo function.

        Args:
            client (str or int, optional): ID of a specific Reseller client or Sub Account (Example: 123456 or 100000_Account).
            did (str or int, optional): Specific DID number or Sub Account (Example: 5551234567).   

        Returns:
            dict:   If no parameter is provided, a dictionary containing the status and information from all the DIDs.
                    If a client ID is provided, a dictionary containing the status and information from the client's DIDs.
                    If a Sub Account is provided, a dictionary containing the status and information of the Sub Account's DID.
                    If a DID is provided, a dictionary containing the status and information of the specific DID.
        """
        
        mtd = "getDIDsInfo"

        try:
            params = {}

            if client:
                params["client"] = client
            if did:
                params["did"] = did
            
            data = self.vms_client.make_request(mtd, params)
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        
        
    def order_did(self,
        did: Union[str, int],
        routing: Optional[str]="sys:hangup",
        pop:Optional[Union[str, int]]=22,
        dial_time:Optional[Union[str, int]]=60,
        cnam:Optional[Union[str, int]]=0,
        billing_type: Optional[Union[str, int]]=1
        )-> dict:
        """
        Calls the VoIP.ms orderDID function.

        Args:
            did (str or int, required): Specific DID number to be ordered (Example: 5551234567).
            routing (str, optional): Routing of the DID. Default is sys:hangup.
            pop (str or int, optional): POP server of the DID. Default is 22 (sanjose1.voip.ms). Data from get_severs.
            dial time (str or int, optional): Ring time of the DID. Default is 60 (seconds).
            cnam: (str or int, optional): Activates CNAM lookup. Default is 0 (disabled). Set 1 for enable.
            billing type (str or int, optional): Sets the Billing plan. Default is 1 (Per Minute). Set 2 for Flat Rate.

        Returns:
            dict: A dictionary containing the status of the request and the DID that was ordered.
        """
        
        mtd = "orderDID"

        try:
            params = {
                "did": did,
                "routing": routing,
                "pop": pop,
                "dialtime": dial_time,
                "cnam": cnam,
                "billing_type": billing_type,
            }
            
            data = self.vms_client.make_request(mtd, params)
            data["result"] = "DID ordered"
            data["did"] = did
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        

    def order_toll_free(self,
        did: Union[str, int],
        routing: Optional[str]="sys:hangup",
        pop:Optional[Union[str, int]]=22,
        dial_time:Optional[Union[str, int]]=60,
        cnam:Optional[Union[str, int]]=0
        )-> dict:
        """
        Calls the VoIP.ms orderTollFree function.

        Args:
            did (str or int, required): Specific Toll-free DID number to be ordered (Example: 8771234567).
            routing (str, optional): Routing of the DID. Default is sys:hangup.
            pop (str or int, optional): POP server of the DID. Default is 22 (sanjose1.voip.ms). Data from get_severs.
            dial time (str or int, optional): Ring time of the DID. Default is 60 (seconds).
            cnam: (str or int, optional): Activates CNAM lookup. Default is 0 (disabled). Set 1 for enable.
            billing type (str or int, optional): Sets the Billing plan. Default is 1 (Per Minute). Set 2 for Flat Rate.

        Returns:
            dict: A dictionary containing the status of the request and the DID that was ordered.
        """
        
        mtd = "orderTollFree"

        try:
            params = {
                "did": did,
                "routing": routing,
                "pop": pop,
                "dialtime": dial_time,
                "cnam": cnam
            }
            
            data = self.vms_client.make_request(mtd, params)
            data["result"] = "DID ordered"
            data["did"] = did
            return data
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error ocurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None