# servidor para sockets TCP que usam IPv6

import socket
from _thread import *
import sys
import os
import signal


UDP_IP = "::"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
sock.bind((UDP_IP, UDP_PORT))
sock.listen()

(client, addr) = sock.accept()

def sendToClient(int1, int2):
    MESSAGE = ""
    while(len(MESSAGE)<2):
        MESSAGE = input("server:" )
    client.send(MESSAGE.encode(encoding="UTF-8"))
    if(MESSAGE=="exit"):
        os.kill(os.getpid(), signal.SIGINT)

while True:
    #start_new_thread(sendToClient, (1,2)) 
    #(client, addr) = sock.accept()
    data = client.recv(1024)
    print("RECEIVED MESSAGE: ", data.decode(encoding="UTF-8"))
    if(data.endswith(b'exit')):
        client.close()
        sys.exit(0)
    start_new_thread(sendToClient, (1,2)) 