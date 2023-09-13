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

'''
ssh -vx -o ServerAliveInterval=90 -o ServerAliveCountMax=240 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -CMS /tmp/sock -p 22 root@10.10.120.1

'''

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
html_completer = WordCompleter(['shell', 'cmd', 'exit', 'structure', 'download', 'upload', 'ldownload', 'lupload'])

###
# IDK wtf im doing here 
###
# below will work but itll be in the context of your own machine not the remote host 
# need to get it to be in the context of the remote host 
def check_command_existence(cmd, socket, username):
    """
    Verifies that a given command exists on the machine.
    :param cmd: The command whose existence we want to check.
    :return: True if the command is present on the system, False otherwise.
    """
    #output = subprocess.Popen(["command", "-v", "%s >/dev/null ; echo $?".format(cmd)])
    #need subprocess.call here, will steal control from the main script, but it will only be for a second as that command wont hang 
    """
    import subprocess
    return_code = subprocess.call(["ssh", "-S", "/tmp/sock", "pi@", "'id'", ">/dev/null", ";echo", "$?"])
    if return_code == 0:
        print("Command executed successfully.")
    else:
        print("Command failed with return code", return_code)
    """
    output = subprocess.call(["ssh", "-S", "{}", "{}@", "'command -v {}'", ">/dev/null", ";echo", "$?".format(socket, username, cmd)])
    print(int(output))
    return int(output) == 0

def check_args(socket, username):
    """
    Verifies that the script is passed a socket file + username to use
    Check that the socket passed with -s actually is present
    Check that the username is passed with -u 
    """
    if not socket:
        logging.error("Wrong number of args, require -s <path-to-socket>")
        sys.exit(2)
    if not username:
        logging.error("Wrong number of args, require -u <username>\r\nThis is the username to use on the remote host when interacting")
        sys.exit(4)
    if not os.path.exists(socket):
        logging.error("Socket file {} not found!!!".format(socket))
        sys.exit(3)

def validate_path(path):
    if os.path.exists(path):
        return True
    else:
        return False

def create_structure(path):
    """
    Creates directory for the downloaded files
    Should expand upon this function in the future to build out a nice tree per host
    Very basic at the moment 
    """
    if os.path.isdir(path + '/target'):
        logging.error("{} already exists".format(path + "/target"))
    else:
        os.system(f'mkdir -p {path}/target')

def do_download(socket, username):
    """
    Downloads file off the remote host and saves it in user chosen location 
    ssh -S /tmp/sock pi@ 'cat /etc/passwd' > /tmp/target_passwd
    """
    r_path = input("Enter the file path to grab: ")
    file_name = r_path.split("/")[-1]
    l_path = input("Enter path to store file (default /tmp/target): ")
    if os.path.isdir("/tmp/target") and l_path == "":
        l_path = "/tmp/target"
    if validate_path(l_path) == False:
        print("No such file or directory, try again...")
    else:
        subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'cat {}' > {}/{}".format(socket, username, r_path, l_path, file_name)])
        return 0
      

def do_upload(socket, username):
    """
    Uploads a file from your local machine to the remote host
    l_path is validated, no way to easily validate r_path, should look into later
    ssh -S /tmp/sock pi@ 'cat > /dev/shm/.a' < /tmp/shell 
    """
    l_path = input("Enter the abs path of the file to upload: ")
    if validate_path(l_path) == False:
        print("No such file or directory, try again...")
        return 1
    r_path = input("Enter the path to upload the file to: ")
    subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'cat > {}' < {}".format(socket, username, r_path, l_path)])
    return 0

def do_download_large(socket, username):
    """
    Downloads larger files from the remote host and saves it in a user chosen location
    Uses zip | gzip
    Should add functionaility to ensure method passed is is actually on device before just running subprocess.Popen
    """
    r_path = input("Enter the file path to grab: ")
    file_name = r_path.split("/")[-1]
    l_path = input("Enter path to store file (default /tmp/target): ")
    if os.path.isdir("/tmp/target") and l_path == "":
        l_path = "/tmp/target"
    if validate_path(l_path) == False:
        print("No such file or directory, try again...")
    else:
        subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'cat {} | gzip' > {}/{}".format(socket, username, r_path, l_path, file_name)])
        return 0
    


def do_upload_large(socket, username):
    '''
    Function to upload a large file to the remote host 
    Two current method are gzip and zip 
    Should add functionaility to ensure method passed is is actually on device before just running subprocess.Popen
    '''
    l_path = input("Enter the abs path of the file to upload: ")
    if validate_path(l_path) == False:
        print("No such file or directory, try again...")
        return 1
    r_path = input("Enter the path to upload the file to: ")
    subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'gzip > {}' < {}".format(socket, username, r_path, l_path)])
    return 0


def spawn_shell(socket, username):
    #ssh -S /tmp/sock pi@ '/bin/sh'
    print("Shell Options:\r\n\r\n/bin/sh (default)\r\n/bin/bash\r\n")
    shell_type = input("Shell Type: ")
    if shell_type == "":
        shell_type = "/bin/sh"
    subprocess.Popen(['xterm', '-e', 'ssh -S {} {}@ "{}"'.format(socket, username, shell_type)], start_new_session=True)
    return 0

def single_cmd(socket, username):
    #ssh -S /tmp/sock pi@ 'id'
    cmd = input("Enter cmd: ")
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
    parser.add_argument("-u", "--username", action="store", dest="username")
    #should have a username arg here and then avoid all the prompts for it 
    #user would set a default username to use for the script 
    #can have a option to switch the username, would be a command to use 

    args = parser.parse_args()

    banner()
    check_args(args.socket, args.username)

    keep_going = True
    try:
        while keep_going:
            #set up our prompt from prompt_toolkit
            session = PromptSession()
            options = session.prompt(message=message, style=style, completer=html_completer)
            options = options.lower()
            options = options.rstrip()

            if options == "shell":
                spawn_shell(args.socket, args.username)

            elif options == 'cmd':
                single_cmd(args.socket, args.username)

            elif options == 'exit':
                print("Goodbye...")
                keep_going = False

            elif options == 'structure':
                path = input("Enter abs path to create directory tree: ")
                if path == "":
                    path = '/tmp'
                create_structure(path)

            elif options == 'download':
                do_download(args.socket, args.username)
            
            elif options == 'upload':
                do_upload(args.socket, args.username)

            elif options == 'test':
                status = check_command_existence('whoami', args.socket, "x")
                if status == True:
                    print("Yes")
                else:
                    print("ugh")

            elif options == 'ldownload':
                do_download_large(args.socket, args.username)

            elif options == 'lupload':
                do_upload_large(args.socket, args.username)


        
    except:
        print("You made the panda sad <panda emoji here>")
        

