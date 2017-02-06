import sys

from ppm.Commands.run import RunCommand
from ppm.utils import BColors


class StartCommand(RunCommand):
	def __init__(self, command: str or list):
		start_output = BColors.BOLD + BColors.OKGREEN + 'Starting: ' + BColors.HEADER + command + BColors.ENDC + '\n'
		super(StartCommand, self).__init__(command=command, start_output=start_output)


# For testing only
if __name__ == '__main__':
	try:
		StartCommand(sys.argv[1])
	except IndexError:
		StartCommand('ls -alF')
