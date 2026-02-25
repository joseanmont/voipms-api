"""VoIP.ms general/utility API functions."""

import requests
from voipms_client import VoipMsClient
from datetime import datetime
from typing import Optional, Union


class General(VoipMsClient):
    """
    General and utility operations for the VoIP.ms API.

    Methods:
        get_balance(advanced): Get account balance and optional call statistics.
        get_conference(id): List conferences or get one by ID.
        get_conference_members(member): List conference members or get one by ID.
        get_conference_recordings(id, date_from, date_to): Get conference recordings.
        get_conference_recording_file(id, recording): Get a conference recording file.
        get_sequences(sequence, client): List sequences or get one by ID.
        get_countries(country): List countries or get one by code.
        get_ip(): Get the public IPv4 address seen by the API.
        get_languages(language): List languages or get one by code.
        get_locales(locales): List locale codes or get one by code.
        get_servers(server): List POP servers or get one by ID.
        get_transactions(date_from, date_to): Get transaction history for a date range.
    """

    def get_balance(self, advanced: Optional[bool] = False) -> dict:
        """
        Get account balance (VoIP.ms getBalance).

        Args:
            advanced: If True, include balance and call statistics. Default False.

        Returns:
            API response with current balance (and optionally statistics).
        """
        mtd = "getBalance"

        try:
            if advanced:
                params = {"advanced": True}
                data = self.get(mtd, params)
            else:
                data = self.get(mtd)
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

    def get_conference(self, id: Optional[Union[str, int]] = None) -> dict:
        """
        List conferences or get one by ID (VoIP.ms getConference).

        Args:
            id: Optional conference ID. If omitted, all conferences are returned.

        Returns:
            API response with conference(s) data.
        """
        mtd = "getConference"

        try:
            params = {}
            if id:
                params["conference"] = id

            data = self.get(mtd, params)
            return data

        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except KeyError as key_err:
            return f"Key error: {key_err}"
        except Exception as err:
            return f'An error occurred: {err}'


    def get_conference_members(
        self, member: Optional[Union[str, int]] = None
    ) -> dict:
        """
        List conference members or get one by ID (VoIP.ms getConferenceMembers).

        Args:
            member: Optional conference member ID. If omitted, all members are returned.

        Returns:
            API response with conference member(s) data.
        """
        mtd = "getConferenceMembers"

        try:
            params = {}
            if member:
                params["member"] = member

            data = self.get(mtd, params)
            return data

        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except KeyError as key_err:
            return f"Key error: {key_err}"
        except Exception as err:
            return f'An error occurred: {err}'

    def get_conference_recordings(
        self,
        id: Union[int, str],
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> dict:
        """
        Get recordings for a conference (VoIP.ms getConferenceRecordings).

        Args:
            id: Conference ID.
            date_from: Start date for range (e.g. '2016-06-03'). Required with date_to.
            date_to: End date for range (e.g. '2016-07-03'). Must be >= date_from.

        Returns:
            API response with conference recordings.

        Raises:
            TypeError: If only one of date_from/date_to is provided, or if date_to is before date_from.
        """
        mtd = "getConferenceRecordings"

        try:
            params = {"conference": id}
            if date_from and not date_to:
                raise TypeError("Missing parameter. Send conference ID, From date and To date.")
            if date_from or date_to:
                df = datetime.strptime(date_from, '%Y-%m-%d')
                dt = datetime.strptime(date_to, '%Y-%m-%d')
                if df <= dt:
                    params["date_from"] = date_from
                    params["date_to"] = date_to
                else:
                    raise TypeError("The TO date cannot be prior the FROM date")

            data = self.get(mtd, params)
            return data

        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except KeyError as key_err:
            return f"Key error: {key_err}"
        except Exception as err:
            return f'An error occurred: {err}'

    def get_conference_recording_file(
        self, id: Union[int, str], recording: Union[int, str]
    ) -> dict:
        """
        Get a specific conference recording file (VoIP.ms getConferenceRecordingFile).

        Args:
            id: Conference ID.
            recording: Recording ID within that conference.

        Returns:
            API response with the recording file data.
        """
        mtd = "getConferenceRecordingFile"

        try:
            params = {
                "conference": id,
                "recording": recording,
            }

            data = self.get(mtd, params)
            return data

        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except KeyError as key_err:
            return f"Key error: {key_err}"
        except Exception as err:
            return f'An error occurred: {err}'


    def get_sequences(
        self,
        sequence: Optional[Union[str, int]] = None,
        client: Optional[Union[str, int]] = None,
    ) -> dict:
        """
        List sequences or get one by ID (VoIP.ms getSequences).

        Note: API may not return sequences for a reseller client when neither
        sequence nor client ID is provided.

        Args:
            sequence: Optional sequence ID.
            client: Optional reseller client ID.

        Returns:
            API response with sequence(s) data.
        """
        mtd = "getSequences"

        try:
            params = {}
            if sequence:
                params["sequence"] = sequence
            if client:
                params["client"] = client

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

    def get_countries(self, country: Optional[str] = None) -> dict:
        """
        List countries or get one by code (VoIP.ms getCountries).

        Args:
            country: Optional country code (e.g. 'CA'). If omitted, all countries are returned.

        Returns:
            API response with country/countries data.
        """
        mtd = "getCountries"

        try:
            params = {}
            if country:
                params["country"] = country

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

    def get_ip(self) -> dict:
        """
        Get the public IPv4 address seen by the API (VoIP.ms getIP).

        Returns:
            API response with the requesting network's public IP.
        """
        mtd = "getIP"

        try:
            data = self.get(mtd)
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
                
    
    def get_languages(
            self, 
            language:Optional[str]=None
        ) -> dict:
                """
                Calls the VoIP.ms getLanguages function.

                Args:
                    language (str, optional): ID code of a specific Language (Example: 'en').

                Returns:
                    dict: The list of available languages and their values, or a specific language if a language ID code is provided.
                """

                mtd = "getLanguages"

                try:
                    params = {}

                    if language:
                        params["language"] = language
                    
                    data = self.get(mtd, params)
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


    def get_locales(
            self, 
            locales:Optional[str]=None
        ) -> dict:
                """
                Calls the VoIP.ms getLocales function.

                Args:
                    locale (str, optional): ID code of a specific Locale code (Example: 'en-US').

                Returns:
                    dict: The list of available Locale codes and their values, or a specific Locale code if a Locale code is provided.
                """

                mtd = "getLocales"

                try:
                    params = {}

                    if locales:
                        params["locale"] = locales

                    data = self.get(mtd, params)
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
                
    
    def get_servers(
            self, 
            server:Optional[Union[int, str]]=None
        ) -> dict:
                """
                Calls the VoIP.ms getServersInfo function.

                Args:
                    server (str, optional): ID of a specific POP server (Example: 65).

                Returns:
                    dict: The list of available POP servers and their values, or a specific POP server if a server ID code is provided.
                """

                mtd = "getServersInfo"

                try:
                    params = {}

                    if server:
                        params["server_pop"] = server

                    data = self.get(mtd, params)
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
                

    def get_transactions(
            self, 
            date_from:str, 
            date_to:str
        ) -> dict :
        """
        Calls the VoIP.ms getTransactionHistory function.

        Args:
            from date (str, required): start date to retrieve transactions. (Example: '2016-06-03').
            to date (str, required): end date to search transactions. (Example: '2016-07-03').

        Returns:
            dict: The data of the transactions of the requested period.
        """

        mtd = "getTransactionHistory"

        try:
            df = datetime.strptime(date_from, '%Y-%m-%d')
            dt = datetime.strptime(date_to, '%Y-%m-%d')
            if df > dt:
                raise ValueError("The TO date cannot be prior the FROM date")
            
            params = {
                    "date_from": date_from,
                    "date_to": date_to
                }
            
            data = self.get(mtd, params)
            return data
                    
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error ocurred: {http_err}"
        except KeyError as key_err:
            return f"Key error: {key_err}"
        except Exception as err:
            return f'An error ocurred: {err}'