import json
import socket
import threading
from threading import Thread, RLock
import struct
import ifaces

class Hello(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080
        self.lock = RLock()
        self.mcast_ttl = 1
        self.local_ip = '::1'
        self.ttl = struct.pack('@i', self.mcast_ttl)
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]

        # Unicast Socket
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.uni_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.uni_sock.bind((ifaces.get_ip_router('eth0'), 5555))

        # Multicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
        self.multi_sock.bind(('', self.mcast_port)) 
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)

    def info_response(self, message, addr):
        try:
            self.uni_sock.sendto(json.dumps(message).encode('utf-8'), addr)

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

    def receive(self):

        while True:

            rcv_msg,addr = self.multi_sock.recvfrom(1024)
            message = json.loads(rcv_msg.decode('utf-8'))

            if message["type"] == "INFO REQUEST":
                message_host = {"src" : "routerIP", "dst" : "hostIP", "type" : "INFO REPLY", "data" : 9223372036854775808}
                self.info_response(message_host, addr)

    def run(self):
        self.receive()

            
