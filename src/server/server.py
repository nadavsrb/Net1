import sys
import os.path
import socket

from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta

"""******************TTLCollector CLASSES******************"""


# this abstract class stands for the ttl collector.
class TTLCollector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def isTTLPassed(self, line: str):
        """
        Checks if the ttl of a line passed.
        :param line: the line to check.
        :return: True if ttl passed, else False.
        """
        pass

    @abstractmethod
    def clean(self):
        """
        Cleans the file from lines witch there ttl passed.
        """
        pass


# this class stands for full ttl collector
class FullTTLCollector(TTLCollector):
    CHAR_BEFORE_TTL = ','

    def __init__(self, ipsFileName: str):
        """
        The constructor.
        :param ipsFileName: the file to clean when needed.
        """
        self.__ipsFileName = ipsFileName

    def isTTLPassed(self, line: str):
        # overriding method

        # delete \n from the line.
        line = line.rstrip('\n')

        # gets the index of the the char before the ttl.
        ttlIndex = line.rfind(self.CHAR_BEFORE_TTL)

        # if true this is not valid line and we
        # would like to clean it
        if ttlIndex == -1:
            return True

        # gets the index of the char after the ttl and before the date.
        dateIndex = line.find(ServerDataManager.CHAR_BEFORE_DATE)

        # if true, than this line wasn't learned and shouldn't be cleaned.
        if dateIndex == -1:
            return False

        # getting the start index of the ttl
        ttlIndex += 1

        # getting the ttl
        ttl = int(line[ttlIndex: dateIndex])

        # getting the start index of the date.
        dateIndex += 1

        # getting the date which the line was learned in.
        dateIn = datetime.strptime(line[dateIndex:], '%Y-%m-%d %H:%M:%S.%f')

        # getting the date which the learned line should be cleaned.
        dateOut = dateIn + timedelta(seconds=ttl)

        # checking if the ttl time passed.
        if dateOut < datetime.now():
            return True

        # if ttl time didn't passed:
        return False

    def clean(self):
        # overriding method

        # opens the file for reading
        with open(self.__ipsFileName, "r") as IPBook:

            # reads the file into lines.
            lines = IPBook.readlines()

        # opens the file for writing.
        with open(self.__ipsFileName, "w") as IPBook:

            # for each line:
            for line in lines:

                # checking if the ttl passed
                if not self.isTTLPassed(line):
                    # if the ttl didn't passed insure
                    # there is '\n' in the end of the line.
                    line = line.rstrip('\n')
                    line += '\n'

                    # writing the line to the file
                    IPBook.write(line)


"""******************FileManager CLASSES******************"""


# this class stand for the file manager.
class FileManager:
    __metaclass__ = ABCMeta

    NO_LINE_FOUND = ""

    @abstractmethod
    def getLine(self, key: str):
        """
        Getting the line witch start with the key.
        :param key: the key to search by.
        :return: the line witch start with the key.
        """
        pass

    @abstractmethod
    def addLine(self, line: str):
        """
        Adding line to the (end of the) file.
        :param line: to add.
        """
        pass


# this class stands for the server data manager
class ServerDataManager(FileManager):
    CHAR_BEFORE_DATE = '|'
    CHAR_AFTER_KEY = ','

    def __init__(self, ipsFileName: str, col: TTLCollector):
        """
        The constructor.
        :param ipsFileName: the name of the file
         which contains the data.
        :param col: the ttl collector.
        """

        self.__ipsFileName = ipsFileName
        self.__col = col

    def getLine(self, key: str):
        # overriding method.

        # making the key valid.
        key += self.CHAR_AFTER_KEY

        # opening the file
        with open(self.__ipsFileName) as IPBook:

            # searching for line which start with the key
            for line in IPBook:

                # if we found line to the key.
                if line.startswith(key):

                    # checking if the ttl passed
                    if self.__col.isTTLPassed(line):
                        # cleans the file by ttl.
                        self.__col.clean()
                        break

                    # if the ttl didn't pass:

                    # getting the index of the char before the date.
                    dateIndex = line.find(self.CHAR_BEFORE_DATE)

                    # if there is a date.
                    # (if there isn't date it's not line which was learned
                    # and we can return it as is).
                    if dateIndex != -1:
                        # deleting the date from the line.
                        line = line[0:dateIndex] + '\n'

                    return line

        # if we didn't find the info:
        return self.NO_LINE_FOUND

    def addLine(self, line: str):
        # overriding method.

        # cleans the file by ttl.
        self.__col.clean()

        # we open the file in the end.
        with open(self.__ipsFileName, 'a') as IPBook:
            # we are adding the date we learned the info to the line.
            line = line.rstrip('\n')
            line += self.CHAR_BEFORE_DATE + str(datetime.now()) + '\n'

            # we are adding the line.
            IPBook.write(line)


"""******************ParentManager CLASSES******************"""


# this abstract class stands for the parent manager.
class ParentManager:
    __metaclass__ = ABCMeta
    NOT_FOUND_INFO = "Info wasn't found"

    @abstractmethod
    def askParent(self, input: str):
        """
        Asking the parent the input.
        :param input: the str to ask the parent.
        :return: the parent's answer.
        """
        pass


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


# this class stands for the IP book handler.
class IPBookHandler(ClientHandler):
    def __init__(self, fm: FileManager, pm: ParentManager):
        """
        The constructor.
        :param fm: the file manager.
        :param pm: the parent manager.
        """

        self.__fm = fm
        self.__pm = pm

    def handleClient(self, input: str):
        # overriding method

        # searching for the client request in the file.
        output = self.__fm.getLine(input)

        # if the info wasn't found
        if output == self.__fm.NO_LINE_FOUND:

            # searching if the parent has the info.
            output = self.__pm.askParent(input)

            # if the parent had the info learning the info into the file.
            if not output == ParentManager.NOT_FOUND_INFO:
                self.__fm.addLine(output)

        # return the answer to the client.
        return output


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


# this class stands for UDP server.
class UDPServer(Server):
    BUFFER_SIZE = 1024

    def start(self, port: int, ch: ClientHandler):
        # overriding method

        # creating the socket, using ipv4 and UDP protocol.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # binding the server to the port.
        # ''= bind to all.
        s.bind(('', port))

        # handling clients.
        while True:
            # receiving massage from client.
            data, addr = s.recvfrom(self.BUFFER_SIZE)

            # getting the answer.
            ans = ch.handleClient(data.decode())

            # sending the answer.
            s.sendto(ans.encode(), addr)


"""******************MAIN FUNCTION******************"""


def main(argv):
    """
    This the main func.
    :param argv: an array of the input of the user.
    """

    # we are expecting 4 inputs.
    if len(argv) != 4:
        raise RuntimeError("ERROR: expecting 4 arguments\n")

    # the first input should be this server's port.
    myPort = int(argv[0])

    # checking the port is valid.
    if myPort < 1024 or myPort > 65535:
        raise RuntimeError("ERROR: this server port should be in the range of 1024 - 65535\n")

    # the second input is the parent server's ip.
    parentIp = argv[1]

    # the third input is the parent server's port.
    parentPort = int(argv[2])

    # here we are checking the parent server's port input is valid.
    if (parentPort < 1024 or parentPort > 65535) and (not parentPort == -1):
        raise RuntimeError("ERROR: this parent server port should be in the range of 1024 - 65535 if exists or -1\n")

    # the ips file name is the fourth argument.
    ipsFileName = argv[3]

    # checking if the file exists.
    if not os.path.isfile(ipsFileName):
        raise RuntimeError("ERROR: make sure the ips file path is accordingly to " +
                           "where u run the server. the location u put is: " + ipsFileName + "\n")

    # creating the ttl collector
    col = FullTTLCollector(ipsFileName)

    # creating the file manager
    fm = ServerDataManager(ipsFileName, col)

    # creating the parent manager
    pm = ParentServerManager(parentIp, parentPort)

    # creating the client handler.
    ch = IPBookHandler(fm, pm)

    # creating and starting the server.
    server = UDPServer()
    server.start(myPort, ch)


# Tells the program from where to start running.
if __name__ == "__main__":
    # Passing to the main only the args from the user.
    main(sys.argv[1:])
