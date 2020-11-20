import socket

from src.server.ClientHandler import ClientHandler
from src.server.Server import Server


# this class stands for UDP server.
class UDPServer(Server):
    BUFFER_SIZE = 1024

    def start(self, port: int, ch: ClientHandler):
        # overriding method

        # creating the socket, using ipv4 and UDP protocol.
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # binding the server to the port.
        # ''= bind to all.
        s.bind(('', port))

        # handling clients.
        while True:
            # receiving massage from client.
            data, addr = s.recvfrom(self.BUFFER_SIZE)

            # getting the answer.
            ans = ch.handleClient(data.decode())

            # sending the answer.
            s.sendto(ans.encode(), addr)
