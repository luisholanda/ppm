import json
import shlex
import subprocess
import sys

from ppm import utils


class RunCommand:
    def __init__(self):
        with open('pyckage.json') as fp:
            pyck = json.load(fp)
            try:
                self._scripts = pyck['scripts']
            except KeyError:
                print('You should have scripts options stored in pyckage.json to use this command')
                sys.exit(1)
            try:
                self._start = self._scripts['start']
            except KeyError:
                self._start = None

    def main(self, args: str, start_output: str = ''):
        if start_output:
            print(start_output, '\n')
        else:
            print(utils.BColors.BOLD + utils.BColors.OKGREEN + 'Running:',
                  utils.BColors.HEADER, self._start, utils.BColors.ENDC, '\n')


        try:
            command_with_args = shlex.split(args)
        except AttributeError:
            command_with_args = args

        self.run(command_with_args)

    @staticmethod
    def run(command: str):
        env = utils.set_env()

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)

        stdout = iter(process.stdout.readline, b'')
        for line in stdout:
            utils.write(line.decode())
