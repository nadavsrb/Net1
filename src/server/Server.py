from abc import ABCMeta, abstractmethod


class Server():
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, port, ch):
        pass
