'''
In this example you will see how to call functions from the VoIP.ms API.

This could be used for any function that has not been added to this package.
'''

from voipms_api import VoipMsClient

func = "getMusicOnHold" # Function of the VoIP.ms API.

vms_client = VoipMsClient() # Client object.
response = vms_client.make_request(func) # Method to send a custom request to the API.

print(response)
