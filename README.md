# voipms-api

This package is developed to streamline the process of integrating with the VoIP.ms API, allowing developers to focus on implementing functionality without the need to write boilerplate code for API connectivity and function calls. The VoIP.ms API Client encapsulates all necessary code to connect and interact with the VoIP.ms API, enabling developers to call functions directly.

## Features

- **Simplified Integration**: Connect to the VoIP.ms API with minimal setup.
- **Modular Design**: Organized into separate modules for different functionalities, allowing targeted imports and reduced overhead.
- **Ongoing Development**: New functions will continue to be added.

## Installation

Add the package to your project to be able to import its modules, classes and methods.

Check requirements.txt to see the packages that need to be installed.

## Package structure

```plaintext
voipms-api
├── src/
│   └── voipms-api/
│       ├── __init__.py
│       ├── voipms_client.py
│       ├── dids.py
│       ├── general.py
│       ├── lnp.py
│       ├── sms.py
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

However, you can also add your credentials or add custom credentials by using the class VoipMsClient from the module "voipms_client". Here is an example:

```
voipms-client = VoipMsClient(username="me@email.com", password="your VoIP.ms API password")
```

Or, you can do it when calling a single instance. For example:

```
from voipms_api import General
balance = General(username="me@email.com", password="api_password")
```

## Examples of scripts

You can find more example scripts in the examples directory. These scripts demonstrate how to use the some features of the voipms_api package.

## Contributing

Currently, we are not accepting collaborations. However, if you have suggestions or feedback, feel free to contact us. Issues can be reported on GitHub.

## License

This package is free to use and can be included in any project. See the LICENSE file for more details.

## Support

For any issues or questions, please raise an issue on GitHub or contact us directly at hello@joseanmont.info

## Special Thanks

Kudos to the VoIP.ms development team. They have a developed an understandable, simple but still powerful API that lets users take their VoIP system beyond limit.