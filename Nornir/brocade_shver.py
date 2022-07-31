#! /usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_multiline
from Tools import apply_filter, set_creds, exclude_host

"""
Script using nornir_netmiko show the current version and flash contents of Brocade ICX series network devices.
"""


def show_version(task):
    commands = ["sh ver", "sh flash"]
    output = task.run(netmiko_multiline, commands=commands)


def write_log(result):
    with open("brocade_shver_output.txt", "w") as f:
        for line in result:
            f.write(
                "**************************************************************************\n"
            )
            f.write(f"{line}")
            f.write(f"{result[line][1]}")
            f.write(
                "\n\n**************************************************************************\n"
            )


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    targets = exclude_host(targets)
    set_creds(targets)
    result = targets.run(task=show_version)
    write_log(result)
    print_result(result)


if __name__ == "__main__":
    main()
