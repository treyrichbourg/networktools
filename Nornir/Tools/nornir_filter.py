#! /usr/bin/python3
from nornir.core.filter import F

"""
Simple functions to dynamically obtain data for filtering nornir SimpleInventory
"""


def confirm(task):
    switches = [target for target in task.inventory.hosts]
    if len(switches) == 1:
        print(f"\nYou are about to target the following device:\n{switches}\n")
    else:
        print(
            f"\nYou are about to target the following devices:\n{len(task.inventory.hosts)} Devices:\n{switches}\n"
        )
    prompt = input("Continue? (y/n): ")
    try:
        if prompt.lower().strip() in ["y", "yes"]:
            return
        elif prompt.lower().strip() in ["n", "no"]:
            exit()
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return confirm(task)


def filter_host(task):
    try:
        prompt = input("Would you like to filter a particular host? (y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            host = input("Enter hostname: ").strip()
            if host not in task.inventory.hosts:
                print("Please enter a valid hostname\n")
                return filter_host(task)
            else:
                target = task.filter(name=host)
                return target
        elif prompt.lower().strip() in ["n", "no"]:
            return task
        else:
            print("Pleae enter a valid input\n")
            return filter_host(task)
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_host(task)


def filter_building(task):
    building_list = []
    try:
        prompt = input("Filter by building? (y/n): ")
        for host in task.inventory.hosts:
            buildings = task.inventory.hosts[host]["building"]
            if buildings not in building_list:
                building_list.append(buildings)
        if prompt.lower().strip() in ["y", "yes"]:
            building = input(
                f"Please enter a building number: \nPossible options: {str(building_list)}\n: "
            ).strip()
            building = int(building)
            if building not in building_list:
                print("Please enter a valid building\n")
                return filter_building(task)
            else:
                target = task.filter(building=building)
                return target
        elif prompt.lower().strip() in ["n", "no"]:
            return task
        else:
            print("Please enter a valid input\n")
            return filter_building(task)
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_building(task)


def filter_role(task):
    layers = ["access", "distribution", "core"]
    try:
        prompt = input("Filter by switch role? (y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            role = input(f"Possible options: \n{layers}\n: ")
            if role not in layers:
                print("Please enter a valid switch role\n")
                return filter_role(task)
            else:
                target = task.filter(role=role)
                return target
        elif prompt.lower().strip() in ["n", "no"]:
            return task
        else:
            print("Please enter a valid input\n")
            return filter_role(task)
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_role(task)


def filter_site(task):
    sites = []
    try:
        prompt = input("Filter by site? (y/n): ")
        for host in task.inventory.hosts:
            site = task.inventory.hosts[host]["site"]
            if site not in sites:
                sites.append(site)
        if prompt.lower().strip() in ["y", "yes"]:
            role = input(f"Possible options: \n{sites}\n: ")
            if site not in sites:
                print("Please enter a valid site\n")
                return filter_site(task)
            else:
                target = task.filter(site=site)
                return target
        elif prompt.lower().strip() in ["n", "no"]:
            return task
        else:
            print("Please enter a valid input\n")
            return filter_site(task)
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_site(task)


def exclude_host(task):
    try:
        total = len(task.inventory.hosts)
        current_selection = [target for target in task.inventory.hosts]
        if total == 1:
            print(
                f"\nCurrently you have {total} selected device:\n{current_selection}\n"
            )
        else:
            print(
                f"\nCurrently you have {total} selected devices:\n{current_selection}\n"
            )
        prompt = input("Would you like to exclude a host from this selection?(y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            hostnames = input(
                "Enter the hostnames to exclude below (for multiple hostnames separate by ',':\n"
            )
            hostnames = hostnames.split(",")
            for host in hostnames:
                if host.strip() not in task.inventory.hosts:
                    print("Please enter a valid hostname")
                    return exclude_host(task)
                else:
                    host = host.strip()
                    task = task.filter(~F(name=host))
            return task
        elif prompt.lower().strip() in ["n", "no"]:
            return task
        else:
            print("Please enter a valid input\n")
            return exclude_host(task)
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return exclude_host(task)


def apply_filter(task):
    target = filter_host(task)
    if len(target.inventory.hosts) == 1:
        return target
    targets = filter_building(task)
    targets = filter_role(targets)
    return targets
