#!/usr/bin/python3 
import sys
from scapy.all import srp,Ether,ARP,conf

if len(sys.argv) != 2:
    print("Usage aping.py <network>/CIDR")
    print(" --> python3 arping.py 10.10.10.0/24")
    sys.exit(1)

conf.verb = 0
ans,unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=sys.argv[1]), timeout=3)
for s,r in ans:
    print(r.sprintf("%Ether.src% %ARP.psrc%"))





