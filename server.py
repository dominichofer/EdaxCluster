import socket
import sys
from workspread import Server


if __name__ == '__main__':
    #port = int(sys.argv[1])
    port = 12350

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))

    Server().run(sock)
