import requests
from typing import Optional, Union


class Fax():
    '''
    A class to call the Virtual Fax functions of the VoIP.ms API.

    Methods:
        send_fax:
            Sends a Fax from a specific DID to a specific number.
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

    def send_fax(
            self,
            to_number: Union[str, int],
            from_name: str,
            from_number: Union[str, int],
            file:str,
            send_email_enabled: Optional[Union[str, int]] = None,
            send_email: Optional[str] = None,
            station_id:str = None,
            test:Optional[Union[str, int]] = None
        ) -> dict:
        """
        Calls the VoIP.ms sendFaxMessage function. 
        Sends a fax from a specific DID to a specific number.

        Args:
            to_number (str or int): The number to send the fax to.
            from_name (str): The name of the sender.
            from_number (str or int): DID number of the sender.
            file (str): The file path of the fax to be sent.
            send_email_enabled (str or int, optional): Values: 1 = true, 0 = false
            send_email (str, optional): Email address where you want send a copy of your Fax.
            station_id (str, optional): To identify a equipment or department sending the Fax.
            test (str or int, optional): Set to true if testing how to send a Fax Message.
        Returns:
            dict: A dictionary containing the status of the request.
        """

        mtd = "sendFaxMessage"

        try:
            params = {
                "to_number": to_number,
                "from_name": from_name,
                "from_number": from_number,
                "file": file,
            }

            # Optional in this package.
            if send_email_enabled:
                params["send_email_enabled"] = send_email_enabled
            if send_email:
                params["send_email"] = send_email
            if station_id:
                params["station_id"] = station_id
            if test:
                params["test"] = test

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