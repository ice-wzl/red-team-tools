#!/usr/bin/python3 
import os
import sys
try:
    from scapy.all import srp,Ether,ARP,conf
except ModuleNotFoundError:
    print("[!] Scapy not found...pip3 install scapy")
    sys.exit(3)


if len(sys.argv) != 2:
    print("Usage aping.py <network>/CIDR")
    print(" --> python3 arping.py 10.10.10.0/24")
    print(" --> python3 arping.py 192.168.15.1")
    sys.exit(1)

if os.getuid() != 0:
    print("[!] Script must be run as root...")
    sys.exit(2)

conf.verb = 0
ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=sys.argv[1]), timeout=3)
for s,r in ans:
    print(r.sprintf("%Ether.src% <--> %ARP.psrc%"))



