from abc import ABCMeta


class FileManager:
    __metaclass__ = ABCMeta

    NO_LINE_FOUND = ""

    def getLine(self, key: str):
        pass

    def addLine(self, line: str):
        pass
