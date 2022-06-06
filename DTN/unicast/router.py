import json
import socket
import threading
import struct
import time

class Router():

    unicast_socket = None
    
    def __init__(self):
        self.cache = {}
        host,port = ('::1', 6666) # '2001:0::10'
        self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.server_socket.connect((host,port))
        self.host_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.host_socket.bind((host,5555)) # socket = (IP(meu IP) + Port)
        self.return_path = {}
    
    def send_to_server(self, message): 
        self.server_socket.send(json.dumps(message).encode('utf-8'))

    def receive_from_server(self):
        data,addr = self.server_socket.recvfrom(2048)
        return json.loads(data.decode('utf-8'))

    def receive_from_host(self):
        # Receive message from multicast group
        data, addr = self.host_socket.recvfrom(2048)

        msg = data.decode('utf-8')

        message = json.loads(msg)

        src = message["src"]

        self.cache[src] = addr

        print(self.cache)

        return message


    def send_to_host(self, message):
        dst = message["dst"]
        self.host_socket.sendto(json.dumps(message).encode('utf-8'), self.cache[dst])
        del self.cache[dst]

    def handle(self):

        while True:
            message_host = self.receive_from_host()
            self.send_to_server(message_host)
            message_server = self.receive_from_server()
            self.send_to_host(message_server)
    
    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

router = Router()
router.main()