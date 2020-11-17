import socket

from src.server.ParentManager import ParentManager


class ParentServerManager(ParentManager):
    BUFFER_SIZE = 1024

    def __init__(self, parentIP: str, parentPort: int):
        self.__parentIP = parentIP
        self.__parentPort = parentPort

    def askParent(self, input: str):
        if self.__parentIP == "-1" or self.__parentPort == -1:
            return self.NOT_FOUND_INFO

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.sendto(input.encode(), (self.__parentIP, self.__parentPort))
        data, addr = s.recvfrom(self.BUFFER_SIZE)

        s.close()
        return str(data)
