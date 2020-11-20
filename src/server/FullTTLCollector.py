from datetime import datetime, timedelta

from src.server.ServerDataManager import ServerDataManager
from src.server.TTLCollector import TTLCollector


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
