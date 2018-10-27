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
            status = True
        else:
            sock.send("Error: could not find file.")
            status = False

    except sock.error:
        sock.send('Error: could not download file')
        status = False
    sock.close()
    return status


def file_upload(filename, sock):
    '''
    Receives a file from the client and stores it into the server
    '''
    try:
        if os.path.exists(filename):
            sock.send('Error: cannot overwrite file.')
            status = False
        else:
            sock.send('OK')
            filesize = sock.recv(1024)
            # server does not allow zero-sized file
            if filesize == 0:
                sock.send('Error: File cannot have size 0')
                status = False
                sock.close()

            bytes_to_recv = sock.recv(1024)
            file_length = len(bytes_to_recv)
            with open(filename, 'wb') as f:
                while file_length < filesize:
                    f.write(bytes_to_recv)
                    bytes_to_recv = sock.recv(1024)
                    file_length += len(bytes_to_recv)
            status = True

    except sock.error:
        sock.send('Error: could not upload file')
    sock.close()
    return status


def listdirectory(sock):
    #  sends current directory contents
    sock.send(os.listdir())
    sock.close()
    return True


def request_report(cli_addr, cli_port, request, status):
    '''
    print a report of a client request to server terminal
    '''
    if status:
        print('{}:{} {}, Success'.format(cli_addr, cli_port, request))
    else:
        print('{}:{} {}, Failure'.format(cli_addr, cli_port, request))
