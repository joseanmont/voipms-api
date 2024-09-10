from voipms_api import Accounts

kwargs = {
    "username": "MyAPI-SubAcc",
    "password": "MyExamplePassword",
    "internal_extension": 250,
    "internal_voicemail": 1,
    "internal_cnam": "MY INT CNAM",
    "enable_internal_cnam": 1,
    "internal_extension": 8898,
}

acc = Accounts()
new_sub_account = acc.create_subaccount(**kwargs)
print(new_sub_account)