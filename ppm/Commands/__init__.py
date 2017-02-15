# Don't read this :)
from ppm.Commands import add, init, remove, run, start

command = {
    'add'   : add.AddCommand,
    'init'  : init.InitCommand,
    'remove': remove.RemoveCommand,
    'run'   : run.RunCommand,
    'start' : start.StartCommand
}
