from abc import ABCMeta, abstractmethod


class Command:
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform_command(self, param_string):
        raise NotImplementedError("command method perform is not implemented")

    @abstractmethod
    def is_exit_command(self):
        raise NotImplementedError("is exit method perform is not implemented")