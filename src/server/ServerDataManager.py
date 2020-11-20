from datetime import datetime

from src.server.FileManager import FileManager
from src.server.TTLCollector import TTLCollector


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
