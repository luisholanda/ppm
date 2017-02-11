import shlex
import subprocess
import sys

from ppm import utils


class RunCommand:
	def __init__(self):
		# Setup argsparser
		pass

	def main(self, command: str or list, start_output: str = ''):
		if start_output:
			utils.write(start_output)

		try:
			command_with_args = shlex.split(command)
		except AttributeError:
			command_with_args = command

		self.run(command_with_args)

	@staticmethod
	def run(command: list):
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

		stdout = iter(process.stdout.readline, b'')
		for line in stdout:
			utils.write(line.decode())


if __name__ == '__main__':
	utils.set_env()
	cmd = RunCommand()
	try:
		cmd.main(sys.argv[1:])
	except IndexError:
		cmd.main('ls -alF')
