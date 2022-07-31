#! /usr/bin/python3
import getpass

"""
Convert user input into default credentials for Nornir.
"""


def get_creds():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    secret = getpass.getpass("Enter Secret: ")
    return username, password, secret


def get_user():
    username = input("Enter Username: ")
    return username


def get_password():
    password = getpass.getpass("Enter Password: ")
    return password


def get_secret():
    secret = getpass.getpass("Enter Secret: ")
    return secret


def set_creds(task):
    username, password, secret = get_creds()
    task.inventory.defaults.username = username
    task.inventory.defaults.password = password
    task.inventory.defaults.connection_options["netmiko"].extras["secret"] = secret
