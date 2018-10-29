import os


def file_sent(filename, sock):
    '''
    Sents a file as a stream of bytes from a socket
    '''
    status = False
    try:
        if os.path.isfile(filename):
            filesize = os.path.getsize(filename)
            if filesize != 0:
                sock.send(str(filesize).encode())
                with open(filename, 'rb') as f:
                    bytes_to_send = f.read(1024)
                    while len(bytes_to_send) != 0:
                        sock.send(bytes_to_send)
                        bytes_to_send = f.read(1024)
                print('File {}, size: {} sent'.format(filename, filesize))
                status = True
            else:
                print('Error: cannot sent empty file.')
        else:
            print('Error: could not find file.')

    except Exception as e:
        print(e)
    return status


def file_receive(filename, sock):
    '''
    Receives a file as a stream of bytes to a socket
    '''
    status = False
    try:
        # cannot allow overwriting files
        if os.path.exists(filename):
            print('Error: cannot overwrite file.')
        else:
            filesize = sock.recv(1024)
            filesize = int(filesize.decode())
            # server does not allow zero-sized files to be transferred
            if filesize == 0:
                print('Error: File cannot have size 0')

            file_length = 0
            with open(filename, 'wb') as f:
                while file_length < filesize:
                    bytes_to_recv = sock.recv(1024)
                    f.write(bytes_to_recv)
                    file_length += len(bytes_to_recv)
            print('file {} received, size: {}'.format(filename, filesize))
            status = True
    except Exception as e:
        print(e)
    return status


def listdirectory(sock):
    #  sends current directory contents
    for stuff in os.listdir():
        print(stuff)
        sock.send(stuff.encode())
    return True


def request_report(cli_addr, cli_port, request, status):
    '''
    print a report of a client request to server terminal
    '''
    if status:
        print('Report: {} {}, Success'.format(cli_addr, request))
    else:
        print('Report: {} {}, Failure'.format(cli_addr, request))
