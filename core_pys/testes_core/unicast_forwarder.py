import socket
import json
import time

class forwarder():

    def __init__(self):

        self.nextHop = "2001:6::1"
        self.infoValue = 0

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

    def main(self):
        while True:
            self.receive()

forwarder = forwarder()
forwarder.main()
