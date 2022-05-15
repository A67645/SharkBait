import json
import socket
import threading
import time

class Server():
    
    sock = None
    message = ""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.bind((host,port))

    def send(self,addr):
        self.sock.sendto(self.message.encode('utf-8'),addr)

    def handle(self):
        while True:
            data,addr = self.sock.recvfrom(2048)
            self.message = data.decode('utf-8')

            print("datagram received from router")

            self.send(addr)

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

server = Server()
server.main()