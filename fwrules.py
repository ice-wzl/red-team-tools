#!/usr/bin/python3

import argparse
import os 
import sys
import re 
import time 
import subprocess 


TIMEOUT = '360'
dbg = False 
ipt = '/sbin/iptables'
iptsave = '/sbin/iptables-save'
iptrestore = '/sbin/iptables-restore'
logfile = '/tmp/getopdatalog'

global my_ip

def lo_get_ip(ifname):
    #this function should get the ip from a specific interface
    pass

def lo_execute(cmd):
    #this function should be able to execute commands and return back to the user
    if dbg:
        print('# ' + cmd)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output = proc.stdout.read()
    return output

def lo_get_rules():
    #this function should get and return the rules 
    return lo_execute(ipt + ' -L -n -v --line-numbers')

def lo_clear_rules():
    #this function should clear out the rules, flush them all 
    #this will not change default policy i.e. if you have default DROP it will stay that way 
    return lo_execute(ipt + ' -F')

def lo_flush_accept():
    #this function should change back all the rules to default policy ACCEPT
    #should also flush the rules 
    lo_execute(ipt + ' -t filter -P INPUT ACCEPT')
    lo_execute(ipt + ' -t filter -P OUTPUT ACCEPT')
    lo_execute(ipt + ' -t filter -P FORWARD ACCEPT')
    lo_execute(ipt + ' -F')

def lo_set_local_rules():
    #this function should set the local rules 
    in_rules = [
            ipt + ' -t filter -P INPUT DROP',
            ipt + ' -t filter -A INPUT -i lo -j ACCEPT',
            ipt + ' -t filter -A INPUT -i eth0 -j ACCEPT',
            ipt + ' -t filter -P INPUT -i wlan0 -j ACCEPT',
            ]
    out_rules = [
            ipt + ' -t filter -P OUTPUT DROP',
            ipt + ' -t filter -A OUTPUT -o lo -j ACCEPT',
            ipt + ' -t filter -A OUTPUT -o eth0 -j ACCEPT',
            ipt + ' -t filter -A OUTPUT -o wlan0 -j ACCEPT',
            ]
    fwd_rules = [
            ipt + ' -t filter -P FORWARD DROP',
            ]
    for r in in_rules:
        lo_execute(r)
    for r in out_rules:
        lo_execute(r)
    for r in fwd_rules:
        lo_execute(r)

def lo_set_default_rules():
    #function should set the local rules, operating baseline 
    #need to figure out how to handle my_ip here...global var?? 
    in_rules = [
        ipt + ' -t filter -A INPUT -i eth0 -s 0.0.0.0/0 -d ' + my_ip + ' -m state --state ESTABLISHED -j ACCEPT',
        ipt + ' -t filter -A INPUT -i eth0 -p icmp -s 0.0.0.0/0 -d ' + my_ip + ' -m state --state ESTABLISHED,RELATED -j ACCEPT'
        ]
    out_rules = [
        ipt + '-t filter -A OUTPUT -o eth0 -p tcp -s ' + my_ip + ' -d 0.0.0.0/0 --dport 80 -j ACCEPT -m state --state NEW,ESTABLISHED',
        ipt + '-t filter -A OUTPUT -o eth0 -p tcp -s ' + my_ip + ' -d 0.0.0.0/0 --dport 443 -j ACCEPT -m state --state NEW,ESTABLISHED',
        ipt + '-t filter -A OUTPUT -o eth0 -p udp -s ' + my_ip + ' -d 0.0.0.0/0 --dport 53 -j ACCEPT',
        ipt + '-t filter -A OUTPUT -o eth0 -p icmp -s ' + my_ip + ' -d 0.0.0.0/0 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT',
        ]

    lo_set_local_rules()

    for r in in_rules:
        lo_execute(r)
    for r in out_rules:
        lo_execute(r)













