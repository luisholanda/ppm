import sys

from ppm import utils
from ppm.Commands.run import RunCommand


class StartCommand(RunCommand):
	def __init__(self):
		super(StartCommand, self).__init__()

	def start(self, command: str or list):
		start_output = utils.BColors.BOLD + utils.BColors.OKGREEN + 'Starting: ' + utils.BColors.HEADER + command \
		               + utils.BColors.ENDC + '\n'
		self.main(command, start_output)

# For testing only
if __name__ == '__main__':
	utils.set_env()
	try:
		StartCommand(sys.argv[1])
	except IndexError:
		StartCommand('ls -alF')
