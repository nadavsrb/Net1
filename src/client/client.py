import sys
import socket

from abc import ABCMeta, abstractmethod

"""******************CLIENT CLASSES******************"""


# This abstract class stands for client.
class Client:
    __metaclass__ = ABCMeta

    @abstractmethod
    def askServer(self, serverIp: str, serverPort: int, ques: str):
        """
        This func ask the server the ques.
        :param serverIp:  the server's ip.
        :param serverPort: the server's port.
        :param ques: the question to ask the server.
        :return: the answer from the server.
        """
        pass


# This class stands for UDP Client.
class UDPClient(Client):
    BUFFER_SIZE = 1024

    def askServer(self, serverIp: str, serverPort: int, ques: str):
        # override method

        # creating the socket, using ipv4 and UDP protocol.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # asking the server, and getting the answer.
        s.sendto(ques.encode(), (serverIp, serverPort))
        data, addr = s.recvfrom(self.BUFFER_SIZE)

        # closing the socket.
        s.close()

        # convert the answer to str and returning it.
        return data.decode()


"""******************TASK CLASSES******************"""


# This abstract class stand for tasks.
class Task:
    __metaclass__ = ABCMeta

    @abstractmethod
    def do(self, input: str):
        """
        The do func of the task.
        :param input: the str input for the task.
        """
        pass


# This class stand for client task = as defined in the exercise.
class ClientTask(Task):
    SEPARATING_CHAR = ','

    def __init__(self, cl: Client, serverIp: str, serverPort: int):
        """
        The constructor.
        :param cl: the client.
        :param serverIp: the server's ip.
        :param serverPort: the server's port.
        """

        self.__cl = cl
        self.__serverIp = serverIp
        self.__serverPort = serverPort

    def do(self, input: str):
        # override method

        # asking the server and storing the answer.
        ans = self.__cl.askServer(self.__serverIp, self.__serverPort, input)

        # storing the index of the start substring witch contains the ip.
        firstIndex = ans.find(self.SEPARATING_CHAR) + 1

        # storing the index of the first char after the substring witch contains the ip.
        lastIndex = ans.rfind(self.SEPARATING_CHAR)

        # if the answer returns don't in the structure
        # so in our case it's must be an answer of unfounded info.
        if firstIndex == -1 or lastIndex == -1:
            print(ans)
            return

        # we are printing the ip substring of the answer.
        print(ans[firstIndex:lastIndex])


"""******************MAIN FUNCTION******************"""


def main(argv):
    """
    This the main func.
    :param argv: an array of the input of the user.
    """

    # we are expecting two inputs
    if len(argv) != 2:
        raise RuntimeError("ERROR: expecting 2 arguments\n")

    # the first input should be the server's ip.
    serverIp = argv[0]

    # the second input should be the server's port.
    serverPort = int(argv[1])

    # we are checking that the port entered is valid.
    if serverPort < 1024 or serverPort > 65535:
        raise RuntimeError("ERROR: serverPort should be in the range of 1024 - 65535\n")

    # we are crating the var that would manage the tasks.
    client = UDPClient()
    task = ClientTask(client, serverIp, serverPort)

    # we are doing the tasks.
    while True:
        task.do(input())


# Tells the program from where to start running.
if __name__ == "__main__":
    # Passing to the main only the args from the user.
    main(sys.argv[1:])
