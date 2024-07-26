from voipms_api import LNP

dids_to_verify = [2052550000, 4388650000, 4044102500]

lnp = LNP()

for did in dids_to_verify:
    x = lnp.get_portability(did)
    result = x["result"]["portable"]
    print(f"The portability verification for {did} returned {result}")