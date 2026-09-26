#!/bin/env python
import datetime as dt
from datetime import date
import os
# misc Variables
dateNow = dt.datetime
birthDay = date(2027, 8, 28)
name = input()
commands = ["ls", "cd", "mkdir","sudo","rm"]
dangerousUser = ["root", "admin"]
user = os.getlogin()
time = dateNow.now()
#-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_

def main():
    
    if (time.hour >= 0 and time.hour <= 6):

        print("Nattinloggning-Ovanligt!")

    for username in dangerousUser:
        if username == user.lower():
            print("WARN : this is an unsafe username")
            exit(1)
    
    print("\nOK : this username is ok\n")

    print("LIST OF COMMON COMMANDS: \n")
    for command in commands:
        print(command)
    print("")

    print(f"[{dateNow.now()}] Hej! jag heter {name}\n")


    #open("./demo_mål.txt") as textFile
   

    delta = (birthDay - date.today())
    print(f"days until my birthday:{delta.days}")
   #-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_






main()
