"""
Bot launcher
TODO:
* add arg_parser
* infinite process loop
? good monkey patching system
"""

import sys
import pytz
import datetime
import subprocess
import argparse
from bot import Bot
from Core.constants import Const


def monkey_injection():
    pass


def args_injection(**kwargs):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        action="store",
        default=Const.BOT_TOKEN
    )

    parser.add_argument(
        "-rf", "--run-forever",
        action="store_true",
        default=True
    )

    parser.add_argument(
        "-l", "--logs",
        action="store",
        default="Data/logs.txt"
    )

    parser.add_argument(
        "-dl", "--dont-load",
        action="store",
        default=[]
    )

    parsed = parser.parse_args()
    return parser


if __name__ == '__main__':
    module = sys.argv[1]
    while True:
        date = datetime.datetime.now()
        print("\nStarting {} - {}".format(module, date))
        p = subprocess.Popen("python " + module, shell=True)
        p.wait()