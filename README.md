# Fast-Copy
Tool to copy file between two remote devices

Pre-requisites:

 1. Python along with some modules should be available on both devices

How to use:

At receiver side :

  # python fast_copy_server.py -h
  usage: fast_copy_server.py [-h] -p PORT

  optional arguments:
    -h, --help            show this help message and exit
    -p PORT, --port PORT  Specify the destination port

  e.g. : 

  # python fast_copy_server.py -p 15000 

At sender side :

  # python fast_copy_client.py -h
  usage: fast_copy_client.py [-h] -f FILENAME -H HOST -p PORT [-s SPLITSIZE]
                             [-l LOCALFILE]

  optional arguments:
    -h, --help            show this help message and exit
    -f FILENAME, --filename FILENAME
                          Specify the filename for copying
    -H HOST, --host HOST  Specify the target host or ip address of the host
    -p PORT, --port PORT  Specify the destination port
    -s SPLITSIZE, --splitsize SPLITSIZE
                          Specify the number of split-size for simultaneous copy
  e.g. : 

  # python fast_copy_client.py -f pyshark-0.4.2.2.tar.gz -H 10.10.10.10 -p 15000 


