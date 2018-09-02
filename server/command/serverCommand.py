from abc import ABCMeta, abstractmethod


# interface of server command
class ServerCommand:
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform_command(self, param_string):
        """
        perform command
        ===============
        :param param_string: string after command (arguments)
        :return: result of performing command
        """
        raise NotImplementedError("command method perform is not implemented")

    @abstractmethod
    def is_exit_command(self):
        """
        :return: is this exit command?
        """
        raise NotImplementedError("is exit method perform is not implemented")