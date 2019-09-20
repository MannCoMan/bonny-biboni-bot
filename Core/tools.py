import os
import logging
import datetime
from Core.constants import Const


def logger(name):
    folder = "Logs/{fold}".format(fold=name)

    if not os.path.exists(folder):
        os.mkdir(folder)

    dformat = datetime.datetime.today()
    dformat = dformat.strftime("%Y_%m")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("{fold}/{file}_{df}.txt".format(
        fold=folder,
        file=name,
        df=dformat
    ))

    formatter = "%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s"
    formatter = logging.Formatter(formatter)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def logs(**kwargs):
    def call(method):
        log = logger(kwargs["name"])
        log.info(kwargs["message"])
        return method
    return call


# function calls counter
def counter(**kwargs):
    def call(method):
        pass


def get_color(color, default=None):
    if not default:
        default = 0x99ccff

    return Const.COLORS.get(color, default)
