import socket

from src.server.ClientHandler import ClientHandler
from src.server.Server import Server


class UDPServer(Server):
    BUFFER_SIZE = 1024

    def start(self, port: int, ch: ClientHandler):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # ''= bind to all
        s.bind(('', port))

        while True:
            data, addr = s.recvfrom(self.BUFFER_SIZE)

            ans = ch.handleClient(data.decode())

            s.sendto(ans.encode(), addr)
