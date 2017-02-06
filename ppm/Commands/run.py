import shlex
import subprocess
import sys

from ppm.utils import write


class RunCommand:
	def __init__(self, command: str or list, start_output: str = ''):
		if start_output:
			write(start_output)

		command_with_args = shlex.split(command)

		self.run(command_with_args)

	def run(self, command: list):
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

		while True:
			output = process.stdout.readline().decode('utf-8')
			err = process.stderr.readlines()

			if err:
				for error in err:
					write(error.decode('utf-8'))

			if process.poll() is not None:
				break
			elif output != '':
				write(output)


if __name__ == '__main__':
	try:
		RunCommand(sys.argv[1])
	except IndexError:
		RunCommand('ls -alF')