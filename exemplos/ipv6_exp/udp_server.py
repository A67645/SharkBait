from queue import Empty
# servidor para sockets UDP que usam IPv6

import socket
from _thread import *
import sys
import os
import signal

#from client import UDP_IP, UDP_PORT

UDP_IP = "::"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

(data, addr) = sock.recvfrom(1024)
print("RECEIVED MESSAGE: ", data)

def sendToClient(int1, int2):
    MESSAGE = input("server:" )
    sock.sendto(MESSAGE.encode(encoding="UTF-8"), addr)
    if(MESSAGE=="exit"):
        os.kill(os.getpid(), signal.SIGINT)

while True:
    (data, addr) = sock.recvfrom(1024)
    print("RECEIVED MESSAGE: ", data.decode(encoding="UTF-8"))
    if(data.endswith(b'exit')):
        sock.close()
        sys.exit(0)
    start_new_thread(sendToClient, (1,2))   
    