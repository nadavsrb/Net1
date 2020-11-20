import os.path
import sys

from src.server.FullTTLCollector import FullTTLCollector
from src.server.IPBookHandler import IPBookHandler
from src.server.ParentServerManager import ParentServerManager
from src.server.ServerDataManager import ServerDataManager
from src.server.UDPServer import UDPServer

"""******************MAIN FUNCTION******************"""


def main(argv):
    """
    This the main func.
    :param argv: an array of the input of the user.
    """

    # we are expecting 4 inputs.
    if len(argv) != 4:
        raise RuntimeError("ERROR: expecting 4 arguments\n")

    # the first input should be this server's port.
    myPort = int(argv[0])

    # checking the port is valid.
    if myPort < 1024 or myPort > 65535:
        raise RuntimeError("ERROR: this server port should be in the range of 1024 - 65535\n")

    # the second input is the parent server's ip.
    parentIp = argv[1]

    # the third input is the parent server's port.
    parentPort = int(argv[2])

    # here we are checking the parent server's port input is valid.
    if (parentPort < 1024 or parentPort > 65535) and (not parentPort == -1):
        raise RuntimeError("ERROR: this parent server port should be in the range of 1024 - 65535 if exists or -1\n")

    # the ips file name is the fourth argument.
    ipsFileName = argv[3]

    # checking if the file exists.
    if not os.path.isfile(ipsFileName):
        raise RuntimeError("ERROR: make sure the ips file path is accordingly to " +
                           "where u run the server. the location u put is: " + ipsFileName + "\n")

    # creating the ttl collector
    col = FullTTLCollector(ipsFileName)

    # creating the file manager
    fm = ServerDataManager(ipsFileName, col)

    # creating the parent manager
    pm = ParentServerManager(parentIp, parentPort)

    # creating the client handler.
    ch = IPBookHandler(fm, pm)

    # creating and starting the server.
    server = UDPServer()
    server.start(myPort, ch)


# Tells the program from where to start running.
if __name__ == "__main__":
    # Passing to the main only the args from the user.
    main(sys.argv[1:])
