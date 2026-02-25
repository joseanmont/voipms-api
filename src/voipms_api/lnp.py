"""VoIP.ms LNP (number portability) functions."""

import requests
from voipms_client import VoipMsClient
from typing import Optional, Union


class LNP(VoipMsClient):
    """
    LNP (local number portability) operations for the VoIP.ms API.

    Methods:
        get_portability(did): Check portability for a single DID.
    """

    def get_portability(self, did: Union[str, int]) -> dict:
        """
        Check whether a DID is portable (VoIP.ms getPortability).

        Args:
            did: DID number to verify (e.g. 5551234567).

        Returns:
            Dict with 'did' and 'result' (API response for the portability check).
        """

        mtd = "getPortability"
        
        try:
            portability_result = {}    

            params = {
                "did": did
            }
            
            response = self.get(mtd, params)
            portability_result["did"] = did
            portability_result["result"] = response

            return portability_result
            
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return None
        except KeyError as key_err:
            print(f"Key error: {key_err}")
            return None
        except Exception as err:
            print(f'An error occurred: {err}')
            return None