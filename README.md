# voipms-api

This package is developed to streamline the process of integrating with the VoIP.ms API, allowing developers to focus on implementing functionality without the need to write boilerplate code for API connectivity and function calls. The VoIP.ms API Client encapsulates all necessary code to connect and interact with the VoIP.ms API, enabling developers to call functions directly.

## Features

- **Simplified Integration**: Connect to the VoIP.ms API with minimal setup.
- **Modular Design**: Organized into separate modules for different functionalities, allowing targeted imports and reduced overhead.
- **Ongoing Development**: New functions will continue to be added.

## Changelog

See [CHANGELOG.md](https://github.com/joseanmont/voipms-api/blob/main/CHANGELOG.md) for the release history.

## Installation

The package is now available at PyPi and can be installed in your virtual environment running this command:

```
pip install voipms-api
```

Requires Python 3.11 or newer.

## Package structure

```plaintext
voipms-api
├── src/
│   └── voipms_api/
│       ├── __init__.py
│       ├── accounts.py
│       ├── call_hunting.py
│       ├── dids.py
│       ├── fax.py
│       ├── forwarding.py
│       ├── general.py
│       ├── ivr.py
│       ├── lnp.py
│       ├── ring_groups.py
│       ├── sms.py
│       ├── voicemail.py
│       └── voipms_client.py
└── tests/
    ├── conftest.py
    ├── test_modules.py
    └── test_voipms_client.py
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

This class also allows you to use the methods "get" and "post" to call a VoIP.ms function that might not be available in this package yet.

Here is an example:

```
from voipms_api import VoipMsClient

vms_client = VoipMsClient(username="me@email.com", password="your VoIP.ms API password")
vms_client.get("getCountries", {"country": "CA"})
```

## Module Capabilities

Currently, the modules of accounts and voice features within the voipms-api package provide basic functionalities for creating, retrieving, and deleting items.

You will find the current available functions in the description of each class.

Additional functionalities will be added over time.

## Examples of scripts

You can find more examples of scripts in the examples directory in the [Github](https://github.com/joseanmont/voipms-api) repository. These scripts demonstrate how to use the some features of the voipms-api package.

## Development

Clone the repository and install the development environment with [pipenv](https://pipenv.pypa.io/) (Python version in `.python-version`):

```
pipenv sync --dev
pipenv run pytest
```

The tests mock the API, so no credentials are needed. To also run the tests that call the real API with the credentials in your `.env`:

```
VOIPMS_LIVE_TESTS=1 pipenv run pytest
```

### Releasing

Versions follow [Semantic Versioning](https://semver.org/): `MAJOR` for breaking changes, `MINOR` for new features, `PATCH` for bug fixes.

1. Update `version` in `pyproject.toml` and move the `Unreleased` notes in `CHANGELOG.md` under the new version and date. Run `pipenv sync --dev` so your local install picks up the new version.
2. Merge to `main`.
3. Tag the release and push the tag. GitHub Actions runs the tests and publishes to PyPI.

```
git tag v1.2.0
git push origin v1.2.0
```

## Contributing

Currently, we are not accepting collaborations. However, if you have suggestions or feedback, feel free to contact us. Issues can be reported on GitHub.

## License

This package is free to use and can be included in any project. See the LICENSE file for more details.

## Support

For any issues or questions, please raise an issue on GitHub or contact us directly at hello@joseanmont.info

## Special Thanks

Kudos to the VoIP.ms development team. They have developed an understandable, simple but still powerful API that lets users take their VoIP system beyond limits.
