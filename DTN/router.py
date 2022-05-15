import json
import socket
import threading
import struct
import time

class Router():

    cache = {}

    ttl = 3

    message = ""
    address = ""
    unicast_socket = None
    
    def __init__(self):
        self.unicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.unicast_socket.connect((host,port))
    
    def send_to_server(self): 
        self.unicast_socket.send(self.message.encode('utf-8'))

    def receive_from_server(self):
        data,addr = self.unicast_socket.recvfrom(2048)
        print("datagram received from server")

    def receive_from_multicast(self):
        # Initialise socket for IPv6 datagrams
        multicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # Allows address to be reused
        multicast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Binds to all interfaces on the given port
        multicast_socket.bind(('', 8080))
        # Allow messages from this socket to loop back for development
        multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        # Construct message for joining multicast group
        mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
        multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

        # Receive message from multicast group
        data, addr = multicast_socket.recvfrom(2048)

        msg = data.decode('utf-8')

        self.address = addr[0]

        self.message = msg


        print("datagram received from client")

    def send_to_multicast(self):
        # Create ipv6 datagram socket
        multicast_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Allow own messages to be sent back (for local testing)
        multicast_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        multicast_socket.sendto(self.message.encode('utf-8'), ("ff02::abcd:1", 8080))

    def handle(self):

        while True:
            self.receive_from_multicast()

            if self.address not in self.cache.keys():
                self.cache[self.address] = [self.message]
                print(self.cache)
                self.send_to_server()
                self.receive_from_server()
                self.send_to_multicast()

            elif self.message not in self.cache[self.address]:
                self.cache[self.address].append(self.message)
                print(self.cache)
                self.send_to_server()
                self.receive_from_server()
                self.send_to_multicast()
            else:
                print("datagram dropped due to redundancy")
            if self.ttl <= 0:
                self.ttl = 3
                self.cache = {}
        
            self.ttl -= 1
    
    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

router = Router()
router.main()