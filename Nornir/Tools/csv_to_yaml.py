#! /usr/bin/python3
"""
Simple script to convert a CSV file to a hosts.yaml file needed for Nornir inventory.
This script was written to my needs and will need to be adjusted for a different environment.
CSV layout is device, hostname, groups, building, role (with the later two being custom keys).
"""
import csv

csv_file = "/path/to/csv_inventory.csv"
yaml_file = "/path/to/output/hosts.yaml"


def csv_to_yaml(input_file, output_file):
    with open(input_file) as f:
        csv_reader = csv.reader(f)
        with open(output_file, "a") as yf:
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


def main() -> None:
    csv_to_yaml(csv_file, yaml_file)


if __name__ == "__main__":
    main()
