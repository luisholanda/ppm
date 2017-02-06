import os
import re
import shlex
import subprocess
import sys

import pip

from ppm import utils


def installation_print(mod: str):
	text = utils.BColors.OKGREEN + 'Installing ' + utils.BColors.OKBLUE + mod \
	       + utils.BColors.OKGREEN + ' ...' + utils.BColors.ENDC
	utils.write(text)


class AddCommand:
	def __init__(self, modules: list):
		self._modules = modules
		self._get_dependencies()

	def _get_dependencies(self):
		for mod in self._modules:
			self._install_module(mod)

	def _install_module(self, mod):
		install_text = utils.BColors.OKGREEN + 'Installing ' + utils.BColors.BOLD + utils.BColors.OKBLUE + mod \
		               + utils.BColors.ENDC + utils.BColors.OKGREEN + ' ...' + utils.BColors.ENDC
		utils.write(install_text)
		len1 = len(install_text)

		modules_folder = os.path.join(os.getcwd(), 'python_modules')
		pip.main(['install', mod, '-t', modules_folder, '-q'])

		version_text = utils.BColors.OKBLUE + f'{self._get_version(mod)} ' \
		               + utils.BColors.OKGREEN + '\u2713 \n'

		len2 = 50 - len1 - len(version_text)
		version_text = ' ' * len2 + version_text
		utils.write(version_text)

	@staticmethod
	def _get_version(mod):
		modules_folder = os.path.join(os.getcwd(), 'python_modules')
		command = 'pip show ' + mod
		os.environ['PYTHONPATH'] = modules_folder
		command = shlex.split(command)
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdout.readline()
		output = process.stdout.readline().decode('utf-8')
		version = re.findall(r'\d+.\d+.\d+', output)
		try:
			version = version[0]
		except IndexError:
			pass

		return version


# For testing only
if __name__ == '__main__':
	AddCommand(sys.argv[1:])
