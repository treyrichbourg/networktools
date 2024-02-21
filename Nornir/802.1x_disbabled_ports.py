from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from Tools import set_creds, apply_filter, exclude_host, confirm
from datetime import date
from tabulate import tabulate
import pandas as pd
import re
import csv


# Scrape the output of 'sh int br'
def switch_command(task):
    command = "sh int br"
    result = task.run(netmiko_send_command, command_string=command)
    return result


# Feed aggregate result of 'sh int br' from the targets and grab required data
def parse_data(data):
    parsed_data = []
    for host in data:
        result = data[host][1]
        result = str(result)
        result = result.split("\n")
        for row in range(3, len(result)):
            row = result[row]
            row_split = re.split(r"\s+", row)
            port = row_split[0]
            vlan = row_split[7]
            vlan_filter = []
            port_name = row_split[10]
            if vlan not in vlan_filter:
                interface_data = {
                    "Hostname": host,
                    "Interface": port,
                    "VLAN": vlan,
                    "Port Name": port_name,
                }
                parsed_data.append(interface_data)
    return parsed_data


def write_csv(parsed_data):
    fieldnames = [
        "Hostname",
        "Interface",
        "VLAN",
        "Port Name",
    ]
    with open(f"Dot1x_Disabled_Ports_{date.today()}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_data)


def main():
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    targets = exclude_host(targets)
    confirm(targets)
    set_creds(targets)
    result = targets.run(task=switch_command)
    parsed_result = parse_data(result)
    write_csv(parsed_result)
    df = pd.DataFrame(parsed_result)
    print(tabulate(df, headers="keys", tablefmt="psql"))
    print(f"***Completed writing file: Dot1x_Disabled_Ports_{date.today()}.csv***")


if __name__ == "__main__":
    main()
