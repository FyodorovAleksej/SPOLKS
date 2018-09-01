from time import gmtime, strftime

from command import Command


class TimeCommand(Command):

    def perform_command(self, param_string):
        return strftime(param_string, gmtime())

    def is_exit_command(self):
        return False
