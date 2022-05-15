import json
import socket
import threading
import struct
import time

class Router():

    unicast_socket = None
    
    def __init__(self):
        self.unicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.unicast_socket.connect((host,port))
    
    def send_to_server(self, message): 
        self.unicast_socket.send(message.encode('utf-8'))

    def receive_from_server(self):
        data,addr = self.unicast_socket.recvfrom(2048)
        return data.decode('utf-8')

    def receive_from_multicast(self):
        # Initialise socket for IPv6 datagrams
        multicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allows address to be reused
        multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Binds to all interfaces on the given port
        multicast_socket.bind(('', 6666))
        # Allow messages from this socket to loop back for development
        multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        # Construct message for joining multicast group
        mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
        multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        # Receive message from multicast group
        data, addr = multicast_socket.recvfrom(2048)

        return data.decode('utf-8')

        print("datagram received from client")

    def send_to_multicast(self, message):
        # Create ipv6 datagram socket
        multicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Allow own messages to be sent back (for local testing)
        multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        multicast_socket.sendto(message.encode('utf-8'), ("ff02::abcd:1", 6666))

    def handle(self):

        while True:
            message_host = self.receive_from_multicast()
            self.send_to_server(message_host)
            message_server = self.receive_from_server()
            self.send_to_multicast(message_server)
    
    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

router = Router()
router.main()