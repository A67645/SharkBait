import json
import socket
import threading
import time

class Server():
    
    sock = None

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.bind((host,port))

    def send(self,addr, message):
        self.sock.sendto(message.encode('utf-8'),addr)

    def handle(self):
        while True:
            data,addr = self.sock.recvfrom(2048)
            message = data.decode('utf-8')

            msg = json.loads(message)

            msg['type'] = 'reply'

            print("received message from host" + msg['src'])

            message = json.dump(msg)

            self.send(addr, message)

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

server = Server()
server.main()