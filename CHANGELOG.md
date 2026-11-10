# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Releases before 1.2.0 were published as pre-releases (`bNN` suffix).

## [2.1.0] - 2026-11-10

### Added
- `CDR` module:
  - `get_cdr`: call detail records for a date range.
  - `get_call_recordings` (all the accounts by default), `get_call_recording` (with `file_path` to save the audio), `delete_call_recording` and `send_call_recording_email`.
  - `get_call_transcriptions` (all the accounts by default, with `file_path` to save them as readable text
    and `include_account` to add the account of each one, which the API does not return).
  - `get_call_accounts`, `get_call_types` and `get_call_billing`, the values accepted by the filters.

## [2.0.0] - 2026-11-10

Errors are now raised as exceptions instead of being printed. On success, every method returns the same as in 1.x.

### Migrating from 1.x
- Replace `if result is None:` checks with `try` / `except VoipMsError:` (or the specific exceptions below).
- Replace `make_request(...)` with `get(...)`.
- Replace `module.vms_client.<attr>` with `module.<attr>` (e.g. `lnp.vms_client.username` → `lnp.username`).

### Added
- Exceptions `VoipMsError` (base), `VoipMsApiError` (with `method`, `status` and `response`) and `VoipMsConnectionError`.

### Changed
- **Breaking:** errors raise exceptions instead of printing a message and returning `None` (or an error message string).
  - The API answering with a status other than `success` raises `VoipMsApiError`. Before, these responses were returned as if they had succeeded.
  - Network errors, timeouts, HTTP errors and invalid responses raise `VoipMsConnectionError`. Its message does not include the API password.
  - Invalid arguments raise `ValueError` (`get_conference_recordings` raised `TypeError`).
  - `send_fax` raises `FileNotFoundError` (or other `OSError`) when the file cannot be read.
- On queries (`get...` API methods), a `no_...` status (e.g. `no_sms`) means there are no results and is returned without raising.
- `update_*` and `delete_*` methods raise `ValueError` when the item to change does not exist, instead of a `KeyError`.
- `create_call_hunting`, `create_ring_group` and `create_ivr` only look up the main account when `members`/`options` are not given. They no longer fail when the account has no sub accounts and members are given.
- `get` and `post` no longer modify the `params` dict passed to them.

### Removed
- **Breaking:** `VoipMsClient.make_request` and the `vms_client` attribute, deprecated in 1.2.1.

## [1.2.1] - 2026-10-23

### Fixed
- Restored compatibility with 1.1.5b11, broken in 1.2.0:
  - `VoipMsClient.make_request` is back as a deprecated alias of `get`.
  - The `vms_client` attribute of the modules is back as a deprecated alias of the object itself.
  - `get_conference`, `get_conference_members`, `get_conference_recordings`, `get_conference_recording_file`
    and `get_transactions` return `None` on error again, instead of an error message string.

### Deprecated
- `make_request` and `vms_client` emit a `DeprecationWarning` and will be removed in 2.0.0.

## [1.2.0] - 2026-10-23

### Added
- `Fax` module with `send_fax`.
- `VoipMsClient.post` to call API methods with the parameters in the request body.
- `timeout` argument on `VoipMsClient` (default 30 seconds). Requests no longer wait forever.
- `voipms_api.__version__`.

### Changed
- Python 3.11 or newer is now required.
- Development environment moved to Python 3.13.

### Fixed
- Modules could not be imported from the installed package (`ModuleNotFoundError: No module named 'voipms_client'`).
- `send_fax` failed to read the file to send.
- `post` always failed with HTTP 500: the API only accepts POST as multipart/form-data. Parameters (including large fax files) are now sent that way, in the request body.
- `test_connection` ignored `verify=False`.
- `verify` and `timeout` were not used for the lookups done by `create_call_hunting`, `create_ring_group` and `create_ivr`.
- `get_sms` and `get_conference_recordings` accepted `date_to` without `date_from`.
- `create_subaccount` and `update_subaccount` accepted `internal_cnam` when `enable_internal_cnam` was `'0'`.

## [1.1.5b11] - 2024-09-10

### Added
- DIDs: `set_did_routing`.

## [1.1.4b11]

### Changed
- Accounts: `create_sub_account` and `update_subaccount`.
  - Additional validations for the username on `create_sub_account`.
  - Argument `extension` renamed to `internal_extension`.
  - Optional argument `internal_voicemail`.
  - Optional argument `internal_cnam` to set a Caller ID name for internal calls.
  - Optional argument `enable_internal_cnam` to enable/disable the internal Caller ID name.

## [1.1.3b11]

### Fixed
- `create_call_hunting` and `update_call_hunting` did not allow adding multiple members.

## [1.1.2b11]

### Added
- Accounts: `update_subaccounts`.
- CallHunting: `update_call_hunting`.
- Forwarding: `update_forwarding`.
- IVR: `update_ivr`.
- RingGroup: `update_ring_group`.
- SMS: `get_sms`.
- Voicemail: `update_voicemail`.

### Changed
- Accounts: `create_sub_account`.
  - Argument `password` is optional so sub accounts can use IP authentication.
  - Optional arguments `ip`, `codecs`, `lock_international` and `callerid_number`.
- RingGroup: `create_ring_group` accepts the optional arguments `announcement`, `music_on_hold` and `language`.

### Fixed
- General: `get_transactions` did not allow getting records from a single day.

## [1.0.2b11]

### Changed
- `create_sub_account` accepts `description` as an optional argument.

## [1.0.1b11]

### Fixed
- Importing errors when using the module Voicemail.

## [1.0.0b11]

### Changed
- All modules were refactored to improve imports.
