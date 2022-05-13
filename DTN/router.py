import json
import socket
import threading
import struct

class Server():

    message = "Hello World!"
    sock = None
    addr = ""
    

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.connect((host,port))
    
    def send_to_server(self, msg, addr):
        self.sock.sendto(json.dumps(msg).encode('utf-8'),addr)

    def receive_from_server(self):
        data,addr = self.sock.recvfrom(2048)
        print(data.decode('utf-8'),addr)

    def receive_from_multicast(self):
        while True:
            # Initialise socket for IPv6 datagrams
            self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

            # Allows address to be reused
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Binds to all interfaces on the given port
            self.sock.bind(('', 8080))

            # Allow messages from this socket to loop back for development
            self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)

            # Construct message for joining multicast group
            mreq = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, "ff02::abcd:1"), (chr(0) * 16).encode('utf-8'))
            self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

            # Receive message from multicast group
            data, addr = self.sock.recvfrom(1024)

            print(data)

    def send_to_multicast(self):
        # Create ipv6 datagram socket
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Allow own messages to be sent back (for local testing)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        sock.sendto(self.message.encode('utf-8'), ("ff02::abcd:1", 8080))

    def handle(self):

        while True:

            self.receive_from_multicast()
            self.send_to_server()
            self.receive_from_server()
            self.send_to_multicast()
    
    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

server = Server(1009, 720, 5)
server.main()