import json
import shlex
import subprocess
import sys

from ppm import utils


class RunCommand:
    def __init__(self):
        # Setup argsparser
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

    def main(self, command: str, start_output: str = ''):
        if start_output:
            utils.write(start_output)

        try:
            command_with_args = shlex.split(command)
        except AttributeError:
            command_with_args = command

        self.run(command_with_args)

    @staticmethod
    def run(command: str):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        stdout = iter(process.stdout.readline, b'')
        for line in stdout:
            utils.write(line.decode())
