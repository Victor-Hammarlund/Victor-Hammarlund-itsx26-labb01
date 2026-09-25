
#!/bin/env python

dataSetA ="../Data/suspicious_ips.txt"
dataSetB ="../Data/access.log"
skipped=0
ip_counts = {}
failed_count = 0
matches = {}
bad_ips= []
with open(dataSetA, encoding="utf-8") as ip_file:
    for line in ip_file:
        bad_ips.append(line.strip())

matches = {}

with open(dataSetB, encoding="utf-8") as log_file:
    print("-logged ips:-")
    for line in log_file:
        if "Failed login" in line:
            failed_count += 1
            #print(line.strip())

        fields = line.split()
        source_fields = [f for f in fields if f.startswith("src=")]
        if not source_fields:
           skipped += 1
           continue
        ip_address = source_fields[0].split("=", 1)[1]
        if ip_address in bad_ips:

            if ip_address not in matches:
                matches[ip_address] = 0

            matches[ip_address] += 1
        print(f"{ip_address}")
        

print("WARN Suspicious ips occur in login logs")
for ip_address, count in sorted(matches.items()):
    print(f"{ip_address}: {count}")



