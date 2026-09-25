#!/bin/env python

#failed_count = 0
#with open("../Data/newLog.log", encoding="utf-8") as log_file:
#    for line in log_file:
#        if "Permission denied" in line:
#            failed_count += 1
#            print(line.strip())
#
#
#print(f"Permission denied: {failed_count}")



def _passwordChecker_(losenfras):
    variation = 0
    if any(c.islower() for c in losenfras):
        variation += 1
    if any(c.isupper() for c in losenfras):
        variation += 1
    if any(c.isdigit() for c in losenfras):
        variation += 1
    if any(not c.isalnum() for c in losenfras):
        variation += 1
    langd = len(losenfras)
    if langd >= 12 and variation >= 3:
        return "stark"
    elif langd >= 8 and variation >= 2:
        return "medel"
    else:
        return "svag"
print(_passwordChecker_(input("Enter Password:")))
