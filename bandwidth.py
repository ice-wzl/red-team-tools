#!/usr/bin/python3 
import os
import psutil
from termcolor import cprint 
from datetime import datetime
import argparse
from time import sleep

###Alternate Methods####
#get ip addresses
#[[i.address for i in x if i.family == socket.AF_INET] for x in psutil.net_if_addrs().values()]
#bytes sent 
#[x.bytes_sent for x in psutil.net_io_counters(pernic=True).values()] 
########################

def get_bytes_for_interfaces_log():
    interface_list = psutil.net_if_addrs().keys()
    ifile = "bwon_logging.txt"
    handle = open(ifile, "a+")
    handle.write(str(date_time) + "\n")
    for i in interface_list:
        interface_bytes = psutil.net_io_counters(pernic=True)
        get_each_interface_bytes = interface_bytes.get(i)
        bytes_sent = round(get_each_interface_bytes[0] / 1048576, 2)
        bytes_recv = round(get_each_interface_bytes[1] / 1048576, 2)
        if bytes_sent > 100 and i != "lo":
            cprint("%s: Bytes Sent: %s MB, Bytes Recv: %s MB" % (i, bytes_sent,bytes_recv), "red", attrs=["bold"])
            handle.write(str("%s: Bytes Sent: %s MB, Bytes Recv: %s MB\n" % (i, bytes_sent,bytes_recv)))
        else:
            print("%s: Bytes Sent: %s MB, Bytes Recv: %s MB" % (i, bytes_sent,bytes_recv))
            handle.write(str("%s: Bytes Sent: %s MB, Bytes Recv: %s MB\n" % (i, bytes_sent,bytes_recv)))
    handle.write("\n")
    handle.close()


def get_bytes_for_interfaces():
    interface_list = psutil.net_if_addrs().keys()
    for i in interface_list:
        interface_bytes = psutil.net_io_counters(pernic=True)
        get_each_interface_bytes = interface_bytes.get(i)
        bytes_sent = round(get_each_interface_bytes[0] / 1048576, 2)
        bytes_recv = round(get_each_interface_bytes[1] / 1048576, 2)
        if bytes_sent > 100 and i != "lo":
            cprint("%s: Bytes Sent: %s MB, Bytes Recv: %s MB" % (i, bytes_sent,bytes_recv), "red", attrs=["bold"])
        else:
            print("%s: Bytes Sent: %s MB, Bytes Recv: %s MB" % (i, bytes_sent,bytes_recv))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--no-log", help="Will not store a log file", action="store_false", dest="log")
    parser.add_argument("-p", "--polling-interval", help="Defines polling interval in seconds", action="store", dest="poll")

    args = parser.parse_args()

    while True:
        now = datetime.now()        
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        if args.log == True:
            get_bytes_for_interfaces_log()
        else:
            get_bytes_for_interfaces()
        sleep(int(args.poll))
        os.system("clear")