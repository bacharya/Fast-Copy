#!/usr/bin/python

import socket
import sys
import os
import time
from threading import Thread
import argparse


def  file_copy(fp1, fp2, host, port):

    """ 
    This method takes local file pointer and offset along with remote hostname and port as arguments.
    Also this module reads line-by-line from current file-pointer till offset and writes the line to the socket-buffer.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    i = fp1.tell()
   
    try:
        for line in fp1:
            if i >= fp2:
                break
            s.send(line)
            i = i+len(line)

    finally:
        s.close()

def file_transfer_handshake(host, port, filename, file_size, split_size):

    """
    This module for initial application handshake, where filename, filesize and split-size are exchanged.
    """
    fname = filename.split("/")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))    

    data = fname[-1]+"+"+str(file_size)+"+"+str(split_size)
    length = s.send(data)

    s.close()

if __name__ == '__main__' :


    parser=argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", type=str, help="Specify the filename for copying", required=True)
    parser.add_argument("-H", "--host", type=str, help="Specify the target host or ip address of the host", required=True)
    parser.add_argument("-p", "--port", type=int, help="Specify the destination port", required=True)
    parser.add_argument("-s", "--splitsize", type=int, help="Specify the number of split-size for simultaneous copy", default=10)
    parser.add_argument("-l", "--localfile", type=str, help="Specify local file", default="copied")
    args = parser.parse_args()

    split_size = args.splitsize
    src_file = args.filename
    dst_file = args.localfile
    host = args.host
    port = args.port

    stat = os.stat(src_file)

    print "file size is {}".format(stat.st_size) 
    file_transfer_handshake(host, port, src_file, stat.st_size, split_size)
    time.sleep(2)
    src_fp = list()
    dst_fp = list()

    start = time.localtime()
    print time.strftime("%y-%m-%d %H%M%S", start) 
    i = 0
    for i in range(0,split_size):
        fp1 = open(src_file, "rb")
        offset = i*(stat.st_size//split_size)
        origin = 1
        fp1.seek(offset, origin)
        src_fp.append(fp1)
        dst_fp.append(((i+1)*(stat.st_size//split_size)-1))
        if i == (split_size-1):
            dst_fp[i] = stat.st_size

    jobs = []
    for i in range(0,split_size):
        th1 = Thread(target=file_copy, name='Thread-1', args=(src_fp[i], dst_fp[i], host, port))
        port = port+1
        jobs.append(th1)

    for t in jobs:
        t.start()

    for t in jobs:
        t.join()

    #th1.join()
    time.sleep(2)
    stop = time.localtime()
    print time.strftime("%y-%m-%d %H%M%S", stop) 
    sys.exit()

