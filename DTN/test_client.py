# multicast receiver in client side
import socket
import struct
import time
import threading
import json

class Client():
    message = "The client has spoken"

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

        print(data)

    def send_to_multicast(self):
        # Create ipv6 datagram socket
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Allow own messages to be sent back (for local testing)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        sock.sendto(self.message.encode('utf-8'), ("ff02::abcd:1", 8080))


    def handle(self):
    
        while True:

            self.send_to_multicast()
            self.receive_from_multicast()
            time.sleep(2)

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

client = Client()
client.main()