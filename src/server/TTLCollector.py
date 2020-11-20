from abc import ABCMeta, abstractmethod

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
