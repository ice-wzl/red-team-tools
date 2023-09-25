#!/usr/bin/python3
import os
import pyperclip
from termcolor import cprint

while True:
    buffer_wait = pyperclip.waitForNewPaste()
    cprint("-" * os.get_terminal_size()[0], "red")
    print(buffer_wait.strip())
