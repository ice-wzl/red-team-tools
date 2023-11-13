#!/usr/bin/python3
import argparse 
import sys
"""
Small program to generate stack strings for use in malware development
"""

def main(to_convert, var_to_use):
    """
    Function to convert the user supplied variable and input string into a stack string for malware development 
    """
    stack_str = list(to_convert)
    print("char {}[] = {{ ".format(var_to_use), sep="", end='')
    for i in stack_str:
        if i != stack_str[-1]:
            print("'",i, "'", ",", end="", sep="")
        else:
            print("'",i, "'", end="", sep="")
    print(",'\\0' };",end='')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--string", action="store", help="The input string to convert to a stack string", dest="string")
    parser.add_argument("-v", "--variable", action="store", help="The variable name to use for this stack string", dest="variable")

    args = parser.parse_args()
    
    if not args.string or not args.variable:
        print("Required:")
        print("-s <string>\r\n-v <variable name>")
        print("python3 {} --help".format(sys.argv[0]))
        sys.exit(1)

    main(args.string, args.variable)
