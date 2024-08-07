# voipms-api

This package is developed to streamline the process of integrating with the VoIP.ms API, allowing developers to focus on implementing functionality without the need to write boilerplate code for API connectivity and function calls. The VoIP.ms API Client encapsulates all necessary code to connect and interact with the VoIP.ms API, enabling developers to call functions directly.

## Features

- **Simplified Integration**: Connect to the VoIP.ms API with minimal setup.
- **Modular Design**: Organized into separate modules for different functionalities, allowing targeted imports and reduced overhead.
- **Ongoing Development**: New functions will continue to be added.

## Updates

- **1.1.3b11:
    - Fixed bug on 'create_call_hunting' and 'update_call_hunting' that did not allow adding multiple members.
- **1.1.2b11:
    - Accounts
        - Method updated: 'create_sub_account'
            - arg 'password' set as optional so Sub Accounts can be created using IP authentication.
            - added optional arg 'ip' for sub accounts created with 'auth_type' IP authentication.
            - added optional arg 'codecs' to specify the codec the sub account will use.
 	        - added optional arg 'lock_international' to enable/disable Interntional calls.
 	        - added optional arg 'callerid_number' to set a caller ID number for the sub account.
        - Added method 'update_subaccounts'
    - CallHunting
        - Added method 'update_call_hunting'
    - Forwarding
        - Added method 'update_forwarding'
    - General
        - Bug fixed on 'get_transactions' that did not allow get records from one single day. 
    - IVR
        - Added method 'update_ivr'
    - RingGroup
        - Method updated: 'create_ring_group'
            - added optional arg 'announcement' to set an announcement recording.
            - added optional arg 'music_on_hold' to set music on hold.
            - added optional arg 'language' to set the language.
        - Added method 'update_ring_group'
    - SMS
        - Added method 'get_sms'
    - Voicemail
        - Added method 'update_voicemail'

- **1.0.2b11: The method create_sub_account now accepts description as an optional argument.
- **1.0.1b11: Fixed bug that causes importing errors when using the module Voicemail.
- **1.0.0b11: All modules were refactored to improve imports.

## Installation

The package is now available at PyPi and can be installed in your virtual environment running this command:

```
pip install voipms-api
```

You can also clone the repository in your project from [Github](https://github.com/joseanmont/voipms-api).

**Note:** If you clone it and have problems importing the modules, add the path to the directory and subdirectories in PYTHONPATH.

## Package structure

```plaintext
voipms-api
├── src/
│   └── voipms_api/
│       ├── __init__.py
│       ├── accounts.py
│       ├── call_hunting.py
│       ├── dids.py
│       ├── forwarding.py
│       ├── general.py
│       ├── ivr.py
│       ├── lnp.py
│       ├── ring_groups.py
│       ├── sms.py
│       ├── voicemail.py
│       └── voipms_client.py
│── tests/
│   └── test_voipms_client.py
```

## Usage

The credentials can be loaded on your virtual enviroment by adding the following variables on an .env file:

```.env
VOIPMS_API_USER = "Your VoIP.ms account email"
VOIPMS_API_PASSWORD = "Your VoIP.ms API password"
```

After this, you can start importing the classes and use their functions. Here is an example:

```
from voipms_api import DIDs

dids = DIDs()
print(dids.get_dids_info())
```

Or, you can add the credentials when calling a single instance. For example:

```
from voipms_api import General

balance = General(username="me@email.com", password="api_password")
print(balance.get_balance())
```

Additionally, you can add your credentials or use different credentials by using the class VoipMsClient.

This class also allows you use the method "make_request" to call a VoIP.ms function that might not be available in this package yet.

Here is an example:

```
from voipms_api import VoipMsClient

vms_client = VoipMsClient(username="me@email.com", password="your VoIP.ms API password")
vms_client.make_request("sendFax")
```

## Module Capabilities

Currently, the modules of accounts and voice features within the voipms-api package provide basic functionalities for creating, retrieving, and deleting items. 

You will find the current available functions in the description of each class.

Additional functionalities will be added over time.

## Examples of scripts

You can find more examples of scripts in the examples directory in the [Github](https://github.com/joseanmont/voipms-api) repository. These scripts demonstrate how to use the some features of the voipms-api package.

## Contributing

Currently, we are not accepting collaborations. However, if you have suggestions or feedback, feel free to contact us. Issues can be reported on GitHub.

## License

This package is free to use and can be included in any project. See the LICENSE file for more details.

## Support

For any issues or questions, please raise an issue on GitHub or contact us directly at hello@joseanmont.info

## Special Thanks

Kudos to the VoIP.ms development team. They have developed an understandable, simple but still powerful API that lets users take their VoIP system beyond limits.