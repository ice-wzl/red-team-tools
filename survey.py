#!/usr/bin/python3
import sys
import os
import warnings
import argparse
from datetime import datetime
warnings.filterwarnings(action='ignore', module='paramiko\.*')
import paramiko
import logging
log_format = "%(asctime)s - %(message)s"
logging.basicConfig(format = log_format, stream=sys.stdout, level = logging.ERROR)
logger = logging.getLogger()

class REMOTECONNECT:

    def __init__(self, host, username, password, key):
        self.host = host
        self.username = username 
        self.password = password
        self.key = key
        self.client = None
        self.connect()

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.key == None:
                self.client.connect(hostname=self.host, username = self.username, password = self.password, timeout = 5)
            else:
                self.client.connect(hostname=self.host, username = self.username, key_filename = self.key, timeout = 5)
        except:
            logging.error("Target is down, or authentication failed...")
            sys.exit(1)

    def do_command(self, command):
        try:
            (stdin, stdout, stderr) = self.client.exec_command(command)
            cmd_output = stdout.readlines()
            for line in cmd_output:
                print(line)            
        except:
            logging.error("Bad command(s)")
            sys.exit(1)

    def get_ssh_key(self):
        pass


def banner():
    print('''
          ____
     ---        ---
  ---              ---
 --        _         --      
--         |>         --
--         |<         --
 --        |>        --
  --       |<       --
   --      |>      --
    --     ||-    --
     --    ||    --
      --   ||   --
      |__________|
      <__________>    Survey v1.03
      <__________>    Created by: ice-wzl
           \/                     

    ''')
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", action="store", dest="target")
    parser.add_argument("-u", "--username", action="store", dest="username")
    parser.add_argument("-c", "--config", help="path to config file with commands to run on the remote host seperated by a new line.", action="store", dest="config")

    group_k_or_p = parser.add_mutually_exclusive_group(required=True)
    group_k_or_p.add_argument("-k", "--key", action="store", dest="key")
    group_k_or_p.add_argument("-p", "--password", action="store", dest="password")
    
    args = parser.parse_args()

    banner()

    try:
        if not args.target or not args.username or not args.password and not args.key:
            logging.error("Wrong number of args, require {username, target, password|key}")
            sys.exit(1)
        else:
            target_session = REMOTECONNECT(args.target, args.username, args.password, args.key)
            target_session.connect()
            logging.error("Connected to target...")

            input_file = open(args.config, 'r')
            for line in input_file.readlines():
                print(line.strip('\n'))
                target_session.do_command(line)
    except:
        sys.exit(1)
