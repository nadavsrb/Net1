from abc import ABC, abstractmethod


class Server(ABC):

    @abstractmethod
    def start(self, port, ch):
        pass
