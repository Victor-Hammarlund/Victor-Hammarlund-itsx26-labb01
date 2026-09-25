#!/bin/env pyhton
def write_report(matches, failed_logins, skipped, output_path):
    limitation_text = (
    "Only source IP addresses were analyzed."
    )
    report_lines = [
    "ITSX26 SECURITY REPORT",
    f"Failed logins: {failed_logins}",
    f"IOC matches: {len(matches)}",
    f"Malformed lines skipped: {skipped}",
    "",
    "LIMITATION",
    limitation_text
    ]
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

def load_indicators(path):

    bad_ips = []
    with open(path, encoding="utf-8") as ip_file:
        for line in ip_file:
            bad_ips.append(line.strip())
    return bad_ips
def analyze_access_log(path,indicators):
    matches = {}
    with open(path, encoding="utf-8") as logfile:
        for line in logfile:
            words = line.split()
            source_fields = [
            f for f in words
            if f.startswith("src=")
            ]   
    if source_fields:
        ip_address = source_fields[0].split("=", 1)[1]
    if ip_address in bad_ips:
        if ip_address not in matches:
            matches[ip_address] = 0
        matches[ip_address] += 1
    return matches
def write_report(results,path):
    with open(path, "w", encoding="utf-8") as report:
        for ip, count in matches.items():
            report.write(f"{ip}:")
def main():
    bad_ips = load_indicators("../Data/suspicious_ips.txt")
    matches, failed_logins, skipped = analyze_access_log(
    "../Data/access.log",
    bad_ips
    )
    write_report(
    matches,
    failed_logins,
    skipped,
    "../output/securityreport.txt"
    )
