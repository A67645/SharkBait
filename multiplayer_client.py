# multicast receiver in client side
import socket
import struct
import json

class Client():

    receive_buffer = {}
    send_buffer = []
    sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def __init__(self, dict, list):
        self.receive_buffer = dict
        self.send_buffer = list

    def load_receive_buffer(self, dict):
        self.receive_buffer = dict

    def load_send_buffer(self, list):
        self.send_buffer = list

    def get_receive_buffer(self):
        return self.receive_buffer

    def get_send_buffer(self):
        return self.send_buffer

    def set_send_buffer(self, array):
        self.send_buffer = array

    def receive(self):

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

        data, addr = self.sock.recvfrom(1024)

        utf8_string = data.decode('utf-8')

        JSON_string = json.loads(utf8_string)

        self.load_receive_buffer(JSON_string)

    def receive_unicast(self):
        sock_unicast = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock_unicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host,port = ('::1', 6666) # '2001:0::10'
        sock_unicast.bind((host,port))
        data,addr = sock_unicast.recvfrom(2048)

        JSON_string = data.decode('utf-8')
        window = json.loads(JSON_string)
        self.receive_buffer = window
        #print(self.receive_buffer)
        sock_unicast.close()
        

    #parte que envia ao servidor as coordenadas e orientação
    def send_unicast(self):
        sock_unicast = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock_unicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host,port = ('::1', 6666) # '2001:0::10'
        #sock_unicast.bind((host,port))
        JSON_string = json.dumps(self.send_buffer)
        utf8 = JSON_string.encode('utf-8')
        host,port = ('::1', 6666) # '2001:0::10'
        sock_unicast.sendto(utf8, (host,port))
"""
rb = {}
sb = [1]
client = Client(rb, sb)
while True:
    client.receive_unicast()
    client.send_unicast()

"""
