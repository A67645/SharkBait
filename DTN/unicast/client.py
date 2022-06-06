# multicast receiver in client side
import socket
import struct
import time
import threading
import json

class Client():

    # Initializing
    def __init__(self):
        self.serverIP = '::1'
        self.board = {}
        self.msg = {"src" : "", "dst" : "", "type" : "", "data" : self.board}
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 5555) # '2001:0::10'
        self.sock.connect((host,port))

    def receive_from_router(self):
        data, addr = self.sock.recvfrom(2048)
        message = data.decode('utf-8')

        msg = json.loads(message)

        self.msg = msg

        self.board = msg["data"]

        return addr

    def send_to_router(self, data, addr):
        self.sock.send(data)


    def handle(self):   
        while True:

            self.msg["src"] = "hostIP"
            self.msg["dst"] = "serverIP"
            self.msg["type"] = "DATA REQUEST"
            self.msg["data"] = {"player": 1, "pos" : (10,15), "dir" : "UR"}

            self.send_to_router(json.dumps(self.msg).encode('utf-8'), self.serverIP)

            addr = self.receive_from_router()

            print(f'Server {self.msg["src"]} replied with: {self.msg["data"]}')

            time.sleep(1)


    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

client = Client()
client.main()