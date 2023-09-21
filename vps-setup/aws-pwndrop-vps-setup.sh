#!/bin/bash

#recommend you run this script set your secret path and redirect path before opening your ports to the internet 
#post install your certs will just be the default self signed ones 
#for downloads:
	#curl --insecure 
	#wget --no-check-certificates 

#to use your own certs 
	#place your own certs public.crt and private.key in /usr/local/pwndrop/data/ PRE-INSTALL!!


UID=`id | cut -d "=" -f2 | cut -d ")" -f1`
#root check 
if [ $UID == 0 ]
then 
        echo "You are root, script continuing"
        #stop the popup about restarting services
        export DEBIAN_FRONTEND=noninteractive
        
        apt-get update && apt-get upgrade -y
        apt autoremove -y  

        #ufw configure and turn on 
        echo "y" | ufw enable
        ufw allow ssh
        ufw allow https

        #need this in your hosts file before you stop resolved or else bad things happen
        sed -i /etc/hosts -e "s/^127.0.0.1 localhost$/127.0.0.1 localhost $(hostname)/"
        #get pwndrop installer and bash pipe, code is fine
        curl https://raw.githubusercontent.com/kgretzky/pwndrop/master/install_linux.sh | bash

        #kill aws resolved, interferes with pwndrop dns
        systemctl stop systemd-resolved

else
        echo "You are not root, please run with root permissions"
        exit 1 
fi


