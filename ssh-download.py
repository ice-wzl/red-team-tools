#!/usr/bin/python3
import argparse
import logging
import os
from time import sleep
import subprocess
import sys
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

'''
ssh -vx -o ServerAliveInterval=90 -o ServerAliveCountMax=240 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -CMS /tmp/sock -p 22 root@10.10.120.1

'''

log_format = "%(asctime)s - %(message)s"
logging.basicConfig(format=log_format, stream=sys.stdout, level=logging.ERROR)
logger = logging.getLogger()

style = Style.from_dict({
    # User input (default text).
    '': '#FFFAF0',
    # Prompt.
    'host': '#7CFC00',
    'arrow': '#FFFAF0',
})
# what the prompt is going to look like remotehost -->
message = [
    ('class:host', 'remotehost'),
    ('class:arrow', '--> '),
]

# create the prompt suggester
html_completer = WordCompleter(
    ['shell', 'cmd', 'exit', 'download', 'upload', 'large-download', 'dir-download', 'large-upload', 'dir-upload'])


def check_args(socket, username, structure):
    """
    Verifies that the script is passed a socket file + username to use
    Check that the socket passed with -s actually is present
    Check that the username is passed with -u 
    """
    if not socket:
        logging.error(
            "Wrong number of args, require:\r\n"
            "-s <path-to-socket>\r\n"
            "-u <username>\r\n"
            "-p <file storage dir>"
            "\r\npython3 ssh-download.py -h for more help")
        sys.exit(2)
    if not username:
        logging.error(
            "Wrong number of args, require -u <username>\r\n"
            "This is the username to use on the remote host when interacting")
        sys.exit(4)
    if not os.path.exists(socket):
        logging.error("Socket file {} not found!!!".format(socket))
        sys.exit(3)
    if not validate_path(structure):
        os.mkdir(structure)


def validate_path(path):
    if os.path.exists(path):
        return True
    else:
        return False


def do_download(socket, username, structure):
    """
    Downloads file off the remote host and saves it in user chosen location 
    ssh -S /tmp/sock pi@ 'cat /etc/passwd' > /tmp/target_passwd
    """
    r_path = input("Enter the file path to grab: ")
    file_name = r_path.split("/")[-1]
    subprocess.Popen(
        ["xterm", "-e", "ssh -S {} {}@ 'cat {}' > {}/{}".format(socket, username, r_path, structure, file_name)])
    return 0


def do_download_large(socket, username, structure):
    """
    Downloads larger files from the remote host and saves it in a user chosen location
    Uses zip | gzip
    Should add functionaility to ensure method passed is is actually on device before just running subprocess.Popen
    """
    r_path = input("Enter the file path to grab: ")
    file_name = r_path.split("/")[-1]
    subprocess.Popen(["xterm", "-e",
                      "ssh -S {} {}@ 'cat {} | gzip' > {}/{}".format(socket, username, r_path, structure, file_name)])
    return 0


def download_dir(socket, username, structure):
    r_path = input("Enter the directory to grab: ")
    dir_name = r_path.split("/")[-1]
    if not os.path.exists("/tmp/target/{}".format(dir_name)):
        os.mkdir("{}/{}".format(structure, dir_name))
    l_path = structure + "/" + dir_name
    # -----------------
    files_in_dir = subprocess.Popen(
        ['xterm', '-e', 'ssh -S {} {}@ "ls {}" > /tmp/temp'.format(socket, username, r_path)], start_new_session=True)
    sleep(1.5)
    with open('/tmp/temp', 'r') as fp:
        read_in = fp.read()
        for i in read_in.split():
            subprocess.Popen(
                ["xterm", "-e", "ssh -S {} {}@ 'cat {}/{}' > {}/{}".format(socket, username, r_path, i, l_path, i)])
        os.system('rm /tmp/temp')
        return 0


def do_upload(socket, username):
    """
    Uploads a file from your local machine to the remote host
    l_path is validated, no way to easily validate r_path, should look into later
    ssh -S /tmp/sock pi@ 'cat > /dev/shm/.a' < /tmp/shell 
    """
    l_path = input("Enter the abs path of the file to upload: ")
    if not validate_path(l_path):
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
    if not validate_path(l_path):
        print("No such file or directory, try again...")
        return 1
    r_path = input("Enter the path to upload the file to: ")
    subprocess.Popen(["xterm", "-e", "ssh -S {} {}@ 'gzip > {}' < {}".format(socket, username, r_path, l_path)])
    return 0


def directory_upload(socket, username):
    # ssh -S /tmp/sock pi@ 'cat > /dev/shm/.a' < /tmp/shell
    l_path = input("Enter the abs path of the directory to upload: ")
    if not validate_path(l_path):
        print("No such file or directory, try again...")
        return 1
    r_path = input("Enter the path to upload the file to: ")
    for i in os.listdir(l_path):
        subprocess.Popen(
            ["xterm", "-e", "ssh -S {} {}@ 'cat > {}/{}' < {}/{}".format(socket, username, r_path, i, l_path, i)])
    return 0


def spawn_shell(socket, username):
    # ssh -S /tmp/sock pi@ '/bin/sh'
    print("Shell Options:\r\n\r\n/bin/sh (default)\r\n/bin/bash\r\n")
    shell_type = input("Shell Type: ")
    if shell_type == "":
        shell_type = "/bin/sh"
    subprocess.Popen(['xterm', '-e', 'ssh -S {} {}@ "{}"'.format(socket, username, shell_type)], start_new_session=True)
    return 0


def single_cmd(socket, username):
    # ssh -S /tmp/sock pi@ 'id'
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

    parser.add_argument("-s", "--socket", action="store", dest="socket", help="The socket file to connect to")
    parser.add_argument("-u", "--username", action="store", dest="username",
                        help="The username to use when interacting with the remote host")
    parser.add_argument("-p", "--path", action="store", dest="structure",
                        help="Creates a directory to store your collected files")

    args = parser.parse_args()

    banner()
    check_args(args.socket, args.username, args.structure)

    keep_going = True
    try:
        while keep_going:
            # set up our prompt from prompt_toolkit
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

            elif options == 'download':
                do_download(args.socket, args.username, args.structure)

            elif options == 'dir-download':
                download_dir(args.socket, args.username, args.structure)

            elif options == 'dir-upload':
                directory_upload(args.socket, args.username)

            elif options == 'upload':
                do_upload(args.socket, args.username)

            elif options == 'large-download':
                do_download_large(args.socket, args.username, args.structure)

            elif options == 'large-upload':
                do_upload_large(args.socket, args.username)

    except Exception as e:
        print("You made the mermaid sad " + '\U0001F9DE')
        print(e)
