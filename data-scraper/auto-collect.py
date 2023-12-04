#!/usr/bin/python3

import socket
import requests
import shodan
import sys
from time import sleep
from colorama import Fore, Back, Style
from requests.exceptions import ConnectionError, Timeout, RequestException
from urllib3.exceptions import ConnectionError
from datetime import datetime

now = datetime.now()
date_time = now.strftime("%m-%d-%Y-%H:%M:%S")

# prints the banner
def banner():
    print(
        """
               ...                            
             ;::::;                           
           ;::::; :;                          
         ;:::::'   :;                         
        ;:::::;     ;.                        
       ,:::::'       ;           OOO\         
       ::::::;       ;          OOOOO\        
       ;:::::;       ;         OOOOOOOO       
      ,;::::::;     ;'         / OOOOOOO      
    ;:::::::::`. ,,,;.        /  / DOOOOOO    
  .';:::::::::::::::::;,     /  /     DOOOO   
 ,::::::;::::::;;;;::::;,   /  /        DOOO  
;`::::::`'::::::;;;::::: ,#/  /          DOOO 
:`:::::::`;::::::;;::: ;::#  /            DOOO
::`:::::::`;:::::::: ;::::# /              DOO
`:`:::::::`;:::::: ;::::::#/               DOO
 :::`:::::::`;; ;:::::::::##                OO
 ::::`:::::::`;::::::::;:::#                OO
 `:::::`::::::::::::;'`:;::#                O 
  `:::::`::::::::;' /  / `:#                  
   ::::::`:::::;'  /  /   `#              v.1.0.0
                                  Made by ice-wzl
    """
    )


def setup_api():
    """
    Function sets up the api key for use later on in the script. Will read from the file api.txt containing the key

    Return: returns back the api key in the variable name api
    """
    # should read api key from a file to prevent me from blundering my api key in a git commit
    with open("api.txt", "r") as fp:
        api_key = fp.read().strip()
        print("API key used: {}".format(api_key))
    api = shodan.Shodan(api_key)
    return api


def do_query(api, query):
    """
    Function takes in an api key and a query to perform. 
    Will conduct the query against shodan and print out only the ip addresses into a file called results.txt
    Has no return value 
    """
    # Perform the search
    query = "".join(query)
    print("Query {}".format(query))
    result = api.search(query)
    # Loop through the matches and print each IP
    # for service in result['matches']:
    with open("result.txt", "w+") as fp:
        for service in result["matches"]:
            fp.write(service["ip_str"] + "\n")


def get_tor_session():
    """
    Function has no input parameters. It will get up a tor session to make requests to webservers over tor vice your own ip

    Return: Returns back the session for use later on in the script
    """
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {"http": "socks5://127.0.0.1:9050"}
    return session


def do_request():
    """
    Function performs a sanity check against icanhazip.com to ensure you are not leaking your true public ip 
    Function with read from results.txt containing our ip addresses 
    It will iterate through all the results in the results.txt file and make a request to the ip on port 8000
    It will get the site content html content back and save it in variable site_content 
    It will check if the ip already exists in our history.txt file, by calling check_exist()
    If it is not in history.txt it will make a call to key_words() to check the html content for key words

    Return: none
    """
    # sets up tor socks port as default proxy
    session = get_tor_session()
    # Tor uses the 9050 port as the default socks port
    # Make a request through the Tor connection
    # IP visible through Tor
    try:
        sanity_check = session.get(
            "http://icanhazip.com", timeout=60, proxies=session.proxies
        )
        sanity_check = sanity_check.content
        sanity_decoded = sanity_check.decode()
        print("Your external IP: {}".format(sanity_decoded))
    except OSError:
        print(Fore.RED + "Tor is not running on your host")
        sys.exit(2)
    with open("result.txt", "r") as fp:
        read_in = fp.readlines()
        with requests.sessions.Session() as session:
            for ip in read_in:
                try:
                    # line below is redundant, should not be needed as it is already defined above 
                    session = get_tor_session()
                    response = session.get(
                        "http://{}:8000/".format(ip.strip()),
                        stream=True,
                        timeout=75,
                        proxies=session.proxies,
                    )
                    print(
                        Fore.RESET
                        + "Made request to {}, Status Code: {}".format(
                            ip.strip(), response.status_code
                        )
                    )

                    handle = open("session_history" + date_time, "a+")
                    handle.write("Made request to {}, Status Code: {}\n".format(
                            ip.strip(), response.status_code) + Fore.RESET)
                    handle.close()
                    
                    sleep(5.0)
                    # set the request content to a variable for parsing
                    site_content = response.content
                    # check here if our content has a interesting word in it
                    if not check_exist(ip):
                        # should check if the ip is in our hist file here before doing the keyword check, clutters output
                        key_words(site_content, ip)
                # many exceptions to try and handle gracefully
                except (ConnectionError, Timeout, RequestException):
                    print(Fore.RED + "{}, Host not responsive".format(ip.strip()))
                    
                    handle = open("session_history" + date_time, "a+")
                    handle.write(Fore.RED + "{}, Host not responsive\n".format(ip.strip()) + Fore.RESET)
                    handle.close()


def key_words(content, ip_addr):
    interesting_words = [
        b"exploit",
        b"hacking",
        b".ssh/",
        b"home/",
        b"/etc",
        b"/opt",
        b".aws/",
        b"id_rsa",
        b".viminfo",
        b".bash_history",
        b"passwd",
        b"shadow",
        b"nmap",
        b"nessus",
        b".python_history",
        b".wget-hsts",
        b".git/",
        b"root/",
        b"victim",
        b"sqlmap",
        b"0day",
        b"wireguard",
        b"wg/",
        b".wg-easy/",
        b"pt/",
        b"tools/",
        b"metasploit",
        b"sliver",
        b"havoc",
        b"cobalt_strike",
        b"cobalt-strike",
        b"cobalt",
        b"brute_ratel",
        b"brute",
        b"ratel",
        b"bruteforce",
        b"mrlapis",
        b"lockbit",
        b"revil",
        b"qbot",
        b"qakbot",
        b"malware",
        b"payload",
        b"crypter",
        b"ransom",
        b"ransomware",
        b"collect",
        b"log4j",
        b"nuclei"
        b"gorailgun",
        b"wormhole",
        b"gost",
        b"shellcode",
        b"redlinestealer"
    ]
    for i in interesting_words:
        if i in content:
            i = i.decode()
            print(Fore.GREEN + "\t{} found at {}".format(i, ip_addr.strip()))

            handle = open("session_history" + date_time, "a+")
            handle.write(Fore.GREEN + "\t{} found at {}\n".format(i, ip_addr.strip()) + Fore.RESET)
            handle.close()

    if b".ssh/" in content:
        crawl_ssh(ip_addr)


def crawl_ssh(ip_addr):
    interesting_words = [b"ecdsa", b"rsa", b"pub", b"dsa", b"ecdsa_sk", b"ed25519", b"ed25519_sk"]
    try:

        with requests.sessions.Session() as session:
            session = get_tor_session()
            response = session.get(
                "http://{}:8000/.ssh/".format(ip_addr.strip()),
                stream=True,
                timeout=75,
                proxies=session.proxies,
            )
            print(
                Fore.RESET
                + "Made request to {}, Status Code: {}".format(
                    ip_addr.strip(), response.status_code
                ))
            
            handle = open("session_history" + date_time, "a+")
            handle.write(Fore.RESET + "Made request to {}, Status Code: {}\n".format(ip_addr.strip(), response.status_code))
            handle.close()

            site_content = response.content
            # debugging line uncomment below 
            # print(site_content)
            for i in interesting_words:
                if i in site_content:
                    i = i.decode()
                    print(Fore.GREEN + "\t\t{} found at http://{}:8000/.ssh".format(i, ip_addr))
                    
                    handle = open("session_history" + date_time, "a+")
                    handle.write(Fore.GREEN + "\t\t{} found at http://{}:8000/.ssh\n".format(i, ip_addr))
                    handle.close()

    except (ConnectionError, Timeout, RequestException):
        print(Fore.RED + "{}, Host not responsive".format(ip_addr.strip()))


def check_exist(ip_addr):
    exists = 0
    with open("history.txt", "r") as fp:
        read_file = fp.readlines()
        for i in read_file:
            if i == ip_addr:
                exists = 1
        if exists == 1:
            print("\t{} is in our history file".format(ip_addr.strip("\n")))

            handle = open("session_history" + date_time, "a+")
            handle.write("\t{} is in our history file\n".format(ip_addr.strip("\n")))
            handle.close()
            
            return True
        else:
            # add_entry(ip_addr)
            with open("history.txt", "a") as np:
                np.write(ip_addr)




if __name__ == "__main__":
    # print the banner
    banner()
    # conduct the shodan query to get the results
    do_query(setup_api(), 'Title:"Directory listing for /" port:8000')
    # sleeps for 5 seconds, should not be needed, test if you can remove this 
    sleep(5.0)
    # perform the requests which will loop through the results in results.txt
    do_request()
