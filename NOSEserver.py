import socket

client_ip = input('Enter Client IP: ')
client_port = int(input('Enter Client port: '))

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind()
