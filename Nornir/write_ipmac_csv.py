from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
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
    targets = apply_filter(nr)
    set_creds(targets)
    result = targets.run(task=switch_cmds)
    return result


def parse_data(data):
    switch_info = []
    ip_pattern = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    mac_pattern = "(^8.{15}|^1.{15})"
    serial_pattern = "Serial  #:.{11}"
    for hostname in data:
        output = str(data[hostname][1])
        grab_ip = re.search(ip_pattern, output, re.MULTILINE)
        grab_mac = re.search(mac_pattern, output, re.MULTILINE)
        grab_serial = re.search(serial_pattern, output, re.MULTILINE)
        try:
            ip_address = grab_ip.group()
        except:
            ip_address = "Regex failed to match an IP Address"
        try:
            mac_address = grab_mac.group(0)
            mac_address = mac_address[4:]
            split_mac = ".".join(
                mac_address[i : i + 4] for i in range(0, len(mac_address), 4)
            )
            # mac_address = ".".join(
            #    mac_address[i : i + 4] for i in range(0, len(mac), 4)
            # )
        except:
            mac_address = "Regex failed to match a MAC Address"
        try:
            serial = grab_serial.group(0)
        except:
            serial = "Regex failed to match a Serial #"
        # ip_address = grab_ip.group()
        # mac_address = grab_mac.group(0)
        # serial = grab_serial.group(0)
        info = {
            "Hostname": hostname,
            "IP Address": ip_address,
            # "MAC Address": mac_address[4:],
            "MAC Address": split_mac,
            "Serial": serial[10:],
        }
        switch_info.append(info)
    return switch_info


def write_csv(switch_info):
    fieldnames = ["Hostname", "IP Address", "MAC Address", "Serial"]
    with open(f"Switch_Inventory_{date.today()}.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(switch_info)


def main():
    data = get_data()
    switch_info = parse_data(data)
    write_csv(switch_info)
    print(f"***Completed writing file: Switch_Inventory_{date.today()}.csv***")


if __name__ == "__main__":
    main()
