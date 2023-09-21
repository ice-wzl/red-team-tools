#!/usr/bin/python3
import argparse 
import logging
import os
from time import sleep
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
#what the prompt is going to look like remotehost -->
message = [
    ('class:host',     'remotehost'),
    ('class:arrow',    '--> '),
    ]

#create the prompt suggester
html_completer = WordCompleter(['shell', 'cmd', 'exit', 'structure', 'download', 'upload', 'ldownload', 'ddownload', 'lupload', 'dupload'])


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
    
def download_dir(socket, username):
    #this function is still extremely flawed 
    #hangs when you enter /tmp/target as the l_path 
    #works fine when you just hit enter and the script sets /tmp/target as your l_path
    #should give the user a choice where to store 
    #should check that the structure is created before running any command 
    #should just save it where the user creates the target dir with the dir name being based on the remote host 
    #no reason to over complicate things here should just be directory to grab and save at structure target remote dir name 
    #less confusion from the operator pov 
    #to take it a step further from that should take the entire remote path and create a structure of the remote machine i.e. 
    #if /home/rocky/Documnets/views directory is collected on the local station should be {structure location}/target/home/rocky/Documents/views/files 
    #this would help with organization 
    r_path = input("Enter the directory to grab: ")
    dir_name = r_path.split("/")[-1]
    l_path = input("Enter path to store file (default /tmp/target): ")
    
    #need to make below a function
    if l_path == "" and os.path.exists("/tmp/target"):
        l_path = "/tmp/target"
    if validate_path(l_path) == False:
        print("No such file or directory, try again...")
        return 1
    if l_path == "/tmp/target" or l_path == "" and not os.path.exists("/tmp/target/{}".format(dir_name)):
        os.mkdir("{}/{}".format(l_path, dir_name))
    l_path = l_path + "/" + dir_name
    #-----------------
    #get list of files on remote host 
    files_in_dir = subprocess.Popen(['xterm', '-e', 'ssh -S {} {}@ "ls {}" > /tmp/temp'.format(socket, username, r_path)], start_new_session=True)
    sleep(1.5)
    #subprocess.Popen(['xterm', '-e', 'ssh -S {} {}@ "ls {}" > /tmp/temp'.format(socket, username, r_path)], start_new_session=True)
    with open('/tmp/temp', 'r') as fp:
        read_in = fp.read()
        for i in read_in.split():
            #subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'cat {}/{} | gzip' > {}/{}".format(socket, username, r_path, i, l_path, i)])
            subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'cat {}/{}' > {}/{}".format(socket, username, r_path, i, l_path, i)])
        os.system('rm /tmp/temp')
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

def directory_upload(socket, username):
    #ssh -S /tmp/sock pi@ 'cat > /dev/shm/.a' < /tmp/shell 
    l_path = input("Enter the abs path of the directory to upload: ")
    if validate_path(l_path) == False:
        print("No such file or directory, try again...")
        return 1
    r_path = input("Enter the path to upload the file to: ")
    for i in os.listdir(l_path):
        subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'cat > {}/{}' < {}/{}".format(socket, username, r_path, i, l_path, i)])
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

            elif options == 'ddownload':
                download_dir(args.socket, args.username)

            elif options == 'dupload':
                directory_upload(args.socket, args.username)

            elif options == 'upload':
                do_upload(args.socket, args.username)

            elif options == 'ldownload':
                do_download_large(args.socket, args.username)

            elif options == 'lupload':
                do_upload_large(args.socket, args.username)


        
    except Exception as e:
        print("You made the mermaid sad " + '\U0001F9DE')
        print(e)

