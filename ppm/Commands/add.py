import json
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
        self._egg_info = {
            'dependencies': {},
            'py_version'  : sys.version[0:3]
        }

        try:
            with open('.ppm.info') as f:
                pyck = json.load(f)
                try:
                    self._egg_info['python'] = pyck['python']
                except KeyError:
                    pass
                try:
                    self._egg_info['dependencies'] = pyck['dependencies']
                except KeyError:
                    pass

        except FileNotFoundError:
            # This happen in the first time that the user
            # run ppm in a project
            # The .ppm.info should be only used as a short
            # storage for package's info that must be
            # known in others runs of ppm.
            pass

    def main(self, dependencies: dict or List[str]):
        modules = []

        try:
            for mod, version in dependencies.items():
                # TODO: Version handling
                modules.append(mod)
        except AttributeError:
            modules = dependencies

        self._modules = modules
        self._get_dependencies()

    def _get_dependencies(self):
        pool = Pool(CPU_CORES)

        install_text = utils.BColors.OKGREEN + 'Installing dependencies...' + utils.BColors.ENDC
        print(install_text)

        for err, module, version in pool.imap_unordered(self._install_module, self._modules):
            module_length = len(module)
            version_length = len(version)

            dots_length = TOTAL_LENGTH - module_length - version_length - 2

            if not err:
                self._egg_info['dependencies'][module] = {
                    'name'     : module,
                    'egg_file' : self.egg_info(module, version),
                    'dist_info': self.dist_info(module, version),
                    'version'  : version
                }
                installed_text = module + ' ' * dots_length + utils.BColors.OKBLUE + \
                                 version + utils.BColors.OKGREEN + ' \u2713' + utils.BColors.ENDC

                print(installed_text)
            else:
                dots_length = TOTAL_LENGTH - module_length - len(err) - 2
                fail_text = utils.BColors.FAIL + module + ' ' * dots_length + err + ' \u2717' + utils.BColors.ENDC
                print(fail_text)

        with open('.ppm.info', 'w') as ppm_info:
            ppm = self._egg_info
            ppm['modules_path'] = os.path.join(os.getcwd(), 'python_modules')
            json.dump(ppm, ppm_info, indent=2)

    def _install_module(self, mod: str) -> Tuple[str, str, str]:
        error = None

        try:
            pip.main(['install', mod, '-t', utils.MODULES_FOLDER, '-qq'])
        except Exception:
            error = 'ERROR'

        version = self.get_version(mod)

        if not version:
            error = 'IERROR'
            version = 'failed'
        elif version == 'error':
            error = 'ERROR'

        return error, mod, version

    def egg_info(self, mod: str, ver: str):
        return f"{mod}-{ver}-py{self._egg_info['py_version']}.egg-info"

    @staticmethod
    def dist_info(mod: str, ver: str):
        return f"{mod}-{ver}.dist-info"

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

    def add_module(self, module: str, version: str):
        with open('pyckage.json', 'w+') as fp:
            pyck = json.load(fp)
            pyck['dependencies'][module] = version


if __name__ == '__main__':
    import sys

    utils.set_env()
    cmd = AddCommand()
    cmd.main(sys.argv[1:])
