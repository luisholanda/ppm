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

		command_with_args = shlex.split(command)

		self.run(command_with_args)

	@staticmethod
	def run(command: list):
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		while True:
			output = process.stdout.readline().decode('utf-8')
			err = process.stderr.readlines()

			if err:
				for error in err:
					utils.write(error.decode('utf-8'))

			if process.poll() is not None:
				break
			elif output != '':
				utils.write(output)


if __name__ == '__main__':
	utils.set_env()
	try:
		RunCommand(sys.argv[1])
	except IndexError:
		RunCommand('ls -alF')
