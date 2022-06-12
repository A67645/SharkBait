import json
import socket
import struct
from threading import Thread
from datetime import datetime
from threading import RLock
from hello_sender import HelloSender
from request_handler import Receive_Handler
from json import dumps
from time import sleep
import send_data
import ipaddress

class Host_Movel(Thread):


    def __init__(self, localhost, mcast_group, mcast_port, dead_interv, hello_interval):
        Thread.__init__(self)

        self.mcast_group = mcast_group
        self.mcast_port = mcast_port
        self.dead_interv = dead_interv
        self.hello_interval = hello_interval
        #self.route_table = {}
        #self.queue = {}
        self.lock = RLock()
        self.mcast_ttl = 1
        self.local_ip = localhost
        self.ttl = struct.pack('@i', self.mcast_ttl)
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]


    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)

    def listen(self):
        # abre porta 6666
        #self.sock.bind(('', self.mcast_port))
        mc_address = ipaddress.IPv6Address('ff02::abcd:1')
        listen_port = 6666
        interface_index = socket.if_nametoindex('eth0')
        self.sock.bind((str(mc_address), listen_port, 0, interface_index))

        # Join Multicast Group
        #member_request = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), (chr(0) * 16).encode('utf-8'))
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)

    def send_data(self,msg):
        send_data.send(msg, self.mcast_group, self.mcast_port)
        print(f'message of type {msg["type"]} sent to ({self.mcast_group},{self.mcast_port})')

    def hello_handler(self,msg):
        test_print = msg['type'] + " from: " + msg['source']
        print(test_print)

    def receive(self):

        print("my ipv6: " + self.local_ip)

        while True:

            data, addr = self.sock.recvfrom(1024)

            rcv_msg = json.loads(data.decode('utf-8'))

            print(f'Message of type {rcv_msg["type"]} received from {addr}')

            #receive_handler = Receive_Handler(self.lock, rcv_msg, self.local_ip, self.mcast_group, self.mcast_port)

            #receive_handler.start()

            try:
                self.lock.acquire()
                if rcv_msg["type"] == "Request" and rcv_msg["source"] != self.local_ip:
                    self.send_data(rcv_msg)

                elif rcv_msg["type"] == "Reply":
                    if rcv_msg["destination"]!= self.local_ip:
                        self.send_data(rcv_msg)
                        print("recebi do servidor")
                    else:
                        print('Mensagem para mim')

            finally:
                self.lock.release()



    def send(self):

        hello_sender = HelloSender(self.lock, self.hello_interval, self.local_ip, self.mcast_ttl, self.mcast_group, self.mcast_port)

        hello_sender.start()

        sleep(1)


    def run(self):
        self.create_socket()
        self.listen()
        self.send()
        self.receive()
