from abc import ABC


class FileManager:
    __metaclass__ = ABC

    NO_LINE_FOUND = ""

    def getLine(self, key):
        pass

    def addLine(self, line):
        pass
