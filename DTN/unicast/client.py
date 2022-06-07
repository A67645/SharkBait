# multicast receiver in client side
import socket
import struct
import time
import threading
from threading import Thread, RLock
import json

class Client():

    # Initializing
    def __init__(self):
        self.serverIP = '::1'
        self.hostIP = '::1'
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080
        self.info_value = 0
        self.nextHop = (("", ""), 0)
        self.board = {}
        self.msg = {"src" : "", "dst" : "", "type" : "", "data" : self.board}


        # Unicast Socket
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 5544) # '2001:0::10'
        self.uni_sock.bind((host,port))

        # Mutlicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
        self.multi_sock.bind(('', self.mcast_port)) 
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)

    def receive_from_router(self):
        data, addr = self.sock.recvfrom(2048)
        message = data.decode('utf-8')

        msg = json.loads(message)

        self.msg = msg

        self.board = msg["data"]

        return addr

    def send_to_router(self, data, addr):
        self.sock.sendto(data, addr)

    def next_hop(self):

        # Mensagem de INFO REQUEST
        msg = {"src" : self.hostIP, "dst" : self.mcast_group, "type" : "INFO REQUEST", "data" : ''}

        try:
            self.multi_sock.sendto(json.dumps(msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

            timeout = time.time() + 5
            while time.time() < timeout:
                data,addr = self.uni_sock.recvfrom(1024)
                message = json.loads(data.decode('utf-8'))
                print(f'INFO RESPONSE received from {addr}')
                if message["type"] == "INFO RESPONSE" and message["data"] > self.nextHop[1]:
                    self.nextHop = (addr, message["data"])
                    print(f'{self.nextHop} chosen as next hop')

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

    def handle(self):   
        while True:

            self.msg["src"] = "hostIP"
            self.msg["dst"] = "multicastGroup"
            self.msg["type"] = "INFO REQUEST"
            self.msg["data"] = {}

            self.next_hop()

            time.sleep(1)


    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

client = Client()
client.main()