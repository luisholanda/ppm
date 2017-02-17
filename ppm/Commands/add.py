import json
import os
import sys
from multiprocessing import Pool
from typing import List, Tuple

import pip
from pip.utils import get_installed_version

from ppm import utils

CPU_CORES = len(os.sched_getaffinity(0))

TOTAL_LENGTH = 50


class AddCommand:
    def __init__(self):
        self._modules = []
        self._egg_info = {
            'dependencies': {},
            'py_version': sys.version[0:3]
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

        with open('pyckage.json') as fp:
            pyck = json.load(fp)
            self._pyck = pyck
            dep = self._pyck.get('dependencies')
            self._pyck['dependencies'] = dep if dep else {}

    def main(self, argv: List[str], add: bool):
        modules = []

        if argv:
            dependencies = argv
        else:
            # For now, nothing of version handling
            if self._pyck.get('dependencies'):
                dependencies = list(self._pyck['dependencies'].keys())
            else:
                print("This project doesn't have dependencies yet, "
                      "use `ppm {add, a} MODULE` to add a dependence\n")
                sys.exit(1)

        self._modules = dependencies
        self._get_dependencies()

        if add:
            with open('pyckage.json', 'w') as fp:
                json.dump(self._pyck, fp, indent=2)

    def _get_dependencies(self):
        pool = Pool(CPU_CORES)

        install_text = utils.BColors.OKGREEN + 'Installing dependencies...' + utils.BColors.ENDC
        print(install_text)

        for err, module in pool.imap_unordered(self._install_module, self._modules):
            module_length = len(module)

            version = self.get_version(module)
            if version is None:
                err = 'InstError' if not err else err

            if not err:
                version_length = len(version)
                dots_length = TOTAL_LENGTH - module_length - version_length - 2

                self._egg_info['dependencies'][module] = {
                    'name': module,
                    'egg_file': self.egg_info(module, version),
                    'dist_info': self.dist_info(module, version),
                    'version': version
                }
                installed_text = module + ' ' * dots_length + utils.BColors.OKBLUE + \
                                 version + utils.BColors.OKGREEN + ' \u2713' + utils.BColors.ENDC

                print(installed_text)
                self._pyck['dependencies'][module] = version
            else:
                dots_length = TOTAL_LENGTH - module_length - len(err) - 2
                fail_text = utils.BColors.FAIL + module + ' ' * dots_length + err + ' \u2717' + utils.BColors.ENDC
                print(fail_text)

        with open('.ppm.info', 'w') as ppm_info:
            ppm = self._egg_info
            ppm['modules_path'] = os.path.join(os.getcwd(), 'python_modules')
            json.dump(ppm, ppm_info, indent=2)

    def _install_module(self, mod: str) -> Tuple[str or None, str]:
        error = None

        try:
            pip.main(['install', mod, '-t', utils.MODULES_FOLDER, '-qq'])
        except Exception:
            error = 'Error'

        return error, mod

    def egg_info(self, mod: str, ver: str):
        return f"{mod}-{ver}-py{self._egg_info['py_version']}.egg-info"

    @staticmethod
    def dist_info(mod: str, ver: str):
        return f"{mod}-{ver}.dist-info"

    @staticmethod
    def get_version(mod: str) -> str:
        from ppm.utils import MODULES_FOLDER

        try:
            version = get_installed_version(mod, [MODULES_FOLDER])
        except:
            return 'error'

        return version
