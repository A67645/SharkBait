import socket
import json
import time

class dest():

    def __init__(self):

        self.infoValue = 0

        # unicast sockets definition
        self.uni_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 7777) # '2001:0::10'
        self.uni_sock.bind((host,port))

    def receive_and_respond(self):
        data, addr = self.uni_sock.recvfrom(2048)
        message = json.loads(data.decode('utf-8'))
        print(message)
        print(addr)
        print(type(addr))
        self.uni_sock.sendto(data, addr)


    def main(self):
        while True:
            self.receive_and_respond()

dest = dest()
dest.main()