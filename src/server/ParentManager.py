from abc import ABC, abstractmethod


class ParentManager:
    __metaclass__ = ABC

    @abstractmethod
    def askParent(self, input):
        pass
