#! /usr/bin/python3
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_save_config
from nornir_utils.plugins.functions import print_result
from Tools.get_creds import get_secret

"""
Script for setting the ssh server/client key exchange algorithm to DHGRP14.
This upgrade is for Cisco 2900 series devices as the ISR 4000 series uses a
strong encryption algorithm by default.
"""


def set_secret(task):
    secret = get_secret()
    task.inventory.defaults.connection_options["netmiko"].extras["secret"] = secret


def upgrade_kex(task):
    commands = [
        "ip ssh server algorithm kex diffie-hellman-group14-sha1",
        "ip ssh client algorithm kex diffie-hellman-group14-sha1",
        "exit",
        "sh ip ssh",
    ]
    task.run(netmiko_send_config, config_commands=commands)
    task.run(netmiko_save_config)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    target = nr.filter(platform="cisco_ios")
    set_secret(target)
    result = target.run(task=upgrade_kex)
    print_result(result)


if __name__ == "__main__":
    main()
