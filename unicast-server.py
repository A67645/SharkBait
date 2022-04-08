import json
import socket
import threading

class Server():
    conns = {
        'addresses': {}
    }
    window_map = {
        'fishes': {},
        'players': {}
    }
    window_height = 0
    window_width = 0
    fish_num = 0
    sock = None

    def __init__(self, ww, wh, fn):
        self.window_width = ww
        self.window_height = wh
        self.fish_num = fn
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock.bind((host,port))

    def add_player(self, addr):
        size = len(self.window_map["players"].keys())
        self.window_map["players"][size + 1] = [360,504, 0, 1]
        self.conns["addresses"][size + 1] = addr


    def send(self,msg,addr):
        self.sock.sendto(json.dumps(msg).encode('utf-8'),addr)

    def handle(self):
        while True:
            data,addr = self.sock.recvfrom(2048)
            print(data.decode('utf-8'),addr)

            if addr[0] not in list(self.conns["addresses"].values()):
                self.add_player(addr[0])
                print(self.conns)

            self.send(self.conns,addr)

    def main(self):
        handler = threading.Thread(target=self.handle, args=())
        handler.start()
        handler.join()

server = Server(1009, 720, 5)
server.main()