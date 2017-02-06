import re
import shlex
import subprocess
import sys

import pip

from ppm import utils


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

		pip.main(['install', mod, '-t', utils.MODULES_FOLDER, '-q'])

		version = self._get_version(mod)
		version_text = utils.BColors.OKBLUE + f'{version} ' \
		               + utils.BColors.OKGREEN + '\u2713 \n'

		len2 = 50 - len1 - len(version_text)
		version_text = ' ' * len2 + version_text
		utils.write(version_text)

	@staticmethod
	def _get_version(mod):
		command = 'pip show ' + mod
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
	utils.set_env()
	AddCommand(sys.argv[1:])
