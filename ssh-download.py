#!/usr/bin/python3
import argparse 
import logging
import os
import subprocess
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

log_format = "%(asctime)s - %(message)s"
logging.basicConfig(format = log_format, stream=sys.stdout, level = logging.ERROR)
logger = logging.getLogger()

style = Style.from_dict({
    # User input (default text).
        '':          '#ff0066',
    # Prompt.
        'host':     '#BBEEFF',
        'arrow':     '#00ffff',
    })
#what the prompt is going to look like localhost -->
message = [
    ('class:host',     'remotehost'),
    ('class:arrow',    '--> '),
    ]

#create the prompt suggester
html_completer = WordCompleter(['shell', 'cmd'])


def do_download(r_path, l_path):
    pass

def do_upload(r_path, l_path):
    pass

def do_download_large(r_path, l_path, method):
    pass

def do_upload_large(r_path, l_path, method):
    pass 


def spawn_shell(shell_type, username, socket):
    #ssh -S /tmp/sock pi@ '/bin/sh'
    subprocess.Popen(['xterm', '-e', 'ssh -S {} {}@ "{}"'.format(socket, username, shell_type)], start_new_session=True)
    return 0

def single_cmd(username, cmd, socket):
    #ssh -S /tmp/sock pi@ 'id'
    subprocess.Popen(['xterm', '-e', 'ssh -S {} {}@ "{}"'.format(socket, username, cmd)], start_new_session=True)


def banner():
    print("""
         ,MMM8&&&.
    _...MMMMM88&&&&..._
 .::'''MMMMM88&&&&&&'''::.
::     MMMMM88&&&&&&     ::
'::....MMMMM88&&&&&&....::' - Created by: ice-wzl
   `''''MMMMM88&&&&''''`    - v1.0.0
         'MMM8&&&'

""")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--socket", action="store", dest="socket")
    
    args = parser.parse_args()

    banner()
    if not args.socket:
            logging.error("Wrong number of args, require -s <path-to-socket>")
            sys.exit(2)

    try:
        while True:
            #set up our prompt from prompt_toolkit
            session = PromptSession()
            options = session.prompt(message=message, style=style, completer=html_completer)
            options = options.lower()
            options = options.rstrip()
            if options == "shell":
                print("Shell Options:\r\n/bin/sh\r\n/bin/bash\r\n")
                shell_type = input("Shell Type: ")
                username = input("Username: ")
                spawn_shell(shell_type, username, args.socket)
            elif options == 'cmd':
                cmd = input("Enter cmd: ")
                username = input("Username: ")
                single_cmd(username, cmd, args.socket)
        
    except:
        print("Cry")
        

