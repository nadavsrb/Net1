from abc import ABCMeta, abstractmethod


class TTLCollector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def isTTLPassed(self, line: str):
        pass

    @abstractmethod
    def clean(self):
        pass
