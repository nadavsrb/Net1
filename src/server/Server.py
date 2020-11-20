from abc import ABCMeta, abstractmethod

from src.server.ClientHandler import ClientHandler

"""******************SERVER CLASSES******************"""


# this abstract class stand for server.
class Server:
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self, port: int, ch: ClientHandler):
        """
        Starting the server.
        :param port: the server's port.
        :param ch: the client handler.
        """
        pass
