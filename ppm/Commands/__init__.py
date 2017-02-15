# Don't read this :)
from ppm import Commands

command = {
    'add'   : Commands.add.AddCommand,
    'init'  : Commands.init.InitCommand,
    'remove': Commands.remove.RemoveCommand,
    'run'   : Commands.run.RunCommand,
    'start' : Commands.start.StartCommand
}
