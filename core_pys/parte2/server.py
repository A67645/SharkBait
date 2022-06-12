import json
import socket
import threading
import time
import ifaces

class Server():

    sock = None

    def __init__(self):
        self.window_map = {"fishes" : {1 : (3.6)}, "players" : {1 : (15,15)}}
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 7777) # '2001:0::10'
        self.sock.bind((host,port))

    def send(self,addr, message):
        self.sock.sendto(message.encode('utf-8'),addr)
        print(f'Message {message} sent to router at {addr}')

    def handle(self):
        while True:
            data,addr = self.sock.recvfrom(2048)
            message = data.decode('utf-8')

            msg = json.loads(message)

            print("received message from router with source: " + msg['source'])

            msg['type'] = 'Reply'

            msg['destination'] = msg['source']

            msg['source'] = '2001:0::10'

            msg['data'] = self.window_map

            message = json.dumps(msg)

            self.send(addr, message)

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

server = Server()
server.main()
