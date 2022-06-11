import json
import socket
import threading
from threading import Thread, RLock
import struct
import host

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
            print(f'message sent to {addr}')

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

    def receive(self):

        while True:

            rcv_msg,addr = self.multi_sock.recvfrom(1024)
            message = json.loads(rcv_msg.decode('utf-8'))

            print(f'message {message} received from {addr}')

            message["dst"] = addr[0]
            message["src"] = "host"
            message["type"] = "INFO REPLY"
            self.lock.acquire()
            try:
                message["data"] = host.host.get_infoValue()
            finally:
                self.lock.release()

            self.info_response(message, addr)

    def run(self):
        self.receive()

#router = Router()
#router.main()
