from abc import ABCMeta, abstractmethod

"""******************ParentManager CLASSES******************"""


# this abstract class stands for the parent manager.
class ParentManager:
    __metaclass__ = ABCMeta
    NOT_FOUND_INFO = "Info wasn't found"

    @abstractmethod
    def askParent(self, input: str):
        """
        Asking the parent the input.
        :param input: the str to ask the parent.
        :return: the parent's answer.
        """
        pass
