# multicast sender in server side
import socket
import json
from random import seed
from random import randint
import time

class Server:

    window_map = {}
    window_width=1009 #612
    window_height=720 #437
    fish_num = 5

    def __init__(self, d, ww, wh, fn):
        self.window_map = d
        self.window_width=ww #612
        self.window_height=wh #437
        self.fish_num = fn
        
    # generate a 'fish_num' number of fish coordinates randomly
    def gen_fishes(self):
        i = 1
        # uses random.py library
        while i <= self.fish_num:
            fish_x = randint(0, self.window_width-15)
            fish_y = randint(0, self.window_height-15)
            self.window_map["fishes"][i] = [fish_x, fish_y]
            i += 1

    # replaces an eaten fish of index 'fish_index' with a new one in new random coordinates
    def regen_fish(self, fish_index):
        fish_x = randint(0, self.window_width-15)
        fish_y = randint(0, self.window_height-15)
        self.window_map["fishes"][fish_index] = [fish_x, fish_y]

    # adds new player to the window map with default values: coords
    def add_player(self):
        size = len(self.window_map["players"].keys())
        self.window_map["players"][size + 1] = [360,504, 0, 1]

    def update_player_score(self, player_index):
        self.window_map["players"][2] += 1

    def move_player(self, player_index, posX, posY, orientation):
        score = self.window_map["players"][player_index][2]
        self.window_map["players"][player_index] =  [posX, posY, score, orientation]

    def logout_player(self, player_index):
        i = 1
        dict = {}
        for key, value in self.window_map["players"]:
            if (player_index != i):
                dict[i] = value
                i += 1
        self.window_map = dict

    def get_dict(self):
        return self.window_map

    def main(self):
        while True:
            # fishes: {index : [posX, posY], ...}
            # players : { index : [posX, posY, score, orientation]}     
            JSON_string = json.dumps(self.get_dict())
            # Create ipv6 datagram socket
            sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            # Allow own messages to be sent back (for local testing)
            sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
            sock.sendto(JSON_string.encode('utf-8'), ("ff02::abcd:1", 8080))
            time.sleep(3)

dict = {
    "fishes" : {},
    "players" : {}
}
server = Server(dict, 1009, 721, 5)
server.gen_fishes()
server.add_player()
server.add_player()
server.main()