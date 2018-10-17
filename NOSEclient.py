import socket
import sys

def main():
    try:
        server_addr, server_port, function, filepath = sys.argv
    socketObj = socket.socket()
    socketObj.connect((host, port))

    msg = input(">>")
    while msg != 'q':
        socketObj.send(msg.encode('utf-8'))
        data = socketObj.recv(1024).decode('utf-8')
        print("received from server: {}".format(data))
        msg = input(">>")
    print('terminating connection')
    socketObj.close()


if __name__ == '__main__':
    main()
