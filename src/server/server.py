import os.path
import sys

from src.server.FullTTLCollector import FullTTLCollector
from src.server.IPBookHandler import IPBookHandler
from src.server.ParentServerManager import ParentServerManager
from src.server.ServerDataManager import ServerDataManager
from src.server.UDPServer import UDPServer


def main(argv):
    if len(argv) != 4:
        raise RuntimeError("ERROR: expecting 4 arguments\n")

    myPort = int(argv[0])
    if myPort < 1024 or myPort > 65535:
        raise RuntimeError("ERROR: this server port should be in the range of 1024 - 65535\n")

    parentIp = argv[1]

    parentPort = int(argv[2])
    if (parentPort < 1024 or parentPort > 65535) and (not parentPort == -1):
        raise RuntimeError("ERROR: this parent server port should be in the range of 1024 - 65535 if exists or -1\n")

    ipsFileName = argv[3]
    if not os.path.isfile(ipsFileName):
        raise RuntimeError("ERROR: make sure the ips file path is accordingly to " +
                           "where u run the server. the location u put is: " + ipsFileName + "\n")

    col = FullTTLCollector(ipsFileName)
    fm = ServerDataManager(ipsFileName, col)
    pm = ParentServerManager(parentIp, parentPort)
    ch = IPBookHandler(fm, pm)

    server = UDPServer()
    server.start(myPort, ch)


# Tells the program from where to start running.
if __name__ == "__main__":
    # Passing to the main only the args from the user.
    main(sys.argv[1:])
