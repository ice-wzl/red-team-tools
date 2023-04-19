#!/usr/bin/python3

import os
import sys
import sqlite3 
from termcolor import cprint
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts.progress_bar import formatters

conn = sqlite3.connect('storage.db')
cursor = conn.cursor()


style = Style.from_dict({
    # User input (default text).
        '':          '#ff0066',
    # Prompt.
        'host':     '#BBEEFF',
        'arrow':     '#00ffff',
    })
message = [
    ('class:host',     'localhost'),
    ('class:arrow',    '--> '),
    ]

#create the prompt suggester
html_completer = WordCompleter(['view', 'create', 'delete', 'delrow', 'add', 'exit'])

def banner():
    print("""
   ,   ,
  /////|
 ///// |
|~~~|  |
|===|  |
|j  |  |
| g |  | -ice-wzl
|  t| /  -cred-manger v1.0
|===|/
'---'
    """)


def do_view():
    if os.stat('storage.db')[6] <= 1:
        print("Nothing created yet...create first")
    else:
        print("Data in Table:")
        data = cursor.execute('''SELECT * FROM TARGETS''')
        for row in data:
            print(row)

def do_add():
    if os.stat('storage.db')[6] == 0:
        print("Nothing created yet...create first")
    else:
        ID = input("Enter unique ID: ")
        IPADDR = input("Enter IP Address: ")
        USERNAME = input("Enter Username: ")
        PASSWORD = input("Enter Password: ")
        try:
            cursor.execute('''INSERT INTO TARGETS VALUES("%s", "%s", "%s", "%s")''' % (ID, IPADDR, USERNAME, PASSWORD))
            conn.commit()
        except sqlite3.IntegrityError as e:
            print("Unique ID already exists")

def do_create():
    if os.stat("storage.db")[6] > 1:
        print("Table already created")
    else:
        table = '''CREATE TABLE TARGETS(ID INTEGER PRIMARY KEY, IP VARCHAR(255), USERNAME VARCHAR(255), PASSWORD VARCHAR(255));'''
        cursor.execute(table)
        print("Table Created")

def do_delrow():
    if os.stat('storage.db')[6] <= 1:
        print("Nothing created yet...create first")
    else:
        ID = input("Enter unique ID to delete: ")
        cursor.execute("""DELETE FROM TARGETS WHERE ID = %s""" % (ID))
        conn.commit()    
banner()
while True:
    session = PromptSession()
    options = session.prompt(message=message, style=style, completer=html_completer)
    options = options.lower()
    options = options.rstrip()
    if options == "view":
        do_view()
    elif options == "add":
        do_add()
    elif options == "exit":
        sys.exit(1)
    elif options == "delete":
        os.system('echo "" > storage.db')
        print("storage.db cleared...")
    elif options == "create":
        do_create()
    elif options == "delrow":
        do_delrow()
    else:
        cprint("{create | view | add | delete | delrow | exit}", "blue", attrs=['bold'])

conn.close()

