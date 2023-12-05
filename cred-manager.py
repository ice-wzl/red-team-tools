#!/usr/bin/python3

import os
import sys
import sqlite3
from termcolor import cprint
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style

# get the directory the user wants to create the db in
db_created = False
while db_created == False:
    databse_pass = input(
        "Enter absolute path for storage.db file {/home/user/Documents}: "
    )
    try:
        # see if we were given a valid directory or not
        os.chdir(databse_pass)
        # if we were then create the storage.db file
        conn = sqlite3.connect("storage.db")
        cursor = conn.cursor()
        db_created = True
    # if we were not then give them the error that it isnt valid and loop
    except FileNotFoundError as e:
        print(e)

style = Style.from_dict(
    {
        # User input (default text).
        "": "#ff0066",
        # Prompt.
        "host": "#BBEEFF",
        "arrow": "#00ffff",
    }
)
# what the prompt is going to look like localhost -->
message = [
    ("class:host", "localhost"),
    ("class:arrow", "--> "),
]

# create the prompt suggester
html_completer = WordCompleter(["view", "create", "delete", "delrow", "add", "exit"])


def banner():
    print(
        """
   ,   ,
  /////|
 ///// |
|~~~|  |
|===|  |
|   |  |
|   |  | -ice-wzl
|   | /  -cred-manger v1.0.1
|===|/
'---'
    """
    )


def do_view():
    # created table will have a file size of 1, check that it is 1 or greater, if less let them know they have to
    # create the table first
    if os.stat("storage.db")[6] <= 1:
        print("Nothing created yet...create first")
    else:
        # easy select * from table
        print("Data in Table:")
        print("*" * os.get_terminal_size()[0])
        data = cursor.execute("""SELECT * FROM TARGETS""")
        for row in data:
            print(row)
            print("*" * os.get_terminal_size()[0])

def do_add():
    # check that the table has been created if not let them know
    if os.stat("storage.db")[6] == 0:
        print("Nothing created yet...create first")
    else:
        # take in a unique id for the primary key, what we will use to delete rows if they so choose later on
        ID = input("Enter unique ID: ")
        IPADDR = input("Enter IP Address: ")
        USERNAME = input("Enter Username: ")
        PASSWORD = input("Enter Password: ")
        try:
            cursor.execute(
                """INSERT INTO TARGETS VALUES("%s", "%s", "%s", "%s")"""
                % (ID, IPADDR, USERNAME, PASSWORD)
            )
            conn.commit()
        # need to check that our primary key is actually unique
        except sqlite3.IntegrityError as e:
            print("Unique ID already exists")


def do_create():
    # ensure the targets table hasnt already been created
    if os.stat("storage.db")[6] > 1:
        print("Table already created")
    else:
        try:
            # our table create query
            table = """CREATE TABLE TARGETS(ID INTEGER PRIMARY KEY, IP VARCHAR(255), USERNAME VARCHAR(255), PASSWORD VARCHAR(255));"""
            cursor.execute(table)
            print("Table Created")
        except:
            print("Something went wrong, does your path exist...?")


def do_delrow():
    # again error checking the table is created
    if os.stat("storage.db")[6] <= 1:
        print("Nothing created yet...create first")
    else:
        # delete row off the primary key which is the unique ID
        ID = input("Enter unique ID to delete: ")
        cursor.execute("""DELETE FROM TARGETS WHERE ID = %s""" % (ID))
        conn.commit()

if __name__ == '__main__':
    banner()
    while True:
        # set up our prompt from prompt_toolkit
        session = PromptSession()
        options = session.prompt(message=message, style=style, completer=html_completer)
        options = options.lower()
        options = options.rstrip()
        if options == "view":
            do_view()
        elif options == "add":
            do_add()
        elif options == "exit":
            conn.close()
            sys.exit(1)
        elif options == "delete":
            os.system('echo "" > storage.db')
            print("storage.db cleared...")
        elif options == "create":
            do_create()
        elif options == "delrow":
            do_delrow()
        else:
            # if something crazy is entered at the prompt, give the user the command options
            cprint("{create | view | add | delete | delrow | exit}", "blue", attrs=["bold"])
