from ppm import utils
from ppm.Commands.run import RunCommand


class StartCommand(RunCommand):
    def __init__(self):
        super(StartCommand, self).__init__()

    def main(self):
        if self._start:
            start_output = utils.BColors.BOLD + utils.BColors.OKGREEN + 'Starting: ' \
                           + utils.BColors.HEADER + self._start + utils.BColors.ENDC
            super(StartCommand, self).main(self._start, start_output)
        else:
            print(utils.BColors.FAIL + 'ERROR: start command is not defined in pyckage.json. To use this command, '
                                       'please define one.')
