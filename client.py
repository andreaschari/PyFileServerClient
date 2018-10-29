import socket
import sys
from functions import *


def main():
    server_addr = sys.argv[1]
    server_port = sys.argv[2]
    function = sys.argv[3]
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv_sock.connect((server_addr, int(server_port)))

    if function == 'get':
        filepath = sys.argv[4]
        commandline = function + ' ' + filepath
        srv_sock.send(commandline.encode())
        file_receive(filepath, srv_sock)
    elif function == 'put':
        filepath = sys.argv[4]
        commandline = function + ' ' + filepath
        srv_sock.send(commandline.encode())
        file_sent(filepath, srv_sock)
    elif function == 'list':
        srv_sock.send(b'list')
        data = srv_sock.recv(1024)
        while data != b'':
            print(data.decode())
            data = srv_sock.recv(1024)

    else:
        print('Error: Invalid function')


if __name__ == '__main__':
    main()
