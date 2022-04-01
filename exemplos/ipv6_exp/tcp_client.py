# cliente para sockets TCP que usam IPv6

import signal
import socket
from _thread import *
import sys
import os

UDP_IP = "::1"  #localhost
UDP_PORT = 5005
MESSAGE = "Benvindo ao chat"

print("UDP target IP: ", UDP_IP)
print("UDP target port: ", UDP_PORT)
print("message: ", MESSAGE)

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.connect((UDP_IP, UDP_PORT))
sock.send(MESSAGE.encode(encoding="UTF-8"))

def sendToServer(int1, int2):
    try:
        MESSAGE = input("client:" )
        sock.send(MESSAGE.encode(encoding="UTF-8"))
        if(MESSAGE=="exit"):
            os.kill(os.getpid(), signal.SIGINT)
    except KeyboardInterrupt:
        sock.send(b'exit')
        os.kill(os.getpid(), signal.SIGINT)      

while True:
    try:
        #start_new_thread(sendToServer, (1,2))
        sendToServer(1,2)
        data = sock.recv(1024)
        print("RECEIVED MESSAGE: ", data.decode(encoding="UTF-8"))
        if(data.endswith(b'exit')):
            #sock.close()
            sys.exit(0)
    except KeyboardInterrupt:
        sock.send(b'exit')
        os.kill(os.getpid(), signal.SIGINT)        

