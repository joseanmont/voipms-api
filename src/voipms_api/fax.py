'''
VoIP.ms Virtual Fax functions
'''

import base64
from .voipms_client import VoipMsClient
from typing import Optional, Union


class Fax(VoipMsClient):
    '''
    A class to call the Virtual Fax functions of the VoIP.ms API.

    Methods:
        send_fax:
            Sends a Fax from a specific DID to a specific number.
    '''

    def send_fax(
            self,
            to_number: Union[str, int],
            from_name: str,
            from_number: Union[str, int],
            file_path:str,
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
            dict: Status of the request.
        """

        mtd = "sendFaxMessage"

        # Encode file in base64
        with open(file_path, "rb") as file:
            encoded_content = base64.b64encode(file.read()).decode("ascii")

        params = {
            "to_number": to_number,
            "from_name": from_name,
            "from_number": from_number,
            "file": encoded_content,
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

        data = self.post(mtd, params)
        data = dict(data)
        return data
