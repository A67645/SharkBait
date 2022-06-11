import socket
import json
import time
from threading import Thread

class source():

    def __init__(self):
        Thread.__init__(self)
        # class variables definition
        self.serverIP = "2001:0::10"
        self.hostIP = "2001:6::22"
        self.nextHop = ()
        self.pos = (0,0)
        self.message = {"src" : self.hostIP, "dst" : self.hostIP, "type" : "DATA REQUEST", "data" : self.pos}
        # unicast socket definition
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def send(self):

        addr = (self.nextHop, 5555)
        message = json.dumps(self.message).encode('utf-8')
        self.uni_sock.sendto(message, addr)

    def receive(self):
        data, addr = self.uni_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print("RESPONSE:")
        print(message)

    def run(self):
        while True:
            self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            host,port = ('', 5555) # '2001:0::10'
            print(self.nextHop)
            self.uni_sock.bind((host,port))
            self.send()
            #self.uni_sock.close()
            #time.sleep(2)
            self.receive()

#source = source()
#source.main()
