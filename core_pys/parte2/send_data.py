import socket
from json import dumps

def send(msg, addr, port):
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
    sock.sendto(dumps(msg).encode('utf-8'), (addr, port))
    sock.close()
