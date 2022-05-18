#! /usr/bin/env python3

from netmiko import ConnectHandler
import getpass
from argparse import ArgumentParser


def arg_parse():
    parser = ArgumentParser(description="Arguments for running sh_env.py")
    parser.add_argument(
        "-i", "--ip", required=True, type=str, help="IP address of the device to query"
    )
    args = parser.parse_args()
    return args


def show_env(ip_address, username, password):
    device = ConnectHandler(
        device_type="cisco_ios", ip=ip_address, username=username, password=password
    )
    output = device.send_command("show env all")
    print(output)
    device.disconnect()


def main():
    args = arg_parse()
    ip_address = args.ip
    ssh_username = input("Username: ")
    ssh_password = getpass.getpass("Password: ")
    show_env(ip_address, ssh_username, ssh_password)


if __name__ == "__main__":
    main()
