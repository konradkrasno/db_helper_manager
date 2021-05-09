import configparser
import sys
from typing import Dict

from db_helper_manager.db_manager import DBManager
from db_helper_manager.exceptions import ImproperlyConfiguredError


def get_db_config(config: configparser.ConfigParser) -> Dict:
    return {
        "DIALECT": config.get("db_config", "DIALECT"),
        "NAME": config.get("db_config", "NAME"),
        "USER": config.get("db_config", "USER"),
        "PASSWORD": config.get("db_config", "PASSWORD"),
        "HOST": config.get("db_config", "HOST"),
        "PORT": config.get("db_config", "PORT"),
    }


def main():
    config = configparser.ConfigParser()
    if not config.read("setup.ini"):
        raise ImproperlyConfiguredError(
            "setup.ini not defined! Check README how configure setup.ini file."
        )
    try:
        command = sys.argv[1]
    except IndexError:
        print("No command provided.")
        DBManager.print_command_list()
    else:
        manager = DBManager(db_config=get_db_config(config))
        manager.execute_command(command, *sys.argv[2:])
