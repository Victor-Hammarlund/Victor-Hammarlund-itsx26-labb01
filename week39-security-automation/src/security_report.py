#!/bin/env python
from pathlib import Path
import os
import sys
# Variables
# ----------------------------------------#
pathSuspicious="../data/week39_dataset_basic/suspicious_ips.txt"
pathAccess = "../data/week39_dataset_basic/access.log"
pathAuth = "../data/week39_dataset_basic/auth.log"
pathFirewall = "../data/week39_dataset_basic/firewall.log"
pathOutput = "../output/security_report.txt"
paths = {pathAccess : "access", pathAuth: "Authentication", pathFirewall:"firewall"}

# ----------------------------------------#
#/////////////////////////////////////////#
#               Functions                 #
#/////////////////////////////////////////#
def getSuspiciousIps():
    ips=[]
    with open(pathSuspicious, "r", encoding="utf-8") as badIps:
        for i in badIps:
            ips.append(i.strip())
    return ips
# ----------------------------------------#
def getLog(path, name):

    skippedLines =0
    #print(f"Getting {name} logs ... ")
    logs=[]
    with open(path,"r",encoding="utf-8") as logIps:
        for line in logIps:
            fields=line.split()
            source = [f for f in fields if f.startswith("src=")]
            if not source:
                skippedLines+=1
                continue
            logs.append(source[0].split("=", 1)[1])
    if skippedLines >= 1:
        logs.append(f"skipped {skippedLines} line(s). Missing src field")
    return logs

# ----------------------------------------#
def getBadActionFields(fileName, ioc_list):
    def getBadActionFields(fileName, ioc_list):
        for path, name in paths.items():
            if name == fileName:

                suspicious = []

                with open(path, "r", encoding="utf-8") as log:
                    for line in log:

                        # auth.log
                        if fileName == "Authentication":
                            if "Failed" in line:
                                for ip in ioc_list:
                                    if ip in line:
                                        suspicious.append(ip)

                        # access.log
                        elif fileName == "access":
                            if "status=401" in line:
                                for ip in ioc_list:
                                    if ip in line:
                                        suspicious.append(ip)

                        # firewall.log
                        elif fileName == "firewall":
                            if "DENY" in line or "DROP" in line:
                                for ip in ioc_list:
                                    if ip in line:
                                        suspicious.append(ip)

                counts = occurance(ioc_list, suspicious)

                if not counts:
                    return f"No IOC activity found in {fileName}"

                result = []

                if fileName == "Authentication":
                    for ip, count in counts.items():
                        result.append(
                            f"{ip}: {count} failed login attempt(s)"
                        )

                elif fileName == "access":
                    for ip, count in counts.items():
                        result.append(
                            f"{ip}: {count} unauthorized request(s)"
                        )

                elif fileName == "firewall":
                    for ip, count in counts.items():
                        result.append(
                            f"{ip}: {count} denied/dropped connection(s)"
                        )

                return "\n".join(result)

    return f"File '{fileName}' not found"
                    
    
    #ip failed to login x times as: [user1,user2,user3,user n ...]
# ----------------------------------------#

def writeReport(fileName,loggedIps,badIps, IOC):
    str_conclusion = ""
    if IOC < 1:
        str_conclusion += f"No IP from IOC-list logged in the {fileName} logs"
    else:
        str_conclusion += f"IP-adresses listed in the IOC dataset occur in this log\n+and might need further investigation"
    
    with open(pathOutput, "a", encoding="utf-8") as out:
        output = (f'''╔═════════════════════════════════════════════════════╗\n
                \n║SECURITY REPORT                                      ║
                \nFile Analized: {fileName}                                     \n
                \nThese IP's are logged\n --------------------\n {loggedIps}\n
                \nPossible IOC's\n --------------------\n {getBadActionFields(fileName,getSuspiciousIps() )}\n
                \n --------------------
                \nObservation:
                \nNumber of IP's that match the IOC list: {IOC}
                \n --------------------
                \nConclusion:
                \n{str_conclusion}
                \n --------------------
                \n
                \n╚═════════════════════════════════════════════════════╝''')
        out.write(f"{output}\n")     
       # print(f"\n{getBadActionFields(fileName,getSuspiciousIps() )}\n")
# ----------------------------------------#

def clearOutputFile():
    print("Clearing output file . . .")
    with open(pathOutput, "w") as clear:
        clear.write("")

# ----------------------------------------#

def occurance(ioc,_list):
    matches= {}
    for i in _list:
        if i in ioc:
            if i not in matches:
                matches[i] = 0
            matches[i] +=1
    return matches
  
# ----------------------------------------#
def checkStructure():

    missingPaths =0
    print("Beginning structure control")
    
    # Check dataset paths
    for i in paths:
        check = Path(i)
        if check.exists():
            print(f"File exists : {i}")
        else:
            print(f"Missing path or file. Expected path : {i}")
            missingPaths +=1
            
            
    
    sus = Path(pathSuspicious)
    if sus.exists():
        print(f"File exists : {pathSuspicious}")
    else:
        print(f"Missing path or file. Expected path : {pathSuspicious}")
        missingPaths += 1 

    # Check outputfile
    attempts  = 0
    while True:

        output = Path(pathOutput)
        if output.exists():
            print(f"File exists : {pathOutput}")
            break
        else:
            print(f"Missing path or file. Expected path : {pathOutput}")
            print(f"Attempting creation of {pathOutput}")
            try:
                with open(pathOutput, "w") as file:
                    pass
            except FileExistsError:
                print(f"File {pathOutput} already exists ... ")
            except PermissionError:
                print(f"Insufficient permission while trying to create {pathOutput}")
            except Exception as e:
                print(f"Error occured: {e}")
            attempts +=1
            if attempts >= 3:
                sys.exit(f"Failed to create {pathOutput}\nExiting . . .")

    if missingPaths >= 1:
        sys.exit("Paths are missing or mislocated\nExiting ...")
       


# ----------------------------------------#
    
# ----------------------------------------#

#/////////////////////////////////////////#
#                 Main                    #
#/////////////////////////////////////////#
def main():
    checkStructure()
    clearOutputFile()
    print("Starting Security Report!\n")
    badIps = getSuspiciousIps()

    for path, name in paths.items():
        formatedBadIps=""
        formatedIPs = ""
        ips=getLog(path, name)
        match_ips = occurance(badIps, ips)

        for x, y in match_ips.items():
            formatedBadIps+=f"{x} : occurs {y} times\n "
        
        for ip in ips:
            formatedIPs+=f" {ip}\n "
        writeReport(name,formatedIPs, formatedBadIps, len(match_ips))
        
        
    
    
    
    

#/////////////////////////////////////////#
#                   Run                   #
#/////////////////////////////////////////#
main()

#if not source:
#skipped += 1
#continue
#Show more lines
#
#och sedan rapportera:
#
#Plain Text
#Skipped rows: 3 (missing src field)
'''
Observation:
2 IP-adresser matchade IOC-listan.

Conclusion:
Dessa adresser förekommer i loggarna och bör granskas vidare.

Uncertainty:
Datasetet visar endast förekomst och bekräftar inte skadlig aktivitet.

Security significance:
Matchningen kan hjälpa till att prioritera fortsatt analys.
'''

