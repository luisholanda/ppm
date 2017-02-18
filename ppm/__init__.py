import argparse
import json
import sys
from typing import Dict

from ppm import utils
from ppm.Commands import command

__version__ = '0.1.1'


def create_main_parser() -> argparse.ArgumentParser:
    prog = 'ppm'
    description = """
        This program helps you create Python projects and handle their dependencies.
    """
    epilog = '''Run `ppm COMMAND --help` for more information on specific commands.'''
    usage = '%(prog)s [<command>] [-h] [<args>]'

    parser = argparse.ArgumentParser(
        prog=prog,
        description=description,
        usage=usage,
        epilog=epilog
    )

    subparser = parser.add_subparsers(
        title='Commands',
        metavar='',
        dest='cmd'
    )

    # Add subparser
    add_parser = subparser.add_parser('add',
                                      aliases=['a'],
                                      help='install Python packages',
                                      usage='ppm {add, a} [-h] [--add] [-g] [<modules>]',
                                      description="""
        Easily install Python packages and add them to pyckage.json dependencies.
        If no module is passed, this command will install all dependencies from pyckage.json
                                      """)
    add_parser.add_argument('--add',
                            help="add the packages to pyckage.json",
                            action='store_true')
    add_parser.add_argument('-g',
                            help="install the packages globally",
                            action='store_true')
    add_parser.add_argument('modules',
                            help="packages that will be installed",
                            nargs=argparse.ZERO_OR_MORE)
    add_parser.set_defaults(func=add_comand)

    # Init subparser
    init_parser = subparser.add_parser('init',
                                       aliases=['i'],
                                       help='initialize a Python package with a pyckage.json',
                                       usage='ppm {init, i} [-h]',
                                       description="""
        Easily initialize Python packages and make a initial pyckage.json
                                       """)
    init_parser.set_defaults(func=init_command)

    # Remove subparser
    remove_parser = subparser.add_parser('remove',
                                         aliases=['rm'],
                                         help='remove packages installed at python_modules folder',
                                         usage='ppm {remove, rm} [-h] [-g] <modules>',
                                         description="""
        Remove local installed Python packages and remove them from pyckage.json
                                         """)
    remove_parser.add_argument('modules',
                               help='packages that will be removed',
                               nargs=argparse.ZERO_OR_MORE)
    remove_parser.add_argument('-g',
                               help='remove globally installed packages',
                               action='store_true')
    remove_parser.set_defaults(func=remove_command)

    # Run subparser
    run_parser = subparser.add_parser('run',
                                      help='run scripts detailed in pyckage.json',
                                      usage='ppm run [-h] <script>',
                                      description="""
        Run commands that are specified in scripts field of pyckage.json
                                      """)
    run_parser.add_argument('script',
                            help="name of the script that will be executed",
                            nargs=1)
    run_parser.set_defaults(func=run_command)

    # Start subparser
    start_parser = subparser.add_parser('start',
                                        aliases=['st'],
                                        help='run the start script',
                                        usage='ppm {start, st} [-h]',
                                        description="""
        Start the script `start` detailed in pyckage.json
                                        """)
    start_parser.set_defaults(func=start_command)

    return parser


def add_comand(args: argparse.Namespace or None):
    if not args.g:
        _ = parse_pyckage('add')

    if args and args.modules:
        command['add']().main(args.modules, args.add, args.g)
    else:
        command['add']().main([])


def init_command(_: argparse.Namespace):
    try:
        with open('pyckage.json'):
            print("You don't need to run this command again!\n"
                  "Use `ppm --help` to see others commands")
            sys.exit(1)
    except FileNotFoundError:
        command['init']().main()


def remove_command(args: argparse.Namespace):
    if not args.g:
        _ = parse_pyckage('remove')

    if args.modules:
        command['remove']().main(args.modules, args.g)
    else:
        command['remove']().main([], args.g)


def run_command(args: argparse.Namespace):
    _, scripts, _ = parse_pyckage('run')
    script = args.script[0]

    if script in scripts.keys():
        command['run']().main(scripts[script])
    elif script:
        print(utils.BColors.FAIL + f"Command `{script}` doesn't exists in pyckage.json", utils.BColors.ENDC)


def start_command(args: argparse.Namespace):
    _ = parse_pyckage('start')
    command['start']().main()


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
        print(utils.BColors.BOLD, f'ppm v{__version__}:', utils.BColors.ENDC)
        args = self._parser.parse_args()
        if args.cmd:
            args.func(args)
        else:
            add_comand(None)


def main():
    sys.path.append(utils.MODULES_FOLDER)
    ppm = PythonPackageManager()
    ppm.main()
