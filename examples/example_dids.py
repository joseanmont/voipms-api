from voipms_api import DIDs

dids = DIDs()
my_dids = dids.get_dids_info()
print(my_dids["dids"])