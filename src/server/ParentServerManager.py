import socket

from src.server.ParentManager import ParentManager


# this class stand for the Parent Server Manager
class ParentServerManager(ParentManager):
    BUFFER_SIZE = 1024

    def __init__(self, parentIP: str, parentPort: int):
        """
        The constructor.
        :param parentIP: the parent server's ip.
        :param parentPort: the parent server's port.
        """

        self.__parentIP = parentIP
        self.__parentPort = parentPort

    def askParent(self, input: str):
        # checking if parent exists.
        if self.__parentIP == "-1" or self.__parentPort == -1:
            return self.NOT_FOUND_INFO

        # creating the socket using ipv4 and UDP protocol.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # asking & getting the answer
        s.sendto(input.encode(), (self.__parentIP, self.__parentPort))
        data, addr = s.recvfrom(self.BUFFER_SIZE)

        # closing the socket.
        s.close()

        # converting the answer to str & returning it.
        return data.decode()
