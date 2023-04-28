#! /usr/bin/python3
import csv
import yaml
from datetime import date

"""
Simple script to convert a CSV file a a hosts.yaml file needed for Nornir inventory.
This script was written to my needs and will need to be adjusted for a different environment.
CSV layout is device, hostname, groups, building.
Other information is dynamically entered by passing values to defaults.yaml
"""

today = date.today()
today_formatted = today.strftime("%b-%d-%Y")


csv_file = ""
yaml_file = f""

# Read csv file into a dictionary
def parse_csv(csv_file):
    with open(csv_file) as f:
        csv_reader = csv.reader(f)
        data = {}
        for row in csv_reader:
            data[row[0]] = {
                "hostname": row[1],
                "groups": [row[2]],
                "data": {"building": int(row[3])},
            }
    return data


# Write yaml inventory from parsed csv data
def write_yaml(data, yaml_file):
    with open(yaml_file, "w") as f:
        f.write("---\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def main():
    data = parse_csv(csv_file)
    write_yaml(data, yaml_file)


if __name__ == "__main__":
    main()
