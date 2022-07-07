#! /usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config
from Tools.get_creds import set_credentials
from Tools.nornir_filter import apply_filter
import getpass

"""
Script using nornir_netmiko to update NTP settings on Brocade ICX series networking devices.
"""


def set_ntp_settings(task):
    ntp_key = getpass.getpass("Please enter the NTP key: ")
    ntp_commands = [
        "no ntp",
        "ntp",
        "disable serve",
        "authenticate",
        f"authentication-key key-id 1 sha1 {ntp_key}",
        "server x.x.x.x",
        "wr",
        "sh ntp associations",
        "sh clock",
    ]
    deploy_ntp = task.run(netmiko_send_config, config_commands=ntp_commands)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    set_credentials(targets)
    result = targets.run(task=set_ntp_settings)
    print_result(result)


if __name__ == "__main__":
    main()
