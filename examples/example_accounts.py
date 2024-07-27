from voipms_api import Accounts

kwargs = {
    "username": "MyAPI-SubAccount",
    "password": "42wFhdK95sSz",
    "extension": 1,
}

acc = Accounts()
new_sub_account = acc.create_subaccount(**kwargs)
print(new_sub_account)