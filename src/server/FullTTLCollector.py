from datetime import datetime, timedelta

from src.server.ServerDataManager import ServerDataManager
from src.server.TTLCollector import TTLCollector


class FullTTLCollector(TTLCollector):
    CHAR_BEFORE_TTL = ','

    def __init__(self, ipsFileName: str):
        self.__ipsFileName = ipsFileName

    def isTTLPassed(self, line: str):
        line = line.rstrip('\n')

        dateIndex = line.find(ServerDataManager.CHAR_BEFORE_DATE)
        if dateIndex == -1:
            return False

        ttlIndex = line.rfind(self.CHAR_BEFORE_TTL)

        # if true this is not valid line and we
        # would like to clean it
        if ttlIndex == -1:
            return True

        ttl = int(line[++ttlIndex: dateIndex])
        dateIn = datetime.strptime(line[++dateIndex:], '%Y-%m-%d %H:%M:%S.%f')

        dateOut = dateIn + timedelta(seconds=ttl)
        now = datetime.now()

        if dateOut > now:
            return True

        return False

    def clean(self):
        with open(self.__ipsFileName, "r") as IPBook:
            lines = IPBook.readlines()

        with open(self.__ipsFileName, "w") as IPBook:
            for line in lines:
                if not self.isTTLPassed(line):
                    IPBook.write(line)
