# cliente para sockets UDP que usam IPv6

from re import M
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

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.sendto(MESSAGE.encode(encoding="UTF-8"), (UDP_IP, UDP_PORT))

def sendToServer(int1, int2):
    MESSAGE = input("client:" )
    sock.sendto(MESSAGE.encode(encoding="UTF-8"), (UDP_IP, UDP_PORT))
    if(MESSAGE=="exit"):
        os.kill(os.getpid(), signal.SIGINT)
        

while True:
    start_new_thread(sendToServer, (1,2))
    (data, addr) = sock.recvfrom(1024)
    print("RECEIVED MESSAGE: ", data.decode(encoding="UTF-8"))
    if(data.endswith(b'exit')):
        sock.close()
        sys.exit(0)

