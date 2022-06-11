import socket
import json
import time
from threading import Thread, RLock
from ifaces import get_ip
import multicast_router
import struct

class MC_Router(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080
        self.infoValue = 9223372036854775807
        self.mcast_ttl = 1
        self.local_ip = '::1'
        self.ttl = struct.pack('@i', self.mcast_ttl)
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]

        # Multicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
        self.multi_sock.bind(('2001:6::1', self.mcast_port))
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)


    def info_response(self, message, addr):
        try:
            self.multi_sock.sendto(json.dumps(message).encode('utf-8'), addr)
            print(f'INFO RESPONSE message sent to host {addr}')

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

    def receive(self):

        while True:

            rcv_msg,addr = self.multi_sock.recvfrom(1024)
            message = json.loads(rcv_msg.decode('utf-8'))

            print(f'INFO REQUEST MESSAGE received from host {addr}')

            message["dst"] = addr[0]
            message["src"] = "host"
            message["type"] = "INFO REPLY"
            message["data"] = self.infoValue

            self.info_response(message, addr)

    def run(self):
        self.receive()

class Router():

    def __init__(self):
        self.serverIP = "2001:0::10"
        self.infoValue = 9223372036854775807
        self.previousHop = ''

        # unicast sockets definition
        self.up_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 5555) # '2001:0::10'
        self.up_sock.bind((host,port))

        self.down_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 6666)
        self.down_sock.bind((host,port))


        self.server_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 7777)
        self.server_sock.bind((host,port))


    def fw_to_dest(self):
        data, addr = self.up_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(f'Packet {message} received from Forwarder ({addr[0]},{addr[1]})')

        self.previousHop = addr[0]
        host, port = (self.serverIP, 7777)
        self.server_sock.sendto(data, (host, port))
        print(f'Packet {message} sent to server: {self.serverIP} through 7777')


    def dest_to_fw(self):
        data, addr = self.server_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(f'Packet {message} received from server ({addr[0]},{addr[1]})')
        self.down_sock.sendto(data, (self.previousHop,6666))
        print(f'Packet {message} sent to host {self.previousHop} through 6666')

    def main(self):
        mc_router = MC_Router()
        mc_router.start()

        while True:
            self.fw_to_dest()
            self.dest_to_fw()

router = Router()
router.main()
