from src.server.ClientHandler import ClientHandler
from src.server.FileManager import FileManager
from src.server.ParentManager import ParentManager


class IPBookHandler(ClientHandler):
    def __init__(self, fm: FileManager, pm: ParentManager):
        self.__fm = fm
        self.__pm = pm

    def handleClient(self, input: str):
        output = self.__fm.getLine(input)

        if output == self.__fm.NO_LINE_FOUND:
            output = self.__pm.askParent(input)
            self.__fm.addLine(output)

        return output
