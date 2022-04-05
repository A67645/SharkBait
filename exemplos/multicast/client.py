# multicast receiver in client side
import socket
import struct
import time
import json

while True:
    # Initialise socket for IPv6 datagrams
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Allows address to be reused
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Binds to all interfaces on the given port
    sock.bind(('', 8080))

    # Allow messages from this socket to loop back for development
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)

    # Construct message for joining multicast group
    mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    data, addr = sock.recvfrom(1024)

    utf8_string = data.decode('utf-8')

    print(type(utf8_string))

    JSON_string = json.loads(utf8_string)

    print(JSON_string)
    
    time.sleep(3)