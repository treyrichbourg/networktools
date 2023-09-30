#! /home/trichbourg/Python/nornir/bin/python3
import os
import re
import csv
from pathlib import Path
from datetime import datetime
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F

# Using my own function for setting credentials from an encrypted keyring
from Tools import set_creds_default


"""
Script to query 802.1x authentication status of wired clients and write output.
-TR 9/28/2023
"""

output_dir: str = "/path/to/output/dir"
p: os.PathLike = Path(output_dir)


# Define task sent to hosts
# This task will scrape the status of 802.1x sessions on wired clients
def query_auth(task):
    command = "sh authentication sessions all"
    task = task.filter(F(has_parent_group="switches"))
    task = task.filter(role="access")
    set_creds_default(task)
    r = task.run(netmiko_send_command, command_string=command)
    return r


"""
Unpack and parse Nornir AggregateResult for any wired clients
that do NOT have the status of AUTHENTICATED.
Add results to a dictionary.
Key = Hostname
Value = scraped data for the unauthenticated client
"""


def parse_result(result):
    data = {}
    for hostname in result:
        pattern = "AUTHENTICATED"
        output = str(result[hostname][0])
        match_auth = re.search(pattern, output, re.MULTILINE)
        if match_auth:
            not_authenticated = []
            output = output.split("\n")
            for i in range(5, len(output)):
                line = output[i]
                auth = re.search(pattern, str(line))
                if not auth:
                    line = re.split(r"\s+", line)
                    not_authenticated.append(line)
            data[hostname] = not_authenticated
    return data


"""
Create a list with the information of each unauthenticated client
packed into a nice little nested dictionaries we can easily generate
a spreadsheet from.
"""


def build_spreadsheet(data):
    auth_info = []
    for host in data:
        if data[host]:
            client_info = data[host]
            for i in range(len(client_info)):
                info = {
                    "Switch Name": host,
                    "Switchport": f" {client_info[i][0]} ",
                    "MAC Address": client_info[i][1],
                    "VLAN": client_info[i][4],
                    "Auth State": client_info[i][6],
                    "PAE State": client_info[i][10],
                }
                auth_info.append(info)
    return auth_info


"""
Create a CSV file containing out information of each 
unauthenticated wired client
"""


def write_csv(auth_info):
    p.mkdir(exist_ok=True)
    now = datetime.now()
    fnow = now.strftime("%y-%m-%d_%H%M%S")
    filename = f"802.1x_Status_{fnow}.csv"
    fieldnames = [
        "Switch Name",
        "Switchport",
        "MAC Address",
        "VLAN",
        "Auth State",
        "PAE State",
    ]
    with open(p / filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(auth_info)


def main():
    nr = InitNornir(config_file="/path/to/config.yaml")
    result = query_auth(nr)
    parsed_result = parse_result(result)
    spreadsheet = build_spreadsheet(parsed_result)
    write_csv(spreadsheet)


if __name__ == "__main__":
    main()
