#! /usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from Tools import set_creds, apply_filter, confirm, exclude_host

"""
Script using nornir_netmiko to tftp an image to Brocade ICX series network devices.
Adjust the tftp_server, filename, and flash variables in the send_file function below to modify the image being sent.
"""


def send_file(task):
    tftp_server = "x.x.x.x"
    filename = "image"
    flash = "primary"  # primary, secondary, or bootrom
    command = f"copy tftp flash {tftp_server} {filename} {primary}"
    output = task.run(netmiko_send_command, command_string=command, enable=True)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    targets = exclude_host(targets)
    confirm(targets)
    set_creds(targets)
    result = targets.run(task=send_file)
    print_result(result)


if __name__ == "__main__":
    main()
