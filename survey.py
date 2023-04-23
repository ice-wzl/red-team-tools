#!/usr/bin/python3
import sys
import warnings
import argparse
warnings.filterwarnings(action='ignore', module='paramiko\.*')
import paramiko
from termcolor import cprint
import logging

#TODO 
#add in a remote walk method? dir / and recursively dir directories like root home etc, not like proc and that stuff 


#create the logger
#give it a basic format, setting the output of the logger to stdout
#set the logging level to ERROR
log_format = "%(asctime)s - %(message)s"
logging.basicConfig(format = log_format, stream=sys.stdout, level = logging.ERROR)
logger = logging.getLogger()

class REMOTECONNECT:
    #create what is required for a remote connection, need a host, username, {password|key}, and port
    def __init__(self, host, username, password, key, port):
        self.host = host
        self.username = username 
        self.password = password
        self.key = key
        self.port = port
        self.client = None
        self.connect()

    def connect(self):
        try:
            #initialize the client 
            self.client = paramiko.SSHClient()
            #load all present system host keys 
            self.client.load_system_host_keys()
            #allow the system to auto add if the remote host key is new to us (most likely will be)
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            #this is where we check to see if the user is connecting via password or via key 
            if self.key == None:
                self.client.connect(hostname=self.host, username = self.username, password = self.password, port = self.port, timeout = 10, disabled_algorithms=None)
            else:
                self.client.connect(hostname=self.host, username = self.username, key_filename = self.key, port = self.port, timeout = 10, disabled_algorithms=None)
        except paramiko.SSHException as auth:
            print(auth)
            sys.exit(1)

    def do_command(self, command):
        try:
            #set stdin, stdout, and stderr all to the client....combine them all, we want output back to us either way if cmd was succ or not
            (stdin, stdout, stderr) = self.client.exec_command(command)
            #setting the ability to readlines of stdout to a var to avoid messy code
            cmd_output = stdout.readlines()
            #loop over the output returned from the cmd we just ran and print it back out to the user
            #this is a good spot to check if they want us to shove it to a file or to stdout 
            #this for loop prints all output back to the screen 
            for line in cmd_output:
                print(line, end='')            
        except:
            logging.error("Bad command(s)")
            sys.exit(1)

    #let the user run remote commands and save output to log file instead of printing to stdout 
    def do_logged_command(self, command, logfile):
        (stdin, stdout, stderr) = self.client.exec_command(command)
        cmd_output = stdout.readlines()
        for line in cmd_output:
            logfile = open(args.logfile, "a+")
            logfile.write(line)
            logfile.close()
                         
        
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
    parser.add_argument("-P", "--port", help="the remote port to connect to", action="store", dest="port")
    parser.add_argument("-l", "--log", help="write command output to logfile instead of stdout", action="store", dest="logfile")
    group_k_or_p = parser.add_mutually_exclusive_group(required=True)
    group_k_or_p.add_argument("-k", "--key", action="store", dest="key")
    group_k_or_p.add_argument("-p", "--password", action="store", dest="password")
    
    args = parser.parse_args()

    banner()

    try:
        #check the right amount of args have been passed in via cmdline 
        if not args.target or not args.username or not args.password and not args.key or not args.config or not args.port:
            logging.error("Wrong number of args, require {username, target, password|key, port, config}")
            sys.exit(2)
        #this is if user sets a log file, if they do we will log commands to specified logfile
        elif args.logfile:
            target_session = REMOTECONNECT(args.target, args.username, args.password, args.key, args.port)
            cprint("Authentication Successful with:", "green")
            print("    " + args.target)
            #check that the user is about to survey where they think
            p = input("Are you sure you want to survey?: (Y/n): ")
            p = p.lower()
            #check user response, if no, abort
            if p == "yes" or p == "y" or p == "":
                target_session.connect()
                logging.error("Connected to target...")
                #open up the supplied config and read line by line 
                input_file = open(args.config, 'r')
                for line in input_file.readlines():
                    #open the log file in append mode, write the command about to be executed and close so we dont have an open file handle when it gets 
                    #passed to the do_logged_command method
                    logfile = open(args.logfile, 'a+')
                    logfile.write(line)
                    logfile.close()
                    #print(line.strip('\n'))
                    #execute the command on the remote system and log output to file not stdout, see above method
                    target_session.do_logged_command(line, args.logfile)
        else:
            #instantiate the class with the required connection items 
            target_session = REMOTECONNECT(args.target, args.username, args.password, args.key, args.port)
            #cant hurt to double check
            cprint("Authentication Successful with:", "green")
            print("    " + args.target)
            #check that the user is about to survey where they think
            p = input("Are you sure you want to survey?: (Y/n): ")
            p = p.lower()
            #check user response, if no, abort
            if p == "yes" or p == "y" or p == "":
                target_session.connect()
                #give them some feedback that it worked
                logging.error("Connected to target...")
                #open up the supplied config and read line by line 
                input_file = open(args.config, 'r')
                for line in input_file.readlines():
                    #this print statment shows the cmd run remotely above the cmd output
                    print(line.strip('\n'))
                    #execute the command on the remote system, see above method
                    target_session.do_command(line)
            else:
                print("Aborting...")
                sys.exit(3)

    except Exception as e:
        print(e)
