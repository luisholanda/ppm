import json
import sys

from typing import Dict

import ppm.utils as utils
from ppm.Commands import add, init


class PythonPackageManager:
	def __init__(self):
		self._dependencies: Dict[str, str]
		self._start_script: str
		self._run_scripts: Dict[str, str]

	def main(self, args: list or str):
		command = args[0]
		self._parse_pyckage(command)
		if command == 'add':
			if len(args) > 1:
				add.AddCommand(args[1:])
			else:
				add.AddCommand(self._dependencies)
		elif command == 'init':
			if len(args) > 1:
				sys.exit(1)
			else:
				init.InitCommand()

	def _parse_pyckage(self, command: str):
		try:
			with open('pyckage.json') as file:
				pyckage = json.load(file)

				try:
					self._dependencies = pyckage['dependencies']
				except KeyError:
					self._dependencies = {}

				try:
					self._run_scripts = pyckage['scripts']
				except KeyError:
					self._run_scripts = {}

				try:
					self._start_script = self._run_scripts['start']
				except KeyError:
					self._start_script = None
		except FileNotFoundError:
			if command == 'init':
				pass
			else:
				text = utils.BColors.BOLD + utils.BColors.FAIL + 'You should first use `' \
				       + utils.BColors.UNDERLINE + 'ppm init' + utils.BColors.ENDC \
				       + utils.BColors.BOLD + utils.BColors.FAIL + '`.'
				print(text)
				sys.exit(1)


if __name__ == '__main__':
	ppm = PythonPackageManager()

	args = sys.argv[1:]
	ppm.main(args)
