#! /usr/bin/python3
from pathlib import Path
from datetime import date
from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_netmiko.tasks import netmiko_send_command
from Tools import set_creds, apply_filter, exclude_host, confirm

"""
Script using nornir_netmiko take a backup of the running config
"""

backup_dir = "backups/"
p = Path(backup_dir)
nr = InitNornir(config_file="config.yaml")


def create_backups_dir():
    p.mkdir(exist_ok=True)


def save_config_to_file(destination, hostname, config):
    today = date.today()
    filename = f"{hostname}-{today}.cfg"
    with open(destination / filename, "w") as f:
        f.write(config)


def get_netmiko_backups():
    targets = apply_filter(nr)
    set_creds(targets)
    backup_results = targets.run(task=netmiko_send_command, command_string="show run")

    for hostname in backup_results:
        # create dir for each host in backups root
        dest = p / hostname
        dest.mkdir(exist_ok=True)
        save_config_to_file(
            destination=dest,
            hostname=hostname,
            config=backup_results[hostname][0].result,
        )


def main() -> None:
    create_backups_dir()
    get_netmiko_backups()
    print(f"All devices have been backed up to {backup_dir}")


if __name__ == "__main__":
    main()
