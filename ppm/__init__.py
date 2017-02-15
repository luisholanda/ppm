import argparse
import json
import sys

from typing import Dict

from ppm import utils
from ppm.Commands import add, command, init

__version__ = '0.1.0'


def create_main_parser() -> argparse.ArgumentParser:
    prog = 'ppm'
    description = """
		This program helps you create Python projects and handle their dependencies.
	"""
    usage = '%(prog)s [command] [options]'
    epilog = '''Run `ppm COMMAND --help` for more information on specific commands.'''
    parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            usage=usage,
            epilog=epilog
    )
    parser.add_argument('command',
                        nargs=1,
                        type=str,
                        choices=[
                            'add', 'init', 'remove', 'run', 'start'
                        ],
                        help='The command that should run (default add)'
                        )

    return parser


class PythonPackageManager:
    def __init__(self):
        self._dependencies: Dict[str, str]
        self._start_script: str
        self._run_scripts: Dict[str, str]
        self._parser = create_main_parser()

    def main(self):
        if len(sys.argv) > 1:
            args = self._parser.parse_args()
            self._parse_pyckage(args['command'])
        else:
            command['add']().main()

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
