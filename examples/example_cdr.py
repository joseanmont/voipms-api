from voipms_api import CDR, VoipMsError

cdr = CDR()
account = "100000_VoIP"

# Calls of the last week, with times adjusted to UTC-6.
records = cdr.get_cdr("2026-11-02", "2026-11-09", timezone=-6, account=account)
for call in records.get("cdr", []):
    print(f"{call['date']} {call['callerid']} -> {call['destination']} {call['disposition']} {call['duration']}")

# Download every recording of the same period.
recordings = cdr.get_call_recordings(account, "2026-11-02", "2026-11-09")
for recording in recordings.get("recordings", []):
    file_name = f"{recording['datetime'].replace(':', '-')}_{recording['destination']}.mp3"
    try:
        cdr.get_call_recording(account, recording["callrecording"], file_path=file_name)
        print(f"Saved {file_name}")
    except VoipMsError as e:
        print(f"Could not download {recording['callrecording']}: {e}")

# Save the transcriptions as readable text.
cdr.get_call_transcriptions(account, "2026-11-02", "2026-11-09", file_path="transcriptions.txt")
