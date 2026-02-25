"""VoIP.ms SMS/MMS functions."""

import requests
from voipms_client import VoipMsClient
from datetime import datetime
from typing import Optional, Union


class SMS(VoipMsClient):
    """
    SMS/MMS operations for the VoIP.ms API.

    Methods:
        get_sms(id, date_from, date_to, ...): List or filter SMS messages.
        send_sms(did, dst, message): Send an SMS from a DID to a number.
    """

    def get_sms(
        self,
        id: Optional[Union[str, int]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        type: Optional[Union[str, int]] = None,
        did: Optional[Union[str, int]] = None,
        contact: Optional[Union[str, int]] = None,
        limit: Optional[Union[str, int]] = None,
        timezone: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        Get or filter SMS messages (VoIP.ms getSMS).

        Args:
            id: Optional ID of a specific SMS message.
            date_from: Start date for range (e.g. '2016-06-03'). Use with date_to.
            date_to: End date for range (e.g. '2016-07-03').
            type: Filter by direction: '0' = sent, '1' = received.
            did: Filter by DID (e.g. 2052550000).
            contact: Filter by contact number (e.g. 4042550000).
            limit: Max records to return (default 50). e.g. 20.
            timezone: Timezone offset for message times (-12 to 13).

        Returns:
            API response with requested messages.
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

    def send_sms(
        self,
        did: Union[str, int],
        dst: Union[str, int],
        message: str,
    ) -> dict:
        """
        Send an SMS from a DID to a destination number (VoIP.ms sendSMS).

        Args:
            did: DID to send from.
            dst: Destination phone number.
            message: Message body.

        Returns:
            API response with status.
        """
        
        mtd = "sendSMS"

        try:
            params = {
                "did": did,
                "dst": dst,
                "message": message
            }
            data = self.get(mtd, params)
            data = dict(data)
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