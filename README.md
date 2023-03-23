# Survey
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
