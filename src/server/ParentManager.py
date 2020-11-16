from abc import ABCMeta, abstractmethod


class ParentManager:
    __metaclass__ = ABCMeta

    @abstractmethod
    def askParent(self, input: str):
        pass
