#!/bin/env python

# Variables
# ----------------------------------------#
pathSuspicious="../data/week39_dataset_basic/suspicious_ips.txt"
pathAccess = "../data/week39_dataset_basic/access.log"
pathAuth = "../data/week39_dataset_basic/auth.log"
pathFirewall = "../data/week39_dataset_basic/firewall.log"
paths = {pathAccess : "access", pathAuth: "Authentication", pathFirewall:"firewall"}
skips = 0
# ----------------------------------------#
#/////////////////////////////////////////#
#               Functions                 #
#/////////////////////////////////////////#
def getSuspiciousIps():
    ips=[]
    with open(pathSuspicious, "r", encoding="utf-8") as badIps:
        for i in badIps:
            ips.append(i.strip())
        badIps.close
    return ips
# ----------------------------------------#
def getLog(path, name):
    skippedLines =0
    print(f"Getting {name} logs ... ")
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
        print(f"skipped {skippedLines} lines. Missing src field")
    return logs
            
# ----------------------------------------#

def writeReport(file,loggedIps,badIps):
    print(f"╔═════════════════════════════════════════════════════╗\n║SECURITY REPORT                                      ║\n File Analized: {file}                                     \n These IP's are logged\n --------------------\n {loggedIps}\n Possible IOC's\n --------------------\n {badIps}\n╚═════════════════════════════════════════════════════╝")
# ----------------------------------------#
def occurance(ioc,file):
    matches= {}
    for i in file:
        if i in ioc:
            if i not in matches:
                matches[i] = 0
            matches[i] +=1
    return matches



#/////////////////////////////////////////#
#                 Main                    #
#/////////////////////////////////////////#
def main():
    print("Starting Security Report!\n")
    badIps = getSuspiciousIps()

    for path, name in paths.items():
        formatedBadIps=""
        formatedIPs = ""
        ips=getLog(path, name)
        occurances = occurance(badIps, ips)

        for x, y in occurances.items():
            formatedBadIps+=f"{x} : occurs {y} times\n "
        
        for ip in ips:
            formatedIPs+=f" {ip}\n "
        writeReport(name,formatedIPs, formatedBadIps)
        
        
    
    
    
    

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