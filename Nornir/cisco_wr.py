#! /usr/bin/python3
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_config, netmiko_save_config
from nornir_utils.plugins.functions import print_result
from Tools.get_creds import get_secret
from Tools.nornir_filter import filter_site

"""
Script for saving running-config to startup-config on cisco routers.
"""


def set_secret(task):
    secret = get_secret()
    task.inventory.defaults.connection_options["netmiko"].extras["secret"] = secret


def set_site(task):
    site = filter_site()
    if site is not None:
        task = task.filter(site=site)
        return task


def wr(task):
    task.run(netmiko_save_config)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    target = set_site(nr)
    set_secret(target)
    result = target.run(task=wr)
    print_result(result)


if __name__ == "__main__":
    main()
