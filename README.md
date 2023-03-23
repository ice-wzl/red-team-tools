# Survey
# Installation 
````
git clone https://github.com/ice-wzl/survey.git
cd survey/
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
root@10.0.0.5---> download
remote file to grab: /etc/passwd
Download Success /etc/passwd
````
- Verify that your download worked 
````
root@10.0.0.5---> lls .
total 40
drwxrwxr-x. 3 rocky rocky  159 Mar 23 16:48 .
drwxrwxr-x. 3 rocky rocky   44 Mar 23 16:40 ..
-rw-rw-r--. 1 rocky rocky 1790 Mar 23 16:48 passwd
````
## Logging Considerations 
## transport.py 
- For a file download this is what logging will look like, we are working to mitigate some of these:
- `/var/log/auth.log`
````
Mar 23 20:53:45 gitlab sshd[1374]: Accepted password for root from 10.0.0.3 port 39982 ssh2
Mar 23 20:53:45 gitlab sshd[1374]: pam_unix(sshd:session): session opened for user root(uid=0) by (uid=0)
Mar 23 20:53:45 gitlab systemd-logind[165]: New session 15 of user root.
Mar 23 20:53:49 gitlab sshd[1374]: pam_unix(sshd:session): session closed for user root
Mar 23 20:53:49 gitlab systemd-logind[165]: Session 15 logged out. Waiting for processes to exit.
Mar 23 20:53:49 gitlab systemd-logind[165]: Removed session 15.
````
- File upload:
````
Mar 23 20:56:11 gitlab sshd[1430]: Accepted password for root from 10.0.0.3 port 54274 ssh2
Mar 23 20:56:11 gitlab sshd[1430]: pam_unix(sshd:session): session opened for user root(uid=0) by (uid=0)
Mar 23 20:56:11 gitlab systemd-logind[165]: New session 16 of user root.
Mar 23 20:56:17 gitlab sshd[1430]: pam_unix(sshd:session): session closed for user root
Mar 23 20:56:17 gitlab systemd-logind[165]: Session 16 logged out. Waiting for processes to exit.
Mar 23 20:56:17 gitlab systemd-logind[165]: Removed session 16.
````
- `/var/log/syslog`
- File download:
````
Mar 23 20:57:45 gitlab systemd[1]: Started OpenBSD Secure Shell server per-connection daemon (10.0.0.3:36874).
Mar 23 20:57:45 gitlab systemd[1]: Started Session 17 of User root.
Mar 23 20:57:48 gitlab systemd[1]: ssh@5-10.0.0.5:22-10.0.0.3:36874.service: Deactivated successfully.
Mar 23 20:57:48 gitlab systemd[1]: session-17.scope: Deactivated successfully.
````
- File upload:
````
Mar 23 20:58:17 gitlab systemd[1]: Started OpenBSD Secure Shell server per-connection daemon (10.0.0.3:45948).
Mar 23 20:58:17 gitlab systemd[1]: Started Session 18 of User root.
Mar 23 20:58:26 gitlab systemd[1]: ssh@6-10.0.0.5:22-10.0.0.3:45948.service: Deactivated successfully.
Mar 23 20:58:26 gitlab systemd[1]: session-18.scope: Deactivated successfully.
````
- `journalctl -xe`
````
A session with the ID 17 has been terminated.
Mar 23 20:58:17 gitlab systemd[1]: Started OpenBSD Secure Shell server per-connection daemon (10.0.0.3:>
░░ Subject: A start job for unit ssh@6-10.0.0.5:22-10.0.0.3:45948.service has finished successfully
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ A start job for unit ssh@6-10.0.0.5:22-10.0.0.3:45948.service has finished successfully.
░░ 
░░ The job identifier is 1428.
Mar 23 20:58:17 gitlab sshd[1514]: Accepted password for root from 10.0.0.3 port 45948 ssh2
Mar 23 20:58:17 gitlab sshd[1514]: pam_unix(sshd:session): session opened for user root(uid=0) by (uid=>
Mar 23 20:58:17 gitlab systemd-logind[165]: New session 18 of user root.
░░ Subject: A new session 18 has been created for user root
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ Documentation: sd-login(3)
░░ 
░░ A new session with the ID 18 has been created for the user root.
░░ 
░░ The leading process of the session is 1514.
Mar 23 20:58:17 gitlab systemd[1]: Started Session 18 of User root.
░░ Subject: A start job for unit session-18.scope has finished successfully
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ A start job for unit session-18.scope has finished successfully.
░░ 
░░ The job identifier is 1488.
Mar 23 20:58:25 gitlab sshd[1514]: pam_unix(sshd:session): session closed for user root
Mar 23 20:58:26 gitlab systemd[1]: ssh@6-10.0.0.5:22-10.0.0.3:45948.service: Deactivated successfully.
░░ Subject: Unit succeeded
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ The unit ssh@6-10.0.0.5:22-10.0.0.3:45948.service has successfully entered the 'dead' state.
Mar 23 20:58:26 gitlab systemd[1]: session-18.scope: Deactivated successfully.
░░ Subject: Unit succeeded
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ 
░░ The unit session-18.scope has successfully entered the 'dead' state.
Mar 23 20:58:26 gitlab systemd-logind[165]: Session 18 logged out. Waiting for processes to exit.
Mar 23 20:58:26 gitlab systemd-logind[165]: Removed session 18.
░░ Subject: Session 18 has been terminated
░░ Defined-By: systemd
░░ Support: http://www.ubuntu.com/support
░░ Documentation: sd-login(3)
░░ 
░░ A session with the ID 18 has been terminated.
````
- These are the three places where logs will occur.  From testing, no other logging locations appeared to update.
