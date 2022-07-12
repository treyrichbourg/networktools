#! /usr/bin/python3
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_save_config
from nornir_utils.plugins.functions import print_result
from Tools.get_creds import get_secret
from Tools.nornir_filter import filter_site, apply_filter

"""
This script is used to configure rotary groups and assign to the associated
tty lines for ssh access to devices via a terminal server.
"""


def set_secret(task):
    secret = get_secret()
    task.inventory.defaults.connection_options["netmiko"].extras["secret"] = secret


def set_site(task):
    site = filter_site()
    if site is not None:
        task = task.filter(site=site)
        return task


def rotary_config(task):
    # This variable will be the starting port for your rotary groups.  They will increment by 1
    # eg rotary 1 port 2000, rotary 2 port 2001, rotary 3 port 2002, etc
    port = 2000
    commands = [f"ip ssh port {port} rotary 1 127"]
    # Start line at the tty line # you want to start configuring the rotary groups.  On my devices it is line 3
    line = 3
    rotary = 1
    for i in range(3, 27):
        commands.append(f"line {line}")
        commands.append(f"rotary {rotary}")
        commands.append("transport input ssh")
        commands.append("transport output ssh")
        line += 1
        rotary += 1
    task.run(netmiko_send_config, config_commands=commands)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    # targets = set_site(nr)
    set_secret(targets)
    result = targets.run(task=rotary_config)
    print_result(result)


if __name__ == "__main__":
    main()
