import json
import os
from multiprocessing import Pool

from typing import List, Tuple

from ppm import utils
from ppm.Commands.add import AddCommand

CPU_CORES = len(os.sched_getaffinity(0))


class RemoveCommand:
    def __init__(self):
        self._modules = []
        self._pool = Pool(CPU_CORES)
        self._egg_info = {}

        with open('.ppm.info') as ppm_info:
            info = json.load(ppm_info)
            self._egg_info = info
            self._modules_path = info['modules_path']

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['_pool']
        return self_dict

    def main(self, modules: List[str]):
        if modules:
            self._modules = modules

        for err, module in self._pool.imap_unordered(self.remove_module, self._modules):
            self.logs_uninstall(err, module)

    @staticmethod
    def logs_uninstall(err, module):
        if not err:
            print(utils.BColors.OKGREEN + f'{module} removed' + utils.BColors.ENDC)
        elif err == 'NotFError':
            print(utils.BColors.FAIL + f'{module} is not installed' + utils.BColors.ENDC)
        else:
            print(utils.BColors.FAIL + f'Something bad happen while removing {module}: {err}' \
                  + utils.BColors.ENDC)

    def remove_module(self, module: str) -> Tuple[str, str]:
        import shutil

        error = None
        imported_module = None
        path = None
        file = None

        if not AddCommand.get_version(module):
            return 'NotFError', module

        # Import the module we want to delete
        try:
            locals()[module] = __import__(module, globals=globals())
            imported_module = locals()[module]
        except ImportError:
            error = 'ImpError'
        except ModuleNotFoundError:
            error = 'NotFError'

        # Get the path for the module
        if imported_module:
            try:
                path = imported_module.__path__[0]
            except AttributeError:
                file = imported_module.__file__
            except IndexError:
                error = 'InsError'
        else:
            return error, module

        # Then we delete it
        if path:
            try:
                shutil.rmtree(path)
            except Exception:
                error = 'RmError'

            # Remove also the egg-info file/folder
            # Some module have capitalized egg-info
            try:
                egg_file = self._egg_info['dependencies'][module]['egg_file']
            except KeyError as err:
                # For now I can't handle dependencies of packages
                raise err
            else:
                cap_egg_file = egg_file[0].capitalize() + egg_file[1:]
                paths = {
                    'egg'    : os.path.join(self._modules_path, egg_file),
                    'cap_egg': os.path.join(self._modules_path, cap_egg_file)
                }
                if os.path.exists(paths['egg']):
                    try:
                        shutil.rmtree(paths['egg'])
                    except NotADirectoryError:
                        os.remove(paths['egg'])
                elif os.path.exists(paths['cap_egg']):
                    try:
                        shutil.rmtree(paths['cap_egg'])
                    except NotADirectoryError:
                        os.remove(paths['cap_egg'])

            # Remove also the dist-info file/folder
            # Some module have capitalized dist-info
            try:
                dist_file = self._egg_info['dependencies'][module]['dist_info']
            except KeyError:
                raise err
            else:
                cap_dist_file = dist_file[0].capitalize() + dist_file[1:]
                paths = {
                    'egg'    : os.path.join(self._modules_path, dist_file),
                    'cap_egg': os.path.join(self._modules_path, cap_dist_file)
                }
                if os.path.exists(paths['egg']):
                    try:
                        shutil.rmtree(paths['egg'])
                    except NotADirectoryError:
                        os.remove(paths['egg'])
                elif os.path.exists(paths['cap_egg']):
                    try:
                        shutil.rmtree(paths['cap_egg'])
                    except NotADirectoryError:
                        os.remove(paths['cap_egg'])
        elif file:
            try:
                os.remove(file)
            except FileNotFoundError:
                error = 'RmError'

        # Check if the module is really deleted
        version = AddCommand.get_version(module)

        if version:
            error = 'VerError'

        return error, module
