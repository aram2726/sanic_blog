#!/usr/bin/env python

import argparse
import sys

sys.path.append(".")

from src.infrastructure.controllers import CLIController

COMMAND_MIGRATE = "migrate"

HELP_TEXT = f"""
To migrate database run `{COMMAND_MIGRATE}`.
"""


def help_text():
    print(HELP_TEXT)


def main():
    commands = (COMMAND_MIGRATE,)
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
    else:
        help_text()


if __name__ == "__main__":
    exit(main())
