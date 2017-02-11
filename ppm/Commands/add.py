import os
from multiprocessing import Pool

import pip
from typing import List, Tuple

from ppm import utils

CPU_CORES = len(os.sched_getaffinity(0))

TOTAL_LENGTH = 50


class AddCommand:
	def __init__(self):
		self._modules = []

	def main(self, dependencies: dict or List[str]):
		modules = []

		try:
			for mod, version in dependencies.items():
				# 			TODO: Version handling
				modules.append(mod)
		except AttributeError:
			modules = dependencies

		self._modules = modules
		self._get_dependencies()

	def _get_dependencies(self):
		n = CPU_CORES
		if len(self._modules) < CPU_CORES:
			n = len(self._modules)
		pool = Pool(n)

		install_text = utils.BColors.OKGREEN + 'Installing dependencies...' + utils.BColors.ENDC
		print(install_text)

		for err, module, version in pool.imap_unordered(self._install_module, self._modules):
			module_length = len(module)
			version_length = len(version)

			dots_length = TOTAL_LENGTH - module_length - version_length - 2

			if not err:
				installed_text = module + ' ' * dots_length + utils.BColors.OKBLUE + \
				                 version + utils.BColors.OKGREEN + ' \u2713' + utils.BColors.ENDC

				print(installed_text)
			else:
				fail_text = utils.BColors.FAIL + module + ' ' * dots_length + version + ' \u2717' + utils.BColors.ENDC
				print(fail_text)

	def _install_module(self, mod: str) -> Tuple[str, str, str]:
		error = None
		try:
			pip.main(['install', mod, '-t', utils.MODULES_FOLDER, '-q'])
		except Exception:
			error = 'ERROR'

		version = self.get_version(mod)

		if not version:
			error = 'IERROR'
			version = 'failed'
		elif version == 'error':
			error = 'ERROR'

		return error, mod, version

	@staticmethod
	def get_version(mod: str) -> str:
		from pip.utils import get_installed_version

		path = os.path.join(os.getcwd(), 'python_modules')
		abs_path = os.path.abspath(path)
		try:
			version = get_installed_version(mod, [abs_path])
		except:
			return 'error'

		return version


if __name__ == '__main__':
	utils.set_env()
	cmd = AddCommand()
	cmd.main(['twisted', 'tornado', 'numpy', 'pandas', 'matplotlib', 'seaborn'])
