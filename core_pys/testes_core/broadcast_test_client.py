import socket
import struct
import time
import threading
from threading import Thread, RLock
import json
import func_timeout as timeout


class Client():

    def __init__(self):
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080

        # Unicast Socket
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 5555) # '2001:0::10'
        #self.uni_sock.bind((host,port))

        # Mutlicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        self.multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def receive(self):
        while True:
            print("started receiving")
            data,addr = self.multi_sock.recvfrom(1024)
            print("message received")
            message = json.loads(data.decode('utf-8'))
            print(message)
            self.nextHop = (addr, message["data"])
            print(f'{self.nextHop} chosen as next hop')

    def next_hop(self):

        # Mensagem de INFO REQUEST
        msg = {"src" : "2001:0::20/64", "dst" : self.mcast_group, "type" : "INFO REQUEST", "data" : ''}

        while True:
            self.multi_sock.sendto(json.dumps(msg).encode('utf-8'), (self.mcast_group,self.mcast_port))
            try:
                timeout.func_timeout(3, self.receive, args=())
            except timeout.FunctionTimedOut:
                continue
    def main(self):
        self.next_hop()

client = Client()
client.main()
