#!/usr/bin/python

import socket
import sys
import os
import time
import argparse
import threading

def  file_receive(s, fp2, port):

    """
    This module takes socket, file-pointer and port number as arguments. Also opens a socket and accepts incoming connection request on the specified port.
    This module receives file from the remote host and writes received contents to the local file descriptor.
    """
    s.bind(('',port))
    s.listen(1)
    i = fp2.tell()
    connection, client_address = s.accept()
    try:
        while True:
            data = connection.recv(10000)
            if not data:
                break
            fp2.write(data)
            i = fp2.tell()

    finally:
        s.close()

def file_transfer_handshake(s, port):

    """
    This module for initial application handshake, where filename, filesize and split-size are exchanged.
    """
    s.bind(('',port))
    s.listen(1)
    connection, client_address = s.accept()
    time.sleep(1)
    data = connection.recv(1024)
    parameters = data.split("+")
    s.close()
    connection.close()
    filename = parameters[0]
    file_size = int(parameters[1])
    split_size = int(parameters[2])
  
    return (filename, file_size, split_size)


if __name__ == "__main__":


    parser=argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Specify the destination port", required=True)
    args = parser.parse_args()
    port = args.port
    print "File receiver started" 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dst_file, file_size, split_size = file_transfer_handshake(s, port)
    print "Receiving file : %s \nReceiving file-size : %d\nFile-split streams : %d" % (dst_file, file_size, split_size)
    dst_fp = list()
    dst_sock = list()

    i = 0
    for i in range(0,split_size):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dst_sock.append(s)
        offset = i*(file_size//split_size)
        origin = 1
        fp2 = open(dst_file, "wb")
        fp2.seek(offset, origin)
        dst_fp.append(fp2)

    jobs = []
    for i in range(0,split_size):
        th = threading.Thread(target=file_receive, name='Thread-1', args=(dst_sock[i], dst_fp[i],port))
        port = port+1
        jobs.append(th)

    for t in jobs:
        t.start()

    for t in jobs:
        t.join()

    time.sleep(1)
    stat = os.stat(dst_file)
    if threading.active_count() == 1:
        print "file copied successfully"
        sys.exit()
    else:
        print "file copy might have failed. Please check once for the integrity of the file before re-copying it." 
        sys.exit()


