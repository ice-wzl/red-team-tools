#!/usr/bin/python3 
import os
import socket
import sys
from random import randint
try:
    from scapy.all import *
except ModuleNotFoundError:
    print("[!] Scapy not found...pip3 install scapy")
    sys.exit(3)


if len(sys.argv) != 3:
    print("Usage tcping.py <ip> <port>")
    print(" --> python3 tcping.py 192.168.15.100 22")
    print(" --> python3 tcping.py 192.168.15.100 22,23,80,445,8006")
    sys.exit(1)

if os.getuid() != 0:
    print("[!] Script must be run as root...")
    sys.exit(2)

# packet = IP(version=4, src="192.168.15.172", dst="192.168.15.100")/TCP(sport=50000, dport=8006)

hostname = socket.gethostname()
src_ip_address = socket.gethostbyname(hostname)
conf.verb = 0


if "," in sys.argv[2]:
    ports = [x for x in sys.argv[2].split(",")]
    for i in ports:
        packet= sr1(IP(version=4, src=str(src_ip_address), dst=str(sys.argv[1]))/TCP(sport=randint(30000,55000), dport=int(i), flags="S"))

        if packet['TCP'].flags == 0x12:
            print(f"{sys.argv[1]} {i} --> Open")
        elif packet['TCP'].flags == 0x14:
            print(f"{sys.argv[1]} {i} --> Closed")
        else:
            print(f"Weird response: {packet}")
    sys.exit(1)
else:

    packet= sr1(IP(version=4, src=str(src_ip_address), dst=str(sys.argv[1]))/TCP(sport=randint(30000,55000), dport=int(sys.argv[2]), flags="S"))


    if packet['TCP'].flags == 0x12:
        print(f"{sys.argv[1]} {sys.argv[2]} --> Open")
    elif packet['TCP'].flags == 0x14:
        print(f"{sys.argv[1]} {sys.argv[2]} --> Closed")
    else:
        print(f"Weird response: {packet}")

