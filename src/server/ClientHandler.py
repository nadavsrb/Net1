from abc import ABCMeta, abstractmethod

"""******************ClientHandler CLASSES******************"""


# this abstract class stands for client handler.
class ClientHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def handleClient(self, input: str):
        """
        This method handles client.
        :param input: the str request from the client.
        :return: the answer (str) to the client.
        """
        pass
