import json
import socket
import threading
import time
import ifaces
import pygame
from pygame.locals import *
from random import randint

class Server():

    sock = None

    def __init__(self):
        self.window_map = {"fishes" : {}, "players" : {}}
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        host,port = ('', 7777) # '2001:0::10'
        self.sock.bind((host,port))
        self.window_height = 400
        self.window_width = 600
        self.fish_num = 5
        self.clock_tick_rate=2
        self.shark_rects = {}
        self.fish_rects = {}
        self.conns = {
            'addresses': {}
        }

    def gen_fishes(self):
        i = 1
        # uses random.py library
        while i <= self.fish_num:
            fish_x = randint(0, self.window_width-15)
            fish_y = randint(0, self.window_height-15)
            self.window_map["fishes"][i] = [fish_x, fish_y]
            fish_img_pre = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/fish_model.png')
            fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
            fish_img.convert_alpha()
            self.fish_rects[i] = fish_img.get_rect(x=fish_x, y=fish_y)
            i += 1


    def regen_fish(self, fish_index):
        fish_x = randint(0, self.window_width-15)
        fish_y = randint(0, self.window_height-15)
        self.window_map["fishes"][fish_index] = [fish_x, fish_y]
        fish_img_pre = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/fish_model.png')
        fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
        fish_img.convert_alpha()
        self.fish_rects[fish_index] = fish_img.get_rect(x=fish_x, y=fish_y)

    def add_player(self, addr):
        if addr not in self.conns["addresses"].values():
            size = len(self.window_map["players"].keys())
            self.window_map["players"][size + 1] = [360,504, 0, 1]
            shark_img_pre_r = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
            shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
            shark_img_r.convert_alpha()
            self.conns["addresses"][size + 1] = addr
            self.shark_rects[size + 1] = shark_img_r.get_rect(x=360, y=504)

    def logout_player(self, player_index):
        i = 1
        for key in self.window_map["players"]:
            value = self.window_map["players"][key]
            if (player_index == i):
                self.window_map["players"].pop(key)
                self.conns["addresses"].pop(key)
                i += 1

    def eat_fish(self, index):
        for key in self.fish_rects.keys():
            if (pygame.Rect.colliderect(self.fish_rects[key], self.shark_rects[index])):
                self.regen_fish(key)
                self.window_map["players"][index][2] += 1

    # index = playerid
    def move_player(self, index, ori):

        orientation = ori[0]
        if(len(self.window_map["players"].keys()) == 0):
            return

        posX = self.window_map["players"][index][0]
        posY = self.window_map["players"][index][1]
        side = self.window_map["players"][index][3]

        if(orientation == 1):
           if(posX + 10 < self.window_width-101):
                self.window_map["players"][index][0] += 10
                shark_img_pre_r = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
                shark_img_r.convert_alpha()
                self.shark_rects[index] = shark_img_r.get_rect(x=posX + 10, y=posY)
                side = 1

        elif(orientation == 5):
           if(posX - 10 > 0):
                self.window_map["players"][index][0] -= 10
                shark_img_pre_l = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_l = pygame.transform.rotozoom(shark_img_pre_l, 0, 0.1)
                shark_img_l.convert_alpha()
                self.shark_rects[index] = shark_img_l.get_rect(x=posX - 10, y=posY)
                side = 5

        elif(orientation == 3):
           if(posY + 10 < self.window_height-101):
                self.window_map["players"][index][1] += 10
                shark_img_pre_d = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_d = pygame.transform.rotozoom(shark_img_pre_d, 0, 0.1)
                shark_img_d.convert_alpha()
                self.shark_rects[index] = shark_img_d.get_rect(x=posX, y=posY + 10)
                side = 3

        elif(orientation == 7):
           if(posY - 10 > 0):
                self.window_map["players"][index][1] -= 10
                shark_img_pre_u = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_u = pygame.transform.rotozoom(shark_img_pre_u, 0, 0.1)
                shark_img_u.convert_alpha()
                self.shark_rects[index] = shark_img_u.get_rect(x=posX, y=posY - 10)
                side = 7

        elif(orientation == 2):
            if(posX + 10 < self.window_width-101 and posY + 10 < self.window_height-101):
                self.window_map["players"][index][0] += 10
                self.window_map["players"][index][1] += 10
                shark_img_pre_dr = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_dr = pygame.transform.rotozoom(shark_img_pre_dr, 0, 0.1)
                shark_img_dr.convert_alpha()
                self.shark_rects[index] = shark_img_dr.get_rect(x=posX + 10, y=posY + 10)
                side = 2

        elif(orientation == 8):
            if(posX + 10 < self.window_width-101 and posY - 10 > 0):
                self.window_map["players"][index][0] += 10
                self.window_map["players"][index][1] -= 10
                shark_img_pre_ur = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_ur = pygame.transform.rotozoom(shark_img_pre_ur, 0, 0.1)
                shark_img_ur.convert_alpha()
                self.shark_rects[index] = shark_img_ur.get_rect(x=posX + 10, y=posY - 10)
                side = 8

        elif(orientation == 6):
            if(posX - 10 > 0 and posY - 10 > 0):
                self.window_map["players"][index][0] -= 10
                self.window_map["players"][index][1] -= 10
                shark_img_pre_ul = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_ul = pygame.transform.rotozoom(shark_img_pre_ul, 0, 0.1)
                shark_img_ul.convert_alpha()
                self.shark_rects[index] = shark_img_ul.get_rect(x=posX - 10, y=posY - 10)
                side = 6

        elif(orientation == 4 and posY + 10 < self.window_height-101):
            if(posX - 10 > 0):
                self.window_map["players"][index][0] -= 10
                self.window_map["players"][index][1] += 10
                shark_img_pre_dl = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
                shark_img_dl = pygame.transform.rotozoom(shark_img_pre_dl, 0, 0.1)
                shark_img_dl.convert_alpha()
                self.shark_rects[index] = shark_img_dl.get_rect(x=posX - 10, y=posY + 10)
                side = 4

        elif(orientation == 10):
            return

        self.window_map["players"][index][3] = side
        self.eat_fish(index)

    def getidfromaddr(self,addr):
        for key, value in self.conns["addresses"].items():
         if addr == value:
             return key

    def lststrtolst(self,lst):
        l = lst.strip('][').split(', ')
        l = [int(x) for x in l]
        return l

    def send(self,addr, message):
        self.sock.sendto(message.encode('utf-8'),addr)
        print(f'Message {message} sent to router at {addr}')

    def handle(self):
        pygame.init()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("Shark Bait")
        clock = pygame.time.Clock()
        self.gen_fishes()

        running = True
        while running:
            data,addr = self.sock.recvfrom(2048)
            message = data.decode('utf-8')

            msg = json.loads(message)

            if addr[0] not in list(self.conns["addresses"].values()):
                self.add_player(msg["source"])

            id = self.getidfromaddr(msg["source"])

            update = msg["data"]

            self.move_player(id,update)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            clock.tick(self.clock_tick_rate)

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
