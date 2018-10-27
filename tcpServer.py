import socket
import sys
import os


def file_download(filename, sock):
    '''
    Sends a file from the server and sends it to the client
    '''
    try:
        if os.path.isfile(filename):
            sock.send('EXISTS: {}'.format(os.path.getsize(filename)))
            client_response = sock.recv(1024)
            if client_response[:2] == 'OK':
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    sock.send(bytes_to_send)
                    while bytes_to_send != '':
                        bytes_to_send = f.read(1024)
                        sock.send(bytes_to_send)
        else:
            sock.send("Error: could not find file.")
    except sock.error:
        sock.send('Error: could not download file')
    sock.close()


def file_upload(filename, sock):
    '''
    Receives a file from the client and stores it into the server
    '''
    try:
        if os.path.exists(filename):
            sock.send('Error: cannot overwrite file.')
        else:
            sock.send('OK')
            filesize = sock.recv(1024)
            bytes_to_recv = sock.recv(1024)
            file_length = len(bytes_to_recv)
            with open(filename, 'wb') as f:
                while file_length < filesize:
                    f.write(bytes_to_recv)
                    bytes_to_recv = sock.recv(1024)
                    file_length += len(bytes_to_recv)
            sock.send('UPLOADED')
    except sock.error:
        sock.send('Error: could not upload file')
    sock.close()


def listdirectory(sock):
    #  sends current directory contents
    sock.send(os.listdir())
    sock.close()


def main():

    try:
        # sys.argv[1] is the port number
        # server will listen for connections on input port
        srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_sock.bind(('0.0.0.0', int(sys.argv[1])))
        srv_sock.listen(5)
    except Exception as e:
        print(e)
        exit(1)

    while True:
        try:
            print("Waiting for new client... ")
            cli_sock, cli_addr = srv_sock.accept()
            # Translate the client address to a string (to be used shortly)
            cli_addr_str = str(cli_addr)
            print("Client " + cli_addr_str + " connected.")

            while True:
                command = srv_sock.recv(1024)
                if command[:3].lower() == 'get':
                    file_download(command[4:], cli_sock)
                elif command[:3].lower() == 'put':
                    file_upload(command[4:], cli_sock)
                elif command[:4].lower() == 'list':
                    listdirectory()
                else:
                    cli_sock.send()
        finally:
            """
             If an error occurs or the client closes the connection,
             call close() on the connected socket
             to release the resources allocated to it by the OS.
            """
            print('Connection Terminated.')
            cli_sock.close()
    # Close the server socket as well to release its resources back to the OS
    srv_sock.close()
    # Exit with a zero value, to indicate success
    exit(0)


if __name__ == '__main__':
    main()
