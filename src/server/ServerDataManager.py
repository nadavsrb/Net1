from datetime import datetime

from src.server.FileManager import FileManager
from src.server.TTLCollector import TTLCollector


class ServerDataManager(FileManager):
    CHAR_BEFORE_DATE = '|'

    def __init__(self, ipsFileName: str, col: TTLCollector):
        self.__ipsFileName = ipsFileName
        self.__col = col

    def getLine(self, key: str):
        with open(self.__ipsFileName) as IPBook:
            for line in IPBook:
                if line.startswith(key):
                    if self.__col.isTTLPassed(line):
                        self.__col.clean()
                        break

                    dateIndex = line.find(self.CHAR_BEFORE_DATE)
                    if dateIndex != -1:
                        line = line[0:dateIndex] + '\n'

                    return line

        return self.NO_LINE_FOUND

    def addLine(self, line: str):
        self.__col.clean()

        with open(self.__ipsFileName, 'a') as IPBook:
            line = line.rstrip('\n')
            line += self.CHAR_BEFORE_DATE + str(datetime.now()) + '\n'
            IPBook.write(line)
