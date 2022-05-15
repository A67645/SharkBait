import socket
from json import dumps
   
def send(msg, addr, port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.sendto(dumps(msg).encode('utf-8'), (addr, port))
    sock.close()