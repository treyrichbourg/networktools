#! /usr/bin/python3
"""
Simple functions to dynamically obtain filtering data for Nornir SimpleInventory.
"""


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


def apply_filter(task):
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
