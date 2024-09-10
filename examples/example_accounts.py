from voipms_api import Accounts

kwargs = {
    "subaccount": "206996_MyAPI-SubAcc",
    "password": "42wFhdK95sSz",
    "internal_extension": 250,
    "internal_voicemail": 101,
    "internal_cnam": "API CNAM new",
    "enable_internal_cnam": 1,
    "internal_extension": 8898,
}

acc = Accounts()
new_sub_account = acc.update_subaccount(**kwargs)
print(new_sub_account)