from src.server.ClientHandler import ClientHandler
from src.server.FileManager import FileManager
from src.server.ParentManager import ParentManager


# this class stands for the IP book handler.
class IPBookHandler(ClientHandler):
    def __init__(self, fm: FileManager, pm: ParentManager):
        """
        The constructor.
        :param fm: the file manager.
        :param pm: the parent manager.
        """

        self.__fm = fm
        self.__pm = pm

    def handleClient(self, input: str):
        # overriding method

        # searching for the client request in the file.
        output = self.__fm.getLine(input)

        # if the info wasn't found
        if output == self.__fm.NO_LINE_FOUND:

            # searching if the parent has the info.
            output = self.__pm.askParent(input)

            # if the parent had the info learning the info into the file.
            if not output == ParentManager.NOT_FOUND_INFO:
                self.__fm.addLine(output)

        # return the answer to the client.
        return output
