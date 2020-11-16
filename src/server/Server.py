from abc import ABCMeta, abstractmethod

from src.server.ClientHandler import ClientHandler


class Server:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, port: int, ch: ClientHandler):
        pass
