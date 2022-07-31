#! /usr/bin/python3
import csv

"""
Simple script to convert a CSV file a a hosts.yaml file needed for Nornir inventory.
This script was written to my needs and will need to be adjusted for a different environment.
CSV layout is device, hostname, groups, building.
Other information is dynamically entered by passing values to defaults.yaml
"""

csv_file = "/home/trichbourg/Python/csv_inventory.csv"
yaml_file = "/home/trichbourg/Python/hosts.yaml"


def csv_to_yaml(csv_file, yaml_file):
    with open(csv_file) as f:
        csv_reader = csv.reader(f)
        with open(yaml_file, "a") as yf:
            yf.write("---")
            for row in csv_reader:
                device = row[0]
                hostname = row[1]
                group = row[2]
                building = row[3]
                role = row[4]
                yf.write(
                    f"\n{device}:\n  hostname: {hostname}\n  groups:\n    - {group}\n  data:\n    building: {building}\n    role: {role}\n"
                )


def main():
    csv_to_yaml(csv_file, yaml_file)


if __name__ == "__main__":
    main()
