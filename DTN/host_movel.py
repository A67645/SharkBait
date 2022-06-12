import json
import socket
import struct
import netifaces
from threading import Thread
from datetime import datetime
from threading import RLock
#from hello_sender import HelloSender
from request_handler import Receive_Handler
from json import dumps
from time import sleep
import send_data
import ipaddress

from threading import Thread, RLock
from time import sleep
from json import dumps
import struct
import socket

class HelloSender(Thread):
    def __init__(self, lock, hello_interval, localhost, ttl, mcast_group, mcast_port):
        Thread.__init__(self)
        self.gameState = {"fishes" : {}, "players" : {}}
        self.lock           = lock
        self.hello_interval = hello_interval
        self.ttl            = ttl
        self.localhost      = localhost
        self.mcast_group    = mcast_group
        self.mcast_port     = mcast_port

    def set_gameState(self, gs):
        self.gameState = gs

    def create_socket(self):

        try:
            # Criar o socket do client
            client_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
            client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)

            return client_sock

        except Exception as sock_error:
            print('Failed to create socket: {}'.format(sock_error))

    def hello_sender(self):
        try:
            client_sock = self.create_socket()

                # Messagem a ser enviada
            self.msg = {
                "type": "Request",
                "source": self.localhost,
                "destination" : "2001:0::10",
                "data" : (0,0)
            }

                #print('Sending multicast message to the multicast group ...')
                #print(self.msg)
            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()

    def run(self):
        while True:
            self.lock.acquire()
            try:
                self.hello_sender()
                self.gameState = host_movel.get_gameState()

            except Exception as e:
                print('Failed: {}'.format(e.with_traceback()))

            finally:
                self.lock.release()
                sleep(self.hello_interval)
                print(f'GAME MAP: {self.gameState}')
#_________________________________________________________

class Host_Movel():


    def __init__(self, localhost, mcast_group, mcast_port, dead_interv, hello_interval):
        Thread.__init__(self)
        self.gameState = {"fishes" : {}, "players" : {}}
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

    def get_gameState(self):
        return self.gameState

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
                        self.gameState = rcv_msg["data"]
                        #hello_sender.set_gameState(self.gameState)
                        print('Mensagem para mim')

            finally:
                self.lock.release()



    def send(self):

        hello_sender = HelloSender(self.lock, self.hello_interval, self.local_ip, self.mcast_ttl, self.mcast_group, self.mcast_port)

        hello_sender.start()

        sleep(1)

    def main(self):
        self.create_socket()
        self.listen()
        self.send()
        self.receive()

def get_ip():
        ipv6 = netifaces.ifaddresses('eth0')

        return ipv6[netifaces.AF_INET6][0]['addr']
        return '::1'

host_movel = Host_Movel(localhost=get_ip(), mcast_group='ff02::abcd:1', mcast_port=6666, hello_interval=2, dead_interv=8)
host_movel.main()
