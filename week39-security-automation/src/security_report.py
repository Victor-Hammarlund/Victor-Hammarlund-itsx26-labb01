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
pathNoHits = "../data/week39_dataset_basic/no_hits.log"
paths = {pathAccess : "access", pathAuth: "Authentication", pathFirewall:"firewall", pathNoHits: "noHits"}

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
def getLog(path):

    skippedLines =0
    
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
        for path, name in paths.items():
            if name == fileName:
                
                suspicious = []
                unknown = []

                with open(path, "r", encoding="utf-8") as log:
                    for line in log:

                        # auth.log
                        if fileName == "Authentication":
                            if "Failed" in line:
                               source = [f for f in line.split() if f.startswith("src=")]
                            if source:
                                ip = source[0].split("=", 1)[1]

                                if ip in ioc_list:
                                    suspicious.append(ip)
                                elif ip not in unknown:
                                    unknown.append(ip)
                                
                                   
                                

                        # access.log
                        elif fileName == "access" or fileName == "noHits":
                            if "status=401" in line:
                               source = [f for f in line.split() if f.startswith("src=")]
                            if source:
                                ip = source[0].split("=", 1)[1]

                                if ip in ioc_list:
                                    suspicious.append(ip)
                                elif ip not in unknown:
                                    unknown.append(ip)

                        # firewall.log
                        elif fileName == "firewall":
                            if "DENY" in line or "DROP" in line:
                               source = [f for f in line.split() if f.startswith("src=")]
                               if source:
                                    ip = source[0].split("=", 1)[1]

                                    if ip in ioc_list:
                                        suspicious.append(ip)
                                    elif ip not in unknown:
                                        unknown.append(ip)
                            
                                

                counts = occurance(ioc_list, suspicious)
              
                    
                result = []
                if not counts:
                    if len(unknown) >=1:
                        return f"No IOC-IPs present\nbut there were failed attempt(s) from:\n{"\n".join(unknown)}"    
                    return f"No IOC activity found in {fileName}"
            
                

                if fileName == "Authentication":
                    for ip, count in counts.items():
                        result.append(
                            f"{ip}: {count} failed login attempt(s)"
                        )

                elif fileName == "access" or fileName == "noHits":
                    for ip, count in counts.items():
                        result.append(
                            f"{ip}: {count} unauthorized request(s)"
                        )

                elif fileName == "firewall":
                    for ip, count in counts.items():
                        result.append(
                            f"{ip}: {count} denied/dropped connection(s)"
                        )

                return f"{"\n".join(result)}\nNon IOC failed attempt(s)\n{len(unknown)}\n{"\n".join(unknown)}"
            



        return f"File '{fileName}' not found"
                    
    
    #ip failed to login x times as: [user1,user2,user3,user n ...]

# ----------------------------------------#

def patternMatching(ioc_ips):
    pattern = []
    for ioc in ioc_ips:
         result = []
         match =0
         for path, name in paths.items():
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    if ioc in line:
                        match += 1
            result.append(f"{name}: {match} times")
         pattern.append(f"{ioc} occurs in following logs:\n\t{"\n\t".join(result)}\n")
                
    return pattern

    

# ----------------------------------------#


def writeReport(fileName,loggedIps,badIps, IOC):
    str_conclusion = ""
    if IOC < 1:
        str_conclusion += f"No IP from IOC-list logged in the {fileName} logs.\nBut may still contain unautharized attempts"
    else:
        str_conclusion += f"IP-adresses listed in the suspicious dataset occur in this log\nand might need further investigation"
    
    with open(pathOutput, "a", encoding="utf-8") as out:
        output = (f'''╔═════════════════════════════════════════════════════╗\n
                \n║SECURITY REPORT                                      ║
                \nFile Analized: {fileName}                                     \n
                \nThese IP's are logged\n --------------------\n{loggedIps}\n
                \nPossible IOC's\n --------------------\n{getBadActionFields(fileName,getSuspiciousIps() )}
                \n --------------------
                \nObservation:
                \nTimes IOC-IPs occur in the log: {IOC}
                \n --------------------
                \nConclusion:
                \n{str_conclusion}
                \n --------------------
                \n╚═════════════════════════════════════════════════════╝''')
        out.write(f"{output}\n")     
    
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

def summary(badIps):
    with open(pathOutput, "a") as result:
            pattern = patternMatching(badIps)
            output = (f'''
            \n╔═════════════════════════════════════════════════════╗\n
            \nSUMMARY
            \n
            \n{"\n".join(pattern)}
            \n╚═════════════════════════════════════════════════════╝''')
            result.write(output)
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
                with open(pathOutput, "a") as file:
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
        ips=getLog(path)
        match_ips = occurance(badIps, ips)

        for x, y in match_ips.items():
            formatedBadIps+=f"{x} : occurs {y} times\n "
        
        for ip in ips:
            formatedIPs+=f" {ip}\n "
        writeReport(name,formatedIPs, formatedBadIps, len(match_ips))
    summary(badIps)

        
        
    
    
    
    

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

