from nornir import InitNornir

# from nornir_utils.plugins.functions import print_result
from nornir_netmiko import netmiko_multiline
from Tools import apply_filter, set_creds
from datetime import date
import re
import csv


def switch_cmds(task):
    commands = ["sh run | i ip address", "sh 802-1w", "sh ver"]
    task.run(netmiko_multiline, commands=commands)


def get_data():
    nr = InitNornir(config_file="config.yaml")
    roles = {}
    location = {}
    for host in nr.inventory.hosts:
        roles[host] = nr.inventory.hosts[host]["role"]
        location[host] = nr.inventory.hosts[host].data["building"]

    targets = apply_filter(nr)
    set_creds(targets)
    result = targets.run(task=switch_cmds)
    return result, roles, location


def parse_data(data, roles, location):
    switch_info = []
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    mac_pattern = "(^8.{15}|^1.{15})"
    serial_pattern = "Serial  #:.{11}"
    version_pattern = r"\sVersion\s08.0.{8}"
    for hostname in data:
        output = str(data[hostname][1])
        grab_ip = re.search(ip_pattern, output, re.MULTILINE)
        grab_mac = re.search(mac_pattern, output, re.MULTILINE)
        grab_serial = re.search(serial_pattern, output, re.MULTILINE)
        grab_version = re.search(version_pattern, output, re.MULTILINE)
        if grab_ip:
            ip_address = grab_ip.group()
        else:
            ip_address = "Regex failed to match an IP Address"
        if grab_mac:
            mac_address = grab_mac.group(0)
            mac_address = mac_address[4:]
            split_mac = ".".join(
                mac_address[i : i + 4] for i in range(0, len(mac_address), 4)
            )
        else:
            split_mac = "Regex failed to match a MAC Address"
        if grab_serial:
            serial = grab_serial.group(0)
        else:
            serial = "Regex failed to match a Serial #"
        if grab_version:
            version = grab_version.group()
            version = version.strip()
            version = version[8:]
        else:
            version = "Regex failed to match the software version"
        info = {
            "Hostname": hostname,
            "IP Address": ip_address,
            "MAC Address": split_mac,
            "Serial": serial[10:],
            "Version": version,
            "Role": roles[hostname],
            "Building": location[hostname],
        }
        switch_info.append(info)
    return switch_info


def write_csv(switch_info):
    fieldnames = [
        "Hostname",
        "IP Address",
        "MAC Address",
        "Serial",
        "Version",
        "Role",
        "Building",
    ]
    with open(f"Switch_Inventory_{date.today()}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(switch_info)


def main():
    data, roles, location = get_data()
    switch_info = parse_data(data, roles, location)
    write_csv(switch_info)
    print(f"***Completed writing file: Switch_Inventory_{date.today()}.csv***")


if __name__ == "__main__":
    main()
