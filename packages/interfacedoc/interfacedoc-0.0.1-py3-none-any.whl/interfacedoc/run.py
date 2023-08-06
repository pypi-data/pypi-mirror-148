#!python3

from interfacedoc import InterfaceInstaller
import os
import sys

# python3 interface startproject <str:project_name>

def start():
    command = sys.argv

    if len(command) >= 3:

        if command[1] == "startproject":

            installer = InterfaceInstaller(path=os.getcwd(), project_name=command[2])
            installer.run()
            
        else:
            print("command not found")
    else:
        print("command invalid")