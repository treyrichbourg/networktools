#! /usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_config
from Tools.get_creds import set_creds
from Tools.nornir_filter import apply_filter


"""
Script using nornir_netmiko to grab the NTP settings of Brocade ICX series network devices.
"""


def show_ntp_settings(task):
    show_commands = ["sh ntp associations", "sh ntp status", "sh clock"]
    deploy_show = task.run(netmiko_send_config, config_commands=show_commands)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    set_creds(targets)
    result = targets.run(task=show_ntp_settings)
    print_result(result)


if __name__ == "__main__":
    main()
