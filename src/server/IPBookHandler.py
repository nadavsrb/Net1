from src.server.ClientHandler import ClientHandler


class IPBookHandler(ClientHandler):
    def __init__(self, fm, pm):
        self.__fm = fm
        self.__pm = pm

    def handleClient(self, input):
        output = self.__fm.getLine(input)

        if output == self.__fm.NO_LINE_FOUND:
            output = self.__pm.askParent()
            self.__fm.addLine(output)

        return output
