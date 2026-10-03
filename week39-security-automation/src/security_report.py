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
# Read and return suspicious IP-address list
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
    # Open log file
    with open(path,"r",encoding="utf-8") as logIps:
    # Scan entire log file after source addresses
        for line in logIps:
            fields=line.split()
            source = [f for f in fields if f.startswith("src=")]
            # Note lines missing a source field
            if not source:
                skippedLines+=1
                continue
            logs.append(source[0].split("=", 1)[1])
    # Append the amount of skipped lines to logs
    if skippedLines >= 1:
        logs.append(f"skipped {skippedLines} line(s). Missing src field")
    return logs

# ----------------------------------------#

# Return status and occurance count of IP-address
def getBadActionFields(fileName, ioc_list):
        # Loop through all log files
        for path, name in paths.items():
            if name == fileName:
                
                suspicious = []
                unknown = []
                # Open logfile in read mode
                with open(path, "r", encoding="utf-8") as log:
                    for line in log:

                        # auth.log
                        if fileName == "Authentication":
                            # Append suspicious source address that failed to login to list
                            if "Failed" in line:
                               print(f"LINE\n{line}\n")#Troubleshooting
                               source = [f for f in line.split() if f.startswith("src=")]
                               if source:
                                ip = source[0].split("=", 1)[1]
                                print(f"IP TO ADD\n{ip}\n")#Troubleshooting
                                if ip in ioc_list:
                                    suspicious.append(ip)
                                # If ip failed to login but is not listed as ioc append to unknown
                                elif ip not in unknown:
                                    unknown.append(ip)
                                                                  


                        # access.log
                        elif fileName == "access" or fileName == "noHits":
                            # Append addresses that made an unauthorized access attempt
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
                            # Append addresses that were dropped or denied by the firewall
                            if "DENY" in line or "DROP" in line:
                               source = [f for f in line.split() if f.startswith("src=")]
                               if source:
                                    ip = source[0].split("=", 1)[1]

                                    if ip in ioc_list:
                                        suspicious.append(ip)
                                    elif ip not in unknown:
                                            unknown.append(ip)
                            
                                
                # organize and count occurances of each suspicious ip
                counts = occurance(ioc_list, suspicious)
              
                    
                result = []
                if not counts:
                    if len(unknown) >=1:
                        return f"No IOC-IPs present\nbut there were failed attempt(s) from:\n{"\n".join(unknown)}"    
                    return f"No IOC activity found in {fileName}"
            
                
                # Now create a list of the addresses with occurance count, then format it for report 
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

                # Return formated strings and failed attempts from unknown addresses
                return f"{"\n".join(result)}\nNon IOC failed attempt(s)\n{len(unknown)}\n{"\n".join(unknown)}"
            


        # Unexpected file names are handled
        return f"File '{fileName}' not found"
                    
    
    #ip failed to login x times as: [user1,user2,user3,user n ...]

# ----------------------------------------#

# Summerize which logs a ip appears in
def patternMatching(ioc_ips):
    pattern = []

   # Itterate through all the items in the given parameter (suspicious IP-addresses)
    for ioc in ioc_ips:
         result = []
         match =0
         # Add 1 for every match in file
         for path, name in paths.items():
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    if ioc in line:
                        match += 1
            result.append(f"{name}: {match} times")
            # Reset for next file
            match = 0
         # Append a formated string with matches to list
         pattern.append(f"{ioc} occurs in following logs:\n\t{"\n\t".join(result)}\n")
                
    return pattern

    

# ----------------------------------------#


def writeReport(fileName,loggedIps,badIps, IOC):
    str_conclusion = ""
    str_observation = ""
    if IOC < 1:
        str_conclusion += f"No IP from IOC-list logged in the {fileName} logs.\nBut may still contain unautharized attempts"
    else:
        str_conclusion += f"IP-adresses listed in the\nsuspicious dataset occur in this log\nand might need further investigation"

    if IOC >=1:
        str_observation = f"There are {IOC} suspicious IP address(es) that occur\nin this logfile:\n{badIps}"
    else:
        str_observation = f"There are no source addresses\nin this log that match\nwith the list of suspicious addresses"

    
    with open(pathOutput, "a", encoding="utf-8") as out:
        output = (f'''╔═════════════════════════════════════════════════════╗\n
                \n║SECURITY REPORT                                      ║
                \nFile Analized: {fileName} log                                    
                \nThese IP's are logged\n########################\n{loggedIps}
                \nPossible IOC's\n########################\n{getBadActionFields(fileName,getSuspiciousIps() )}
                \nObservation:\n########################
                \n{str_observation}
                \nConclusion:\n########################
                \n{str_conclusion}
                \n
                \nUncertainty:\n########################
                \nA non IOC labeled failed attempt does not\nequal that it is safe or dangerous,\ncould be worth looking into.
                \n╚═════════════════════════════════════════════════════╝''')
        out.write(f"{output}\n")     
    
# ----------------------------------------#
# Logic for clearing the output file for new report generation
def clearOutputFile():
    print("Clearing output file . . .")
    with open(pathOutput, "w") as clear:
        clear.write("")

# ----------------------------------------#
# Return dictionary of suspicious IP-address and their occurance count
def occurance(ioc,logFile):
    matches= {}
    for i in logFile:
        if i in ioc:
            if i not in matches:
                matches[i] = 0
            matches[i] +=1
    return matches

# ----------------------------------------#

# Write summary
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

    # Counter for missing paths
    missingPaths =0
    print("Beginning structure control")
    
    # Check dataset paths
    for i in paths:
        check = Path(i)
        if check.exists():
            print(f"File exists : {i}")
        # Notify if path is missing
        else:
            print(f"Missing path or file. Expected path : {i}")
            missingPaths +=1
            
            
    # Check for expected file path to suspicious IP-addresses
    sus = Path(pathSuspicious)
    if sus.exists():
        print(f"File exists : {pathSuspicious}")
    # Notify if path is missing
    else:
        print(f"Missing path or file. Expected path : {pathSuspicious}")
        missingPaths += 1 

    # Check outputfile
    attempts  = 0
    while True:

        output = Path(pathOutput)
        # Check if file exist at expected path
        if output.exists():
            print(f"File exists : {pathOutput}")
            break
        # Attempt to create file and handle exceptions
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

    # Close program if any expected log file is missing
    if missingPaths >= 1:
        sys.exit("Paths are missing or mislocated\nExiting ...")
       


# ----------------------------------------#
    
# ----------------------------------------#

#/////////////////////////////////////////#
#                 Main                    #
#/////////////////////////////////////////#
def main():
    checkStructure()
    # Reset the report
    clearOutputFile()
    
    print("Starting Security Report!\n")
    badIps = getSuspiciousIps()

    # loop through each declared log file 
    # name = shorter name for log file
    for path, name in paths.items():
        # Strings to be used as arguments in writeReport()
        formatedBadIps=""
        formatedIPs = ""
        
        # Get occurance of each ip in log file 
        ips=getLog(path)
        match_ips = occurance(badIps, ips)

        # Format descriptive string for report
        for x, y in match_ips.items():
            formatedBadIps+=f"{x} : occurs {y} times\n"
        
        for ip in ips:
            formatedIPs+=f"{ip}\n"
        
        writeReport(name,formatedIPs, formatedBadIps, len(match_ips))
    # Append summary to end of report
    summary(badIps)

        
        
    
    
    
    

#/////////////////////////////////////////#
#                   Run                   #
#/////////////////////////////////////////#
main()