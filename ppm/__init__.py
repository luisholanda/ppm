from ppm.Commands.add import AddCommand
from ppm.Commands.run import RunCommand
from ppm.Commands.start import StartCommand

COMMAND_LIST = {
	'start': StartCommand,
	'run'  : RunCommand,
	'add'  : AddCommand
}
