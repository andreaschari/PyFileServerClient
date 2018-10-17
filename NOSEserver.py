import socket
import sys
import os


# server IP addr
server_hostname = socket.gethostname()
server_ip = socket.gethostbyname(server_hostname)
print('Server IP: {}'.format(server_ip))
# server port
try:
    listening_port = sys.argv[1]
except OSError:
# server full path
server_path = os.path.dirname(os.path.realpath(__file__)
print('Server Path: {}'.format(server_path))
)
try:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(listening_port)
except Exception as exc:
    print(exc)
    exit(1)
