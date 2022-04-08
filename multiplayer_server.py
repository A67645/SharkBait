# multicast sender in server side
import socket
import json
from random import seed
from random import randint
import threading
import time
from turtle import window_width
import pygame
from pygame.locals import *

class Server:

    conns = {
        'addresses': {1 : '::1'}
    }
    window_map = {}
    window_width=1009 #612
    window_height=720 #437
    clock_tick_rate = 1
    shark_rects = {}
    fish_rects = {}
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
            fish_img_pre = pygame.image.load('img_nobg/fish_model.png')
            fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
            fish_img.convert_alpha()
            self.fish_rects[i] = fish_img.get_rect(x=fish_x, y=fish_y)
            i += 1

    # replaces an eaten fish of index 'fish_index' with a new one in new random coordinates
    def regen_fish(self, fish_index):
        fish_x = randint(0, self.window_width-15)
        fish_y = randint(0, self.window_height-15)
        self.window_map["fishes"][fish_index] = [fish_x, fish_y]
        fish_img_pre = pygame.image.load('img_nobg/fish_model.png')
        fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
        fish_img.convert_alpha()
        self.fish_rects[fish_index] = fish_img.get_rect(x=fish_x, y=fish_y)

    # adds new player to the window map with default values: coords
    def add_player(self, addr):
        size = len(self.window_map["players"].keys())
        self.window_map["players"][size + 1] = [360,504, 0, 1]
        shark_img_pre_r = pygame.image.load('img_nobg/shark_model_right.png')
        shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
        shark_img_r.convert_alpha()
        self.conns["addresses"][size + 1] = addr
        self.shark_rects[size + 1] = shark_img_r.get_rect(x=360, y=504)

    def update_player_score(self, player_index):
        self.window_map["players"][player_index][2] += 1

    def logout_player(self, player_index):
        i = 1
        for key in self.window_map["players"]:
            value = self.window_map["players"][key]
            if (player_index == i):
                self.window_map["players"].pop(key)
                self.conns["addresses"].pop(key)
                i += 1

    def get_dict(self):
        return self.window_map

    def eat_fish(self, index):
        for key in self.fish_rects.keys():
            if (pygame.Rect.colliderect(self.fish_rects[key], self.shark_rects[index])):
                self.regen_fish(key)
                self.window_map["players"][index][2] += 1

    def move_player(self, index, orientation):

        if(len(self.window_map["players"].keys()) == 0):
            return

        posX = self.window_map["players"][index][0]
        posY = self.window_map["players"][index][1]
        side = self.window_map["players"][index][3]

        if(orientation == 1):
           if(posX + 10 < self.window_width-101):
                self.window_map["players"][index][0] += 10
                shark_img_pre_r = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
                shark_img_r.convert_alpha()
                self.shark_rects[index] = shark_img_r.get_rect(x=posX + 10, y=posY)
                side = 1

        elif(orientation == 5):
           if(posX - 10 > 0):
                self.window_map["players"][index][0] -= 10
                shark_img_pre_l = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_l = pygame.transform.rotozoom(shark_img_pre_l, 0, 0.1)
                shark_img_l.convert_alpha()
                self.shark_rects[index] = shark_img_l.get_rect(x=posX - 10, y=posY)
                side = 5

        elif(orientation == 3):
           if(posY + 10 < self.window_height-101):
                self.window_map["players"][index][1] += 10
                shark_img_pre_d = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_d = pygame.transform.rotozoom(shark_img_pre_d, 0, 0.1)
                shark_img_d.convert_alpha()
                self.shark_rects[index] = shark_img_d.get_rect(x=posX, y=posY + 10)
                side = 3

        elif(orientation == 7):
           if(posY - 10 > 0):
                self.window_map["players"][index][1] -= 10
                shark_img_pre_u = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_u = pygame.transform.rotozoom(shark_img_pre_u, 0, 0.1)
                shark_img_u.convert_alpha()
                self.shark_rects[index] = shark_img_u.get_rect(x=posX, y=posY - 10)
                side = 7

        elif(orientation == 2):
            if(posX + 10 < self.window_width-101 and posY + 10 < self.window_height-101):
                self.window_map["players"][index][0] += 10
                self.window_map["players"][index][1] += 10
                shark_img_pre_dr = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_dr = pygame.transform.rotozoom(shark_img_pre_dr, 0, 0.1)
                shark_img_dr.convert_alpha()
                self.shark_rects[index] = shark_img_dr.get_rect(x=posX + 10, y=posY + 10)
                side = 2
                

        elif(orientation == 8):
            if(posX + 10 < self.window_width-101 and posY - 10 > 0):
                self.window_map["players"][index][0] += 10
                self.window_map["players"][index][1] -= 10
                shark_img_pre_ur = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_ur = pygame.transform.rotozoom(shark_img_pre_ur, 0, 0.1)
                shark_img_ur.convert_alpha()
                self.shark_rects[index] = shark_img_ur.get_rect(x=posX + 10, y=posY - 10)
                side = 8
                
        elif(orientation == 6):
            if(posX - 10 > 0 and posY - 10 > 0):
                self.window_map["players"][index][0] -= 10
                self.window_map["players"][index][1] -= 10
                shark_img_pre_ul = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_ul = pygame.transform.rotozoom(shark_img_pre_ul, 0, 0.1)
                shark_img_ul.convert_alpha()
                self.shark_rects[index] = shark_img_ul.get_rect(x=posX - 10, y=posY - 10)
                side = 6

        elif(orientation == 4 and posY + 10 < self.window_height-101):
            if(posX - 10 > 0):
                self.window_map["players"][index][0] -= 10
                self.window_map["players"][index][1] += 10
                shark_img_pre_dl = pygame.image.load('img_nobg/shark_model_right.png')
                shark_img_dl = pygame.transform.rotozoom(shark_img_pre_dl, 0, 0.1)
                shark_img_dl.convert_alpha()
                self.shark_rects[index] = shark_img_dl.get_rect(x=posX - 10, y=posY + 10)
                side = 4

        elif(orientation == 10):
            return

        self.window_map["players"][index][3] = side
        self.eat_fish(index)

    def send(self):
        # fishes: {index : [posX, posY], ...}
        # players : { index : [posX, posY, score, orientation]} 
        JSON_string = json.dumps(self.get_dict())
        # Create ipv6 datagram socket
        sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # Allow own messages to be sent back (for local testing)
        sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, True)
        sock.sendto(JSON_string.encode('utf-8'), ("ff02::abcd:1", 8080))

    def receive_unicast(self):
        sock_unicast = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock_unicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host,port = ('::1', 6666) # '2001:0::10'
        sock_unicast.bind((host,port))
        data,addr = sock_unicast.recvfrom(2048)

        if addr[0] not in list(self.conns["addresses"].values()):
            self.add_player(addr[0])

        JSON_string = data.decode('utf-8')
        orientation = json.loads(JSON_string)
        self.move_player(1, orientation)
        #print(orientation)
        sock_unicast.close()

    def send_unicast(self):
        sock_unicast = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        sock_unicast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #sock_unicast.bind((host,port))
        JSON_string = json.dumps(self.window_map)
        utf8 = JSON_string.encode('utf-8')
        host,port = ('::1', 6666) # '2001:0::10'
        sock_unicast.sendto(utf8, (host,port))


    def main(self):
        #unicast = threading.Thread(target=self.receive_unicast, args=())
        #unicast.start()
        #unicast.join()

        pygame.init()
        # Open a window
        size = (1009, 720)
        screen = pygame.display.set_mode(size)

        # Set title to the window
        pygame.display.set_caption("Shark Bait")

        clock = pygame.time.Clock() 
        self.gen_fishes()

        running = True
        while running:
            self.receive_unicast()
            self.send_unicast()
  
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            clock.tick(self.clock_tick_rate)

            
dict = {
    "fishes" : {},
    "players" : {}
}

server = Server(dict, 1009, 721, 5)
server.main()