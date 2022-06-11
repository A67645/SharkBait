import socket
import json
import time
from threading import Thread, RLock
from ifaces import get_ip, get_ip_router
import multicast_listener
import multicast_sender
import unicast_forwarder
import func_timeout as timeout
import struct

class MC_Listener(Thread):

    def __init__(self, lock):
        Thread.__init__(self)
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080
        self.lock = lock
        self.mcast_ttl = 1
        self.local_ip = '::1'
        self.ttl = struct.pack('@i', self.mcast_ttl)
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]

        # Multicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
        self.multi_sock.bind(('', self.mcast_port))
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)


    def info_response(self, message, addr):
        try:
            self.multi_sock.sendto(json.dumps(message).encode('utf-8'), addr)
            print(f'INFO RESPONSE {message} sent to {addr}')

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

    def receive(self):

        while True:

            rcv_msg,addr = self.multi_sock.recvfrom(1024)
            message = json.loads(rcv_msg.decode('utf-8'))

            print(f'INFO REQUEST message received from host {addr}')

            message["dst"] = addr[0]
            message["src"] = get_ip()
            message["type"] = "INFO REPLY"
            self.lock.acquire()
            try:
                message["data"] = host.get_infoValue()
            finally:
                self.lock.release()

            self.info_response(message, addr)

    def run(self):
        self.receive()

class MC_Sender(Thread):

    def __init__(self, lock):
        Thread.__init__(self)
        self.lock = lock
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080
        self.nextHop = ((), 0)

        # Mutlicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
        self.multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def receive(self):
        while True:
            data,addr = self.multi_sock.recvfrom(1024)
            message = json.loads(data.decode('utf-8'))
            print(f'INFO REPLY message received from {addr}')
            if message["data"] >= self.nextHop[1]:
                self.nextHop = (addr[0], message["data"])
                print(f'{self.nextHop} chosen as next hop')
                self.lock.acquire()
                try:
                    host.set_nextHop((addr, message["data"]))
                finally:
                    self.lock.release()

    def next_hop(self):

        # Mensagem de INFO REQUEST
        msg = {"src" : "2001:0::20/64", "dst" : self.mcast_group, "type" : "INFO REQUEST", "data" : ''}

        while True:
            self.multi_sock.sendto(json.dumps(msg).encode('utf-8'), (self.mcast_group,self.mcast_port))
            print("INFO REQUEST message sent to mc group")
            try:
                timeout.func_timeout(3, self.receive, args=())
            except timeout.FunctionTimedOut:
                time.sleep(1)
                continue
    def run(self):
        self.next_hop()

class forwarder(Thread):

    def __init__(self, lock):
        Thread.__init__(self)
        self.lock = lock
        self.nextHop = ()
        self.infoValue = 0
        self.previousHop = ''

        # unicast sockets definition
        self.up_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 5555) # '2001:0::10'
        self.up_sock.bind((host,port))

        self.down_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 6666)
        self.down_sock.bind((host,port))

    def send_to_nextHop(self, message, addr):
        data = json.dumps(message).encode('utf-8')
        self.up_sock.sendto(data, addr)
        print(f'DATA REQUEST message {message} sent to ({addr[0]},{addr[1]})')

    def receive(self): #fw_to_dest
        data, addr = self.up_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(f'DATA REPLY message {message} received from ({addr[0]},{addr[1]})')
        self.previousHop = addr[0]
        self.lock.acquire()
        try:
            address = host.nextHop[0]
            host, port = (address[0], 5555)

        finally:
            self.lock.release()
            self.up_sock.sendto(data, (host, port))


    def dest_to_fw(self):
        print('about to receive DATA REPLY')
        data, addr = self.down_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(f'DATA REPLY message {message} received from ({addr[0]},{addr[1]})')
        self.lock.acquire()
        try:
            iv = host.get_infoValue()
            iv += 1
            host.set_infoValue(iv)
            if addr[0] == host.hostIP:
                host.gameState = message["data"]
                print(f'Game state changed to {message["data"]}')
            else:
                self.down_sock.sendto(data, (self.previousHop,6666))
        finally:
            self.lock.release()

    def run(self):
        while True:
            self.receive()
            self.dest_to_fw()

class Host():

    def __init__(self):
        self.gameState = {}
        self.pos = ()
        self.nextHop = ()
        self.infoValue = 0
        self.serverIP = "2001:0::10"
        self.host_port = ('',5555)
        self.hostIP = get_ip()
        self.message = {"src" : self.hostIP, "dst" : self.serverIP, "type" : "DATA REQUEST", "data" : self.pos}
        self.lock = RLock()
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def get_nextHop(self):
        return self.nextHop

    def get_infoValue(self):
        return self.infoValue

    def set_nextHop(self, nh):
        self.nextHop = nh

    def set_infoValue(self, iv):
        self.infoValue = iv

    def bind(self):
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.uni_sock.bind(self.host_port)

    def send(self):
        addr = (self.nextHop, 5555)
        message = json.dumps(self.message).encode('utf-8')
        self.uni_sock.sendto(message, addr)

    def receive(self):
        data, addr = self.uni_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(message)
        self.infoValue += 1
        self.gameState = message["data"]

    def main(self):
        # Start multicast Info Reply Listener
        mc_listener = MC_Listener(self.lock)
        mc_listener.start()

        # Start multicast Info Request sender
        mc_sender = MC_Sender(self.lock)
        mc_sender.start()

        # Start Data Forwarder
        unicast_forwarder = forwarder(self.lock)
        unicast_forwarder.start()

        # Vê se se consegue conectar com o router,
        # se sim coloca next hop como sendo:
        # (<IP DO ROUTER>,9223372036854775807)
        self.nextHop = ('2001:6::1',9223372036854775807)

        time.sleep(5)

        while True: # main game loop
            message = {"src" : self.hostIP, "dst" : self.serverIP, "type" : "DATA REQUEST", "data" : self.pos}
            unicast_forwarder.send_to_nextHop(message, (self.nextHop[0],5555))
            time.sleep(2)

host = Host()
host.main()
