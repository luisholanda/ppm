import argparse
import json
import sys

from typing import Dict

from ppm import utils
from ppm.Commands import command

__version__ = '0.1.0'


def create_main_parser() -> argparse.ArgumentParser:
    prog = 'ppm'
    description = """
		This program helps you create Python projects and handle their dependencies.
	"""
    usage = '%(prog)s [command] [args]'
    epilog = '''Run `ppm COMMAND --help` for more information on specific commands.'''
    parser = argparse.ArgumentParser(
            prog=prog,
            description=description,
            epilog=epilog
    )

    subparser = parser.add_subparsers(dest='cmd')

    # Add subparser
    add_parser = subparser.add_parser('add',
                                      aliases='a',
                                      description="""
        Easily install Python packages and add them to pyckage.json dependencies.
                                      """)
    add_parser.add_argument('modules',
                            nargs=argparse.ZERO_OR_MORE)
    add_parser.set_defaults(func=add_comand)

    # Init subparser
    init_parser = subparser.add_parser('init',
                                       aliases='i',
                                       description="""
        Easily initialize Python packages and make a initial pyckage.json
                                       """)
    init_parser.set_defaults(func=init_command)

    # Remove subparser
    remove_parser = subparser.add_parser('remove',
                                         aliases=['rem', 'rm'],
                                         description="""
        Remove local installed Python packages and remove them from pyckage.json
                                         """)
    remove_parser.add_argument('modules',
                               nargs=argparse.ZERO_OR_MORE)
    remove_parser.set_defaults(func=remove_command)

    return parser


def add_comand(args: argparse.Namespace or None):
    _ = parse_pyckage('add')
    if args and args.modules:
        command['add']().main(args.modules)
    else:
        command['add']().main([])


def init_command(args: argparse.Namespace):
    try:
        with open('pyckage.json'):
            print("You don't need to run this command again!\n"
                  "Use `ppm --help` to see others commands")
            sys.exit(1)
    except FileNotFoundError:
        command['init']().main()


def remove_command(args: argparse.Namespace):
    _ = parse_pyckage('remove')
    if args.modules:
        command['remove']().main(args.modules)
    else:
        command['remove']().main([])


def parse_pyckage(command: str) -> (Dict[str, str], str, str):
    try:
        with open('pyckage.json') as file:
            pyckage = json.load(file)
            try:
                _dependencies = pyckage['dependencies']
            except KeyError:
                _dependencies = {}

            try:
                _run_scripts = pyckage['scripts']
            except KeyError:
                _run_scripts = {}

            try:
                _start_script = _run_scripts['start']
            except KeyError:
                _start_script = None

            return _dependencies, _run_scripts, _start_script
    except FileNotFoundError:
        if command == 'init':
            pass
        else:
            text = utils.BColors.BOLD + utils.BColors.FAIL + 'You should first use `' \
                   + utils.BColors.UNDERLINE + 'ppm init' + utils.BColors.ENDC \
                       + utils.BColors.BOLD + utils.BColors.FAIL + '`.'
            print(text)
            sys.exit(1)


class PythonPackageManager:
    def __init__(self):
        self._parser = create_main_parser()

    def main(self):
        args = self._parser.parse_args()
        if args.cmd:
            args.func(args)
        else:
            add_comand(None)
