#! /usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command, netmiko_save_config
from Tools import set_creds, apply_filter, confirm, exclude_host

"""
Script using nornir_netmiko to save the running config to startup config on a Ruckus ICX device.
"""


def bs():
    print(bs)


def write_mem(task):
    task.run(netmiko_save_config, cmd="write mem", confirm=False)
    # command = "write mem"
    # output = task.run(netmiko_send_command, command_string=command, enable=True)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    targets = exclude_host(targets)
    confirm(targets)
    set_creds(targets)
    result = targets.run(task=write_mem)
    print_result(result)


if __name__ == "__main__":
    main()
