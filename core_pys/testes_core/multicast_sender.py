import socket
import struct
import time
import threading
from threading import Thread, RLock
import json
import func_timeout as timeout
import host


class MC_Sender(Thread):

    def __init__(self, lock):
        Thread.__init__(self)
        self.lock = lock
        self.mcast_group = "ff02::abcd:1"
        self.mcast_port = 8080
        self.nextHop = ((), 0)

        # Mutlicast Socket
        self.multi_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.multi_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        self.multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def receive(self):
        while True:
            data,addr = self.multi_sock.recvfrom(1024)
            message = json.loads(data.decode('utf-8'))
            print(f'message {message} received from {addr}')
            if message["data"] >= self.nextHop[1]:
                self.nextHop = (addr, message["data"])
                self.lock.acquire()
                try:
                    host.host.set_nextHop((addr, message["data"]))
                finally:
                    self.lock.release()
                print(f'{self.nextHop} chosen as next hop')

    def next_hop(self):

        # Mensagem de INFO REQUEST
        msg = {"src" : "2001:0::20/64", "dst" : self.mcast_group, "type" : "INFO REQUEST", "data" : ''}

        while True:
            self.multi_sock.sendto(json.dumps(msg).encode('utf-8'), (self.mcast_group,self.mcast_port))
            print("Message sent to mc group")
            try:
                timeout.func_timeout(3, self.receive, args=())
            except timeout.FunctionTimedOut:
                time.sleep(1)
                continue
    def run(self):
        self.next_hop()

#client = Client()
#client.main()
