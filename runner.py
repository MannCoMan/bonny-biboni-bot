"""
Bot launcher
TODO:
* add arg_parser
* infinite process loop
? good monkey patching system
"""

import sys
import datetime
import subprocess
import argparse
from bot import Bot
from Core.constants import Const


def monkey_injection():
    pass


def parse_args(**kwargs):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        action="store",
        default="bot.py"
    )

    parser.add_argument(
        "--token",
        action="store",
        default=Const.BOT_TOKEN
    )

    parser.add_argument(
        "--forever",
        action="store_true",
        default=True
    )

    parser.add_argument(
        "--logs",
        action="store",
        default="Data/logs.txt"
    )

    parser.add_argument(
        "--dont-load",
        action="store",
        default=[]
    )

    parsed = parser.parse_args()
    return vars(parsed)


if __name__ == '__main__':
    parsed = parse_args()
    module = parsed.get("file")

    while True:
        date = datetime.datetime.now()
        print("\nStarting {} - {}".format(module, date))
        p = subprocess.Popen("python3 " + module, shell=True)
        p.wait()

        token = parsed.get("token", Const.BOT_TOKEN)

        if not token:
            raise RuntimeError("Can't get token get token")
        bot = Bot(parsed).run(token)
