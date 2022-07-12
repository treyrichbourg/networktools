#! /usr/bin/python3
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from Tools.get_creds import get_secret
from Tools.nornir_filter import filter_site

"""
Script for mitigating NTP mode 6 vulnerability on cisco IOS and IOSXE devices.
"""


def set_secret(task):
    secret = get_secret()
    task.inventory.defaults.connection_options["netmiko"].extras["secret"] = secret


def set_site(task):
    site = filter_site()
    if site is not None:
        task = task.filter(site=site)
        return task


def disable_mode_control(task):
    commands = [
        "no ntp allow mode control 0",
        "exit",
        "sh ntp associations",
        "sh run | i mode control",
    ]
    deploy_commands = task.run(netmiko_send_config, config_commands=commands)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    nr = set_site(nr)
    set_secret(nr)
    result = nr.run(task=disable_mode_control)
    print_result(result)


if __name__ == "__main__":
    main()
