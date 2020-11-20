from abc import ABCMeta, abstractmethod

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
