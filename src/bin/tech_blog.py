#!/usr/bin/env python

import argparse
import asyncio
import sys
from getpass import getpass

sys.path.append(".")

from src.infrastructure.controllers import CLIController

COMMAND_MIGRATE = "migrate"
COMMAND_SUPERUSER = "create_superuser"

HELP_TEXT = f"""
To migrate database run `{COMMAND_MIGRATE}`.
To create a superuser run `{COMMAND_SUPERUSER}`.
"""


def help_text():
    print(HELP_TEXT)


async def create_superuser():
    email = str(input("\nEmail: "))
    username = str(input("\nUsername: "))
    password = str(getpass("\nPassword: "))

    controller = CLIController()
    await controller.create_superuser(username, email, password)


def main():
    commands = (COMMAND_MIGRATE, COMMAND_SUPERUSER)
    parser = argparse.ArgumentParser(
        description="Enter command to execute.", usage=", ".join(commands)
    )
    parser.add_argument(
        "Action", metavar="action", type=str, choices=commands, help=HELP_TEXT
    )

    args = parser.parse_args()
    handler_name = args.Action
    controller = CLIController()
    if handler_name == COMMAND_MIGRATE:
        controller.migrate()
    elif handler_name == COMMAND_SUPERUSER:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_superuser())
        loop.close()
    else:
        help_text()


if __name__ == "__main__":
    exit(main())
