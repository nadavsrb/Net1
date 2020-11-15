import socket

from src.server.ParentManager import ParentManager


class ParentServerManager(ParentManager):
    BUFFER_SIZE = 1024

    def __init__(self, parentIP, parentPort):
        self.__parentIP = parentIP
        self.__parentPort = parentPort

    def askParent(self, input):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.sendto(input, (self.__parentIP, self.__parentPort))
        data, addr = s.recvfrom(self.BUFFER_SIZE)

        s.close()
        return data
