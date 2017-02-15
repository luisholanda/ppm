import os
import sys


def write(text: str):
    sys.stdout.write(text)
    sys.stdout.flush()


MODULES_FOLDER = os.path.join(os.getcwd(), 'python_modules')


def set_env():
    sys.path.append(MODULES_FOLDER)


def parse_version(ver: tuple):
    return f'{ver[0]}.{ver[1]}'


def tuple_version(ver: str):
    return ver[0], ver[2]


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
