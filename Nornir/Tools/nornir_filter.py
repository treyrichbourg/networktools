#! /usr/bin/python3
"""
Simple functions to dynamically obtain data for filtering nornir SimpleInventory
"""


def filter_host(task):
    try:
        prompt = input("Would you like to filter a particular host? (y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            host = input("Enter hostname: ").strip()
            if host not in task.inventory.hosts:
                print("Please enter a valid hostname\n")
                return filter_host()
            else:
                return host
        elif prompt.lower().strip() in ["n", "no"]:
            return
        else:
            print("Pleae enter a valid input\n")
            return filter_host()
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_host()


def filter_building():
    building_list = []
    try:
        prompt = input("Filter by building? (y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            building = input(
                f"Please enter a building number: \nPossible options: {str(building_list)}\n: "
            ).strip()
            building = int(building)
            if building not in building_list:
                print("Please enter a valid building\n")
                return filter_building()
            else:
                return building
        elif prompt.lower().strip() in ["n", "no"]:
            return
        else:
            print("Please enter a valid input\n")
            return filter_building()
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_building()


def filter_role():
    layers = ["access", "distribution", "core"]
    try:
        prompt = input("Filter by switch role? (y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            role = input(f"Possible options: \n{layers}\n: ")
            if role not in layers:
                print("Please enter a valid switch role\n")
                return filter_role()
            else:
                return role
        elif prompt.lower().strip() in ["n", "no"]:
            return
        else:
            print("Please enter a valid input\n")
            return filter_role()
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_role()


def filter_site():
    sites = []
    try:
        prompt = input("Filter by site? (y/n): ")
        if prompt.lower().strip() in ["y", "yes"]:
            role = input(f"Possible options: \n{sites}\n: ")
            if role not in sites:
                print("Please enter a valid site\n")
                return filter_site()
            else:
                return role
        elif prompt.lower().strip() in ["n", "no"]:
            return
        else:
            print("Please enter a valid input\n")
            return filter_site()
    except Exception as error:
        print("Please enter a valid input\n")
        print(error)
        return filter_site()


def apply_filter(task):
    host = filter_host(task)
    if host is not None:
        target = task.filter(name=host)
        return target
    else:
        pass
    building = filter_building()
    role = filter_role()
    if building is None and role is None:
        return task
    elif building is not None and role is not None:
        targets = task.filter(building=building, role=role)
        return targets
    elif building is None:
        targets = task.filter(role=role)
        return targets
    else:
        targets = task.filter(building=building)
        return targets
