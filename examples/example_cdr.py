from voipms_api import CDR, VoipMsError

cdr = CDR()

# Calls of the last week of one sub account, with times adjusted to UTC-6.
records = cdr.get_cdr("2026-11-02", "2026-11-09", timezone=-6, account="100000_VoIP")
for call in records.get("cdr", []):
    print(f"{call['date']} {call['callerid']} -> {call['destination']} {call['disposition']} {call['duration']}")

# Download every recording of the same period, from the main account and all the sub accounts.
recordings = cdr.get_call_recordings("2026-11-02", "2026-11-09")
for recording in recordings.get("recordings", []):
    file_name = f"{recording['account']}_{recording['datetime'].replace(':', '-')}_{recording['destination']}.mp3"
    try:
        cdr.get_call_recording(recording["account"], recording["callrecording"], file_path=file_name)
        print(f"Saved {file_name}")
    except VoipMsError as e:
        print(f"Could not download {recording['callrecording']}: {e}")

# Save the transcriptions of all the accounts as readable text.
cdr.get_call_transcriptions("2026-11-02", "2026-11-09", file_path="transcriptions.txt")
