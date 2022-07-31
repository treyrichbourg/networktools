#! /usr/bin/python3
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from nornir.core.filter import F
from Tools import apply_filter, set_creds, exclude_host, confirm

"""
Script using nornir_netmiko to reload Brocade ICX series network devices.
Adjust the flash variable in the boot_sys function to choose which flash to boot from.
This is mainly used when updating firmware or switching flash images.
Otherwise use a standard reload script.
"""


def boot_sys(task):
    flash = "primary"  # primary or secondary
    command = f"boot system flash {flash} yes"
    output = task.run(netmiko_send_command, command_string=command, enable=True)


def main() -> None:
    nr = InitNornir(config_file="config.yaml")
    targets = apply_filter(nr)
    targets = exclude_host(targets)
    confirm(targets)
    set_creds(targets)
    targets.run(task=boot_sys)
    for target in targets.inventory.hosts:
        print(f"{target} is reloading.")


if __name__ == "__main__":
    main()
