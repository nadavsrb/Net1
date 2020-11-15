from abc import ABC, abstractmethod


class ClientHandler(ABC):

    @abstractmethod
    def handleClient(self, input):
        pass
