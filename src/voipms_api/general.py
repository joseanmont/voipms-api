'''
VoIP.ms General functions
'''

import requests
from datetime import datetime
from typing import Optional, Union

class General():
    '''
    A class to call the general functions of the VoIP.ms API.

    Methods:
        get_balance:
            Returns the current balance of the VoIP.ms account and call statistics.
        get_conference:
            Returns all the conferences if no ID is provided.
        get_conference_members:
            Returns the data of the conference members, or a specific conference member.
        get_conference_recordings:
            Returns the data of the recordings of the requested conference.
        get_conference_recording_file:
            Returns the file of a specific conference recording.
        get_sequences:
            Returns the data of the existing sequences, or a specific sequence.
        get_countries:
            Returns the list of available countries and their values, or a specific country and its values.
        get_ip:
            Returns the public IPv4 address of the network the request comes from.
        get_languages:
            Returns the list of available languages and their values, or a specific language and its values.
        get_locales:
            Returns the list of available Locale codes and their values, or a specific Locale code and its values.
        get_servers:
            Returns the list of available POP servers and their values, or a specific POP server and its values.
        get_transactions:
            Returns the transactions of a specific period.
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

    
    def get_balance(
            self, 
            advanced:Optional[bool]=False
        ) -> dict:
        """
        Calls the VoIP.ms getBalance function.

        Args:
            advanced (bool, optional): If True, also returns Balance and Calls Statistics of the Account. Default is False.

        Returns:
            dict: A dictionary containing the status and the current account balance.
        """
        
        mtd = "getBalance"

        try:
            if advanced:
                params = {
                     "advanced": True,
                }
                data = self.vms_client.make_request(mtd, params)
            else:
                 data = self.vms_client.make_request(mtd)
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


    def get_conference(
            self, 
            id:Optional[Union[str, int]]=None
        ) -> dict:
        """
        Calls the VoIP.ms getConference function.

        Args:
            id (str or int, optional): ID of a specific conference.

        Returns:
            dict: A dictionary containing the status and the data of the existing conferences, or a specific conference if a conference ID is provided.
        """

        mtd = "getConference"

        try:
            params = {}
            if id:
                params["conference"] = id

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


    def get_conference_members(
            self, 
            member:Optional[Union[str, int]]=None
        ) -> dict:
        """
        Calls the VoIP.ms getConferenceMembers function.

        Args:
            member (str or int, optional): ID of a specific conference member.

        Returns:
            dict: A dictionary containing the status and the data of the conference members, or a specific conference member if a member ID is provided.
        """

        mtd = "getConferenceMembers"

        try:
            params = {}
            
            if member:
                params["member"] = member

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
        

    def get_conference_recordings(
            self, 
            id:Union[int, str], 
            date_from:Optional[str]=None, 
            date_to:Optional[str]=None
        ) -> dict :
        """
        Calls the VoIP.ms getConferenceRecordings function.

        Args:
            id (str or int, required): ID of the conference to retrieve the recordings from.
            from date (str, optional): Start date to search recordings. (Example: '2016-06-03').
            to date (str, optional): End date to search recordings. (Example: '2016-07-03').

        Returns:
            dict: A dictionary containing the status and the data of the recordings of the requested conference.
        """

        mtd = "getConferenceRecordings"

        try:
            params = {
                "conference": id
            }
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
        

    def get_conference_recording_file(
            self, 
            id:Union[int, str], 
            recording:Union[int, str]
        ) -> dict:
        """
        Calls the VoIP.ms getConferenceRecordingFile function.

        Args:
            id (str or int, required): ID of the conference to retrieve the recording from.
            recording (str or int, required): ID of the recording to retrieve the file for.            

        Returns:
            dict: A dictionary containing the status and the requested recording file.
        """

        mtd = "getConferenceRecordingFile"

        try:
            params = {
                "conference": id,
                "recording": recording,
            }

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


    def get_sequences(
            self, 
            sequence: Optional[Union[str, int]]=None, 
            client:Optional[Union[str, int]]=None
        ) -> dict:
            # Possible bug from the VoIP.ms API here: Does not return secuences associated with a Reseller client when no Secuence nor Client ID is provided.
            """
            Calls the VoIP.ms getSequences function.

            Args:
                id (str or int, optional): ID of a specific Sequence.
                client (str or int, optional): ID of a specific Reseller client.            

            Returns:
                dict: A dictionary containing the status and the data of the existing sequences, or a specific sequence if a sequence ID is provided.
            """

            mtd = "getSequences"

            try:
                params = {}

                if sequence:
                    params["sequence"] = sequence
                if client:
                    params["client"] = client

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
            

    def get_countries(
            self, 
            country:Optional[str]=None
        ) -> dict:
                """
                Calls the VoIP.ms getCountries function.

                Args:
                    country (str, optional): ID code of a specific Country (Example: 'CA').

                Returns:
                    dict: A dictionary containing the status and the list of available countries and their values, or a specific country if a country ID code is provided.
                """

                mtd = "getCountries"

                try:
                    params = {}

                    if country:
                        params["country"] = country
                    
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
                

    def get_ip(self):
                """
                Calls the VoIP.ms getIP function.

                Returns:
                    dict: A dictionary containing the status and the public IPv4 address of the network the request comes from.
                """

                mtd = "getIP"

                try:
                    data = self.vms_client.make_request(mtd)
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
                
    
    def get_languages(
            self, 
            language:Optional[str]=None
        ) -> dict:
                """
                Calls the VoIP.ms getLanguages function.

                Args:
                    language (str, optional): ID code of a specific Language (Example: 'en').

                Returns:
                    dict: A dictionary containing the status and the list of available languages and their values, or a specific language if a language ID code is provided.
                """

                mtd = "getLanguages"

                try:
                    params = {}

                    if language:
                        params["language"] = language
                    
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


    def get_locales(
            self, 
            locales:Optional[str]=None
        ) -> dict:
                """
                Calls the VoIP.ms getLocales function.

                Args:
                    locale (str, optional): ID code of a specific Locale code (Example: 'en-US').

                Returns:
                    dict: A dictionary containing the status and the list of available Locale codes and their values, or a specific Locale code if a Locale code is provided.
                """

                mtd = "getLocales"

                try:
                    params = {}

                    if locales:
                        params["locale"] = locales

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
                
    
    def get_servers(
            self, 
            server:Optional[Union[int, str]]=None
        ) -> dict:
                """
                Calls the VoIP.ms getServersInfo function.

                Args:
                    server (str, optional): ID of a specific POP server (Example: 65).

                Returns:
                    dict: A dictionary containing the status and the list of available POP servers and their values, or a specific POP server if a server ID code is provided.
                """

                mtd = "getServersInfo"

                try:
                    params = {}

                    if server:
                        params["server_pop"] = server

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
            dict: A dictionary containing the status and the data of the transactions of the requested period.
        """

        mtd = "getTransactionHistory"

        try:
            df = datetime.strptime(date_from, '%Y-%m-%d')
            dt = datetime.strptime(date_to, '%Y-%m-%d')
            if df <= dt:
                params = {
                    "date_from": date_from,
                    "date_to": date_to
                }
            else:
                raise TypeError("The TO date cannot be prior the FROM date")
            
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