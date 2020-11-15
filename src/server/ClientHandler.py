from abc import ABCMeta, abstractmethod


class ClientHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handleClient(self, input):
        pass
