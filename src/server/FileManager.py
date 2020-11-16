from abc import ABCMeta


class FileManager:
    __metaclass__ = ABCMeta

    NO_LINE_FOUND = ""

    def getLine(self, key):
        pass

    def addLine(self, line):
        pass
