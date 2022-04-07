from random import randint
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
    sock_unicast = None

    def __init__(self, ww, wh, fn):
        self.window_width = ww
        self.window_height = wh
        self.fish_num = fn
        self.sock_unicast = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('::1', 6666) # '2001:0::10'
        self.sock_unicast.bind((host,port))
        
    def gen_fishes(self):
        i = 1
        # uses random.py library
        while i <= self.fish_num:
            fish_x = randint(0, self.window_width-15)
            fish_y = randint(0, self.window_height-15)
            self.window_map["fishes"][i] = [fish_x, fish_y]
            i += 1

    def add_player(self, addr):
        size = len(self.window_map["players"].keys())
        self.window_map["players"][size + 1] = [360,504, 0, 1]
        self.conns["addresses"][size + 1] = addr


    def handle_unicast(self):
        while True:
            data,addr = self.sock_unicast.recvfrom(2048)
            print(data.decode('utf-8'),addr)

            if addr[0] not in list(self.conns["addresses"].values()):
                self.add_player(addr[0])
                print(list(self.conns["addresses"].values()))

    def main(self):
        unicast = threading.Thread(target=self.handle_unicast, args=())
        unicast.start()
        unicast.join()

server = Server(1009, 720, 5)
server.gen_fishes()
server.main()