import re
import csv
from datetime import date
from typing import Dict, List, Tuple
from nornir import InitNornir
from nornir.core.task import AggregatedResult
from nornir_netmiko import netmiko_multiline
from Tools import apply_filter, set_creds


def get_host_data() -> Tuple[AggregatedResult, Dict[str, str], Dict[str, int]]:
    """
    Function to execute Netmiko task and return a tuple
    containing the AggregateResult object along with
    role/location data from inventory.
    """
    nr = InitNornir(config_file="config.yaml")
    roles: Dict[str, str] = {}
    location: Dict[str, int] = {}
    commands = ["sh run | i ip address", "sh 802-1w", "sh ver"]

    for host, host_obj in nr.inventory.hosts.items():
        roles[host] = host_obj["role"]
        location[host] = host_obj.data["building"]

    targets = apply_filter(nr)
    set_creds(targets)
    result = targets.run(netmiko_multiline, commands=commands)
    return result, roles, location


def parse_host_data(
    host_data: AggregatedResult, roles: Dict[str, str], location: Dict[str, int]
) -> List[Dict[str, str]]:
    """
    Parse out AggregatedResult object for each host.
    Organize data into a list of nested dictionaries
    that can be easily written into .csv format.
    """
    host_info = []
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    mac_pattern = "(^8.{15}|^1.{15})"
    serial_pattern = "Serial  #:.{11}"
    version_pattern = r"\sVersion\s08.0.{8}"
    for hostname in host_data:
        if host_data[hostname].failed:
            print(f"*****{hostname} IS OFFLINE*****")
            continue

        output = str(host_data[hostname][0])
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
        host_info.append(info)
    return host_info


def write_csv(host_info: List[Dict[str, str]]) -> None:
    """
    Write gathered host data to .csv
    """
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
        writer.writerows(host_info)


def main() -> None:
    host_data, roles, location = get_host_data()
    host_info = parse_host_data(host_data, roles, location)
    write_csv(host_info)
    print(f"***Completed writing file: Switch_Inventory_{date.today()}.csv***")


if __name__ == "__main__":
    main()
