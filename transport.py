#!/usr/bin/python3
import sys
import os
import warnings
import argparse
warnings.filterwarnings(action='ignore', module='paramiko\.*')
import paramiko
import logging
from termcolor import cprint
import subprocess

log_format = "%(asctime)s - %(message)s"
logging.basicConfig(format = log_format, stream=sys.stdout, level = logging.ERROR)
logger = logging.getLogger()

class SFTPTransfer:
    def __init__(self, host, port, username, password):
        self.host = host
        self.username = username 
        self.password = password
        self.port = port
        self.transport = None
        self.sftp = None 

    def connect(self):
        try:
            self.transport = paramiko.Transport((self.host, int(self.port)))
            self.transport.connect(hostkey=None, username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.AuthenticationException as e:
            print("Authentication Failed: " + e)

    def remote_download(self, remote_path, local_path):
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.get(remote_path, local_path)

    def remote_upload(self, remote_path, local_path):
        if self.sftp is None:
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        self.sftp.put(local_path, remote_path)
    
    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()

    def prompt(self):
        p = self.username + "@" + self.host + "---> "
        return p

def banner():
    cprint('''
      __             __
   .-'.'     .-.     '.'-.
 .'.((      ( ^ `>     )).'.
/`'- \'. _____\ (_____.'/ -'`\ 
|-''`.'------' '------'.`''-|
|.-'`.'.'.`/ | | \`.'.'.`'-.|
 \ .' . /  | | | |  \ . '. /
  '._. :  _|_| |_|_  : ._.'
     ````` /T"Y"T\ `````
          / | | | \    transport v1.0
         `'`'`'`'`'`   Created By: ice-wzl
    ''')



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--target", action="store", dest="target")
    parser.add_argument("-P", "--port", action="store", dest="port")
    parser.add_argument("-u", "--username", action="store", dest="username")
    parser.add_argument("-p", "--password", action="store", dest="password")
    
    args = parser.parse_args()
    banner()

#TODO 
#not suck

    try:
        if not args.target or not args.username or not args.password:
            logging.error("Wrong number of args, require {username, target, password}")
            sys.exit(2)
        else:
            while True:
                transfer = SFTPTransfer(args.target, args.port, args.username, args.password)
                read_in_user_input = input(transfer.prompt())
                read_in_user_input = read_in_user_input.lower()
                if read_in_user_input == "exit":
                    sys.exit(10)
                elif read_in_user_input == "upload":
                    transfer.connect()
                    local_path = input("local file to put up: ")
                    remote_path = input("remote path for file: ")
                    transfer.remote_upload(remote_path, local_path)
                    transfer.disconnect()
                elif read_in_user_input == "download":
                    transfer.connect() 
                    remote_path = input("remote file to grab: ")
                    local_path = os.getcwd() + "/" + remote_path.split("/")[-1]
                    transfer.remote_download(remote_path, local_path)
                    print("Download Success " + remote_path)
                    transfer.disconnect()
                elif read_in_user_input == "pwd":
                   print(os.getcwd())
                elif read_in_user_input.split(" ")[0] == "cat":
                    os.system('cat ' + read_in_user_input.split(" ")[1])
                elif read_in_user_input.split(" ")[0] == "lls":
                    print(subprocess.check_output(['ls', '-la', read_in_user_input.split(" ")[1]]).decode('utf-8'))
                elif read_in_user_input == "help":
                    print('''
                exit     --> exit program
                help     --> print this menu
                upload   --> put local file on remote machine
                download --> download remote file to location machine. 
                             save path is your pwd + remote file name 
                lcd      --> change local directory
                lls      --> list current local directory
                cat      --> view file
                pwd      --> see current working directory 
                clear    --> clear screen''')
                elif "lcd" in read_in_user_input:
                    os.chdir(read_in_user_input.split(" ")[1])
                else:
                    print("Unknown Command, run help to see your options.")

    except Exception as e:
        print(e)
