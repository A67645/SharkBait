import socket


class Client():
    sock_unicast = None
    sock_multicast = None

    def __init__(self):
        self.sock_unicast = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

    def send(self, msg):
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock_unicast.sendto(msg.encode('utf-8'), (host,port))

    def main(self):
        self.send('hello')
        while True:
            s = input()
            self.send(s)

    

client = Client()
client.main()