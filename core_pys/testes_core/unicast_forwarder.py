import socket
import json
import time
from threading import Thread, RLock

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

    def receive(self):
        data, addr = self.up_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(message)
        self.previousHop = addr
        self.lock.acquire()
        try:
            addr = Host.nextHop[0]
            host, port = (addr[0], 6666)
        finally:
            self.lock.release()
            self.down_sock.sendto(data, (host, port))

    def dest_to_fw(self):
        data, addr = self.down_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print("RESPONSE:")
        print(message)
        self.up_sock.sendto(data, self.previousHop)
        self.lock.acquire()
        try:
            iv = host.host.get_infoValue()
            iv += 1
            host.host.set_infoValue(iv)
        finally:
            self.lock.release()


    def run(self):
        while True:
            self.receive()
            self.dest_to_fw()

#forwarder = forwarder()
#forwarder.main()
