import json
import socket
import threading
import time

class Server():
    
    sock = None

    def __init__(self):
        self.board = {"sharks" : [(10,14), (15, 25), (13,27)], "fish" : [(14,13), (20,20), (17,27)], "scores" : [1, 7, 10]}
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.bind((host,port))

    def send(self,addr, message):
        self.sock.sendto(message,addr)

    def handle(self):
        while True:
            data, addr = self.sock.recvfrom(2048)
            message = data.decode('utf-8')

            msg = json.loads(message)

            if (msg['type'] == 'DATA REQUEST'):
                print(f'received message from host: {msg["data"]}')
                print(addr)

            dst = msg["src"]
            msg["dst"] = msg["src"]
            msg["src"] = dst
            msg["type"] = "DATA REPLY"
            msg["data"] = self.board

            message = json.dumps(msg)

            self.send(addr, message.encode('utf-8'))

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

server = Server()
server.main()