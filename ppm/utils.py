import os
import sys


def write(text: str):
	sys.stdout.write(text)
	sys.stdout.flush()


MODULES_FOLDER = os.path.join(os.getcwd(), 'python_modules')


def set_env():
	if os.environ.get('PYTHONPATH') is None:
		os.environ['PYTHONPATH'] = MODULES_FOLDER
	else:
		os.environ['PYTHONPATH'] = MODULES_FOLDER + ':' + os.environ['PYTHONPATH']


class BColors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
