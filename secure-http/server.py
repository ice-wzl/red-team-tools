#!/usr/bin/python3
import socket
import argparse
import os
import hashlib
import string
import random
from termcolor import cprint

__author__ = "ice-wzl"
__version__ = "0.1.0"
__license__ = "MIT"

# TODO


def do_hashing(ifile):
    get_hash = hashlib.md5(open(ifile, "rb").read())
    get_final = get_hash.hexdigest()
    print("Sent encrypted file with MD5: {}".format(get_final))
    cprint(
        "*" * os.get_terminal_size()[0],
        "red",
        attrs=["bold"],
    )


def pastable():
    print("Run on the client (change the -b option to something that blends): ")
    cprint(
        "python3 client.py -i {} -p {} -f index.html -b decrypted\n".format(
            args.ipaddress, args.port
        ),
        "light_blue",
        attrs=["bold"],
    )


def do_encrypt(in_file, outfile):
    os.system("cp {} {}".format(in_file, outfile))
    do_enc = os.system(
        "openssl enc -aes-256-cbc -pbkdf2 -salt -pass pass:{} -in {} -out {}".format(
            password_generation(), in_file, outfile
        )
    )
    return do_enc


def password_generation(
    size=20, char=string.ascii_lowercase + string.ascii_uppercase + string.digits
):
    gen_pass = "".join(random.choice(char) for i in range(size))
    print("Your password to decrypt is: " + gen_pass)
    return gen_pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ipaddress", action="store", dest="ipaddress")
    parser.add_argument("-p", "--port", action="store", dest="port")
    parser.add_argument("-f", "--file", action="store", dest="file")

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )
    args = parser.parse_args()

    hammer = "\U0001F528"

    if not args.ipaddress or not args.port or not args.file:
        print(
            "Required arguments {-i <ip_address>, -p <port>, -f <file>}, try again..."
        )
    else:
        port = int(args.port)
        s = socket.socket()
        host = args.ipaddress
        try:
            s.bind((host, port))
            s.listen(5)
        except OSError as e:
            print(e)

        cprint(
            "{} Server hosting {} as index.html at {} on port {} {}\n".format(
                hammer, args.file, args.ipaddress, args.port, hammer
            ),
            attrs=["bold"],
        )
        pastable()

        while True:
            conn, addr = s.accept()
            print("Got connection from {}".format(addr))
            data = conn.recv(1024)
            if b"wK1NLC7DUO2N73E1AxGE" not in data:  # secret key to change
                conn.send(b"Invalid Connection")
            else:
                print("Recieved Key: {}".format(repr(data)))
                do_encrypt(args.file, "index.html")
                f = open("index.html", "rb")
                l = f.read(1024)
                while l:
                    conn.send(l)
                    l = f.read(1024)
                f.close()
                do_hashing("index.html")
                conn.close()
