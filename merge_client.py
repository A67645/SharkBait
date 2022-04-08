import json
import socket
import time

class Client():
    window_map = {
        'fishes': {},
        'players': {}
    }
    orientation = [10]
    sock = None

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.connect((host,port))

    def send(self, ori):
        self.sock.send(json.dumps(str(ori)).encode('utf-8'))
        # time.sleep(3)

    def handle(self):
        self.send("[10]")

        data,addr = self.sock.recvfrom(2048)
        #print(json.loads(data.decode('utf-8')),addr)
        self.window_map = json.loads(data.decode('utf-8'))

        self.send(json.dumps(self.orientation))

client = Client()
client.handle()