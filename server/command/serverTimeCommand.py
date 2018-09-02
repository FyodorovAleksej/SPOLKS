from time import gmtime, strftime

from server.command.serverCommand import ServerCommand


class ServerTimeCommand(ServerCommand):

    def perform_command(self, param_string):
        """
        getting current time in settled format (param_string)
        =====================================================
        :param param_string: time format
        :return: time in input format
        """
        return strftime(param_string, gmtime())

    def is_exit_command(self):
        return False
