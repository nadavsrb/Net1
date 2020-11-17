from abc import ABCMeta, abstractmethod


class ParentManager:
    __metaclass__ = ABCMeta
    NOT_FOUND_INFO = "Info wasn't found"

    @abstractmethod
    def askParent(self, input: str):
        pass
