import sys
import socket

from abc import ABCMeta, abstractmethod


class Client:
    __metaclass__ = ABCMeta

    @abstractmethod
    def askServer(self, serverIp: str, serverPort: int, ques: str):
        pass


class UDPClient(Client):
    BUFFER_SIZE = 1024

    def askServer(self, serverIp: str, serverPort: int, ques: str):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        s.sendto(ques.encode(), (serverIp, serverPort))
        data, addr = s.recvfrom(self.BUFFER_SIZE)

        s.close()

        return data.decode()


class Task:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do(self, input):
        pass


class ClientTask(Task):
    SEPARATING_CHAR = ','

    def __init__(self, cl: Client, serverIp: str, serverPort: int):
        self.__cl = cl
        self.__serverIp = serverIp
        self.__serverPort = serverPort

    def do(self, input: str):
        ans = self.__cl.askServer(self.__serverIp, self.__serverPort, input)

        firstIndex = ans.find(self.SEPARATING_CHAR) + 1
        lastIndex = ans.rfind(self.SEPARATING_CHAR)

        if firstIndex == -1 or lastIndex == -1:
            print(ans)
            return;

        print(ans[firstIndex:lastIndex])


def main(argv):
    if len(argv) != 2:
        raise RuntimeError("ERROR: expecting 2 arguments\n")

    serverIp = argv[0]

    serverPort = int(argv[1])
    if serverPort < 1024 or serverPort > 65535:
        raise RuntimeError("ERROR: serverPort should be in the range of 1024 - 65535\n")

    client = UDPClient()
    task = ClientTask(client, serverIp, serverPort)

    while True:
        task.do(input())


if __name__ == "__main__":
    main(sys.argv[1:])
