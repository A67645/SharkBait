import json
import socket
import time

class Client():
    sock = None

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.connect((host,port))

    def send(self, msg):
        self.sock.send(msg.encode('utf-8'))

    def main(self):
        self.send('hello')
        while True:
            self.send('second')
            time.sleep(3)

            data,addr = self.sock.recvfrom(2048)
            print(json.loads(data.decode('utf-8')),addr)

client = Client()
client.main()