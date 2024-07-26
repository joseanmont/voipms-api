from voipms_api import General

vms_grl = General()

balance = vms_grl.get_balance()
print(balance["balance"])

conference = vms_grl.get_conference()
print(conference["conference"])