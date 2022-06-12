import json
import socket
import struct
import netifaces
from threading import Thread
from datetime import datetime
from threading import RLock
from json import dumps
from time import sleep
import send_data
import ipaddress
import pygame
from pygame.locals import *
from random import seed
from random import randint

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from threading import Thread, RLock
from time import sleep
from json import dumps
import struct
import socket

class HelloSender(Thread):
    def __init__(self, lock, hello_interval, localhost, ttl, mcast_group, mcast_port):
        Thread.__init__(self)
        pygame.init()
        self.window_map = {"fishes" : {}, "players" : {}}
        self.lock           = lock
        self.hello_interval = hello_interval
        self.ttl            = ttl
        self.localhost      = localhost
        self.mcast_group    = mcast_group
        self.mcast_port     = mcast_port
        self.window_width = 800
        self.window_height = 600
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('/home/core/Desktop/SharkBait/core_pys/parte2/Canterbury.ttf', 32)
        self.img_dict = {}
        self.orientation = [10]
        self.sb_x = 10
        self.sb_y = 10
        # Load Background Image
        self.img_dict[0] = pygame.transform.rotozoom(pygame.image.load("/home/core/Desktop/SharkBait/core_pys/parte2/ocean_background.png").convert(), 0, 1.648).convert_alpha()

        # Load Fish Image
        fish_img_pre = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/fish_model.png')
        fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
        self.img_dict[9] = fish_img.convert_alpha()

        # Load Shark Right
        shark_img_pre_r = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_right.png')
        shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
        shark_img_r.convert_alpha()
        self.img_dict[1] = shark_img_r

        # Load Shark Left
        shark_img_pre_l = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_left.png')
        shark_img_l = pygame.transform.rotozoom(shark_img_pre_l, 0, 0.1)
        shark_img_l.convert_alpha()
        self.img_dict[5] = shark_img_l

        # Load Shark Up
        shark_img_pre_u = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_up.png')
        shark_img_u = pygame.transform.rotozoom(shark_img_pre_u, 0, 0.1)
        shark_img_u.convert_alpha()
        self.img_dict[7] = shark_img_u

        # Load Shark Down
        shark_img_pre_d = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_down.png')
        shark_img_d = pygame.transform.rotozoom(shark_img_pre_d, 0, 0.1)
        shark_img_d.convert_alpha()
        self.img_dict[3] = shark_img_d

        # Load Shark Up Right
        shark_img_pre_ur = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_up_right.png')
        shark_img_ur = pygame.transform.rotozoom(shark_img_pre_ur, 0, 0.14)
        shark_img_ur.convert_alpha()
        self.img_dict[8] = shark_img_ur

        # Load Shark Up Left
        shark_img_pre_ul = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_up_left.png')
        shark_img_ul = pygame.transform.rotozoom(shark_img_pre_ul, 0, 0.14)
        shark_img_ul.convert_alpha()
        self.img_dict[6] = shark_img_ul

        # Load Shark Down Right
        shark_img_pre_dr = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_down_right.png')
        shark_img_dr = pygame.transform.rotozoom(shark_img_pre_dr, 0, 0.14)
        shark_img_dr.convert_alpha()
        self.img_dict[2] = shark_img_dr

        # Load Shark Down Left
        shark_img_pre_dl = pygame.image.load('/home/core/Desktop/SharkBait/core_pys/parte2/img_nobg/shark_model_down_left.png')
        shark_img_dl = pygame.transform.rotozoom(shark_img_pre_dl, 0, 0.14)
        shark_img_dl.convert_alpha()
        self.img_dict[4] = shark_img_dl

    def show_scores(self):

        scores = {}

        for key in self.window_map["players"]:
            value = self.window_map["players"][key]
            scores[key] = value[2]

        i = 0
        for key in scores:
            value = scores[key]
            score = self.font.render(f"{key} : {str(value)}", True, (0, 0, 0))
            self.screen.blit(score, (self.sb_x, self.sb_y + i*20))
            i += 1

    def set_title(self, title):
        pygame.display.set_caption(title)

    def draw(self):

        self.screen.blit(self.img_dict[0], [0, 0])

        for key in self.window_map["fishes"]:
            value = self.window_map["fishes"][key]
            self.screen.blit(self.img_dict[9], value)

        for key in self.window_map["players"]:
            value = self.window_map["players"][key]
            orientation = value[3]
            self.screen.blit(self.img_dict[orientation], [value[0], value[1]])

        self.show_scores()

        pygame.display.flip()
        self.clock.tick(30)


    def set_window_map(self, gs):
        self.window_map = gs

    def create_socket(self):

        try:
            # Criar o socket do client
            client_sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, self.ttl)
            client_sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)

            return client_sock

        except Exception as sock_error:
            print('Failed to create socket: {}'.format(sock_error))

    def hello_sender(self):
        try:
            client_sock = self.create_socket()

                # Messagem a ser enviada
            self.msg = {
                "type": "Request",
                "source": self.localhost,
                "destination" : "2001:0::10",
                "data" : self.orientation
            }

                #print('Sending multicast message to the multicast group ...')
                #print(self.msg)
            client_sock.sendto(dumps(self.msg).encode('utf-8'), (self.mcast_group,self.mcast_port))

        except socket.gaierror as socket_error:
            print('Sending error: {}'.format(socket_error))

        finally:
            client_sock.close()

    def send_request(self):
        self.lock.acquire()
        try:
            self.hello_sender()
            self.window_map = host_movel.get_window_map()

        except Exception as e:
            print('Failed: {}'.format(e.with_traceback()))

        finally:
            self.lock.release()
            sleep(self.hello_interval)
            print(f'GAME MAP: {self.window_map}')

    def run(self):
        running = True
        while running == True:
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == KEYDOWN:

                    if event.key == K_RIGHT:
                        self.orientation[0] = 1

                    elif event.key == K_LEFT:
                        self.orientation[0] = 5

                    elif event.key == K_UP:
                        self.orientation[0] = 7

                    elif event.key == K_DOWN:
                        self.orientation[0] = 3

                    if event.key == K_UP and keys[K_RIGHT] != False:
                        self.orientation[0] = 8

                    elif event.key == K_UP and keys[K_LEFT] != False:
                        self.orientation[0] = 6

                    elif event.key == K_DOWN and keys[K_RIGHT] != False:
                        self.orientation[0] = 2

                    elif event.key == K_DOWN and keys[K_LEFT] != False:
                        self.orientation[0] = 4

                    elif event.key == K_RIGHT and keys[K_UP] != False:
                        self.orientation[0] = 8

                    elif event.key == K_LEFT and keys[K_UP] != False:
                        self.orientation[0] = 6

                    elif event.key == K_RIGHT and keys[K_DOWN] != False:
                        self.orientation[0] = 2

                    elif event.key == K_LEFT and keys[K_DOWN] != False:
                        self.orientation[0] = 4

                elif event.type == KEYUP:

                    if event.key == K_LEFT and keys[K_UP] != False:
                        self.orientation[0] = 7

                    elif event.key == K_UP and keys[K_LEFT] != False:
                        self.orientation[0] = 5

                    elif event.key == K_UP and keys[K_RIGHT] != False:
                        self.orientation[0] = 1

                    elif event.key == K_RIGHT and keys[K_UP] != False:
                        self.orientation[0] = 7

                    elif event.key == K_DOWN and keys[K_LEFT] != False:
                        self.orientation[0] = 5

                    elif event.key == K_LEFT and keys[K_DOWN] != False:
                        self.orientation[0] = 3

                    elif event.key == K_DOWN and keys[K_RIGHT] != False:
                        self.orientation[0] = 1

                    elif event.key == K_RIGHT and keys[K_DOWN] != False:
                        self.orientation[0] = 3

                else:
                    self.orientation[0] = 10
            self.send_request()
            self.draw()
#_________________________________________________________

class Host_Movel():


    def __init__(self, localhost, mcast_group, mcast_port, dead_interv, hello_interval):
        Thread.__init__(self)
        self.window_map = {"fishes" : {}, "players" : {}}
        self.mcast_group = mcast_group
        self.mcast_port = mcast_port
        self.dead_interv = dead_interv
        self.hello_interval = hello_interval
        #self.route_table = {}
        #self.queue = {}
        self.lock = RLock()
        self.mcast_ttl = 1
        self.local_ip = localhost
        self.ttl = struct.pack('@i', self.mcast_ttl)
        self.addrinfo = socket.getaddrinfo(self.mcast_group, None, socket.AF_INET6)[0]


    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)

    def listen(self):
        # abre porta 6666
        #self.sock.bind(('', self.mcast_port))
        mc_address = ipaddress.IPv6Address('ff02::abcd:1')
        listen_port = 6666
        interface_index = socket.if_nametoindex('eth0')
        self.sock.bind((str(mc_address), listen_port, 0, interface_index))

        # Join Multicast Group
        #member_request = struct.pack("16s15s".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), (chr(0) * 16).encode('utf-8'))
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_LOOP, False)
        member_request = struct.pack("16sI".encode('utf-8'), socket.inet_pton(socket.AF_INET6, self.mcast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, member_request)

    def send_data(self,msg):
        send_data.send(msg, self.mcast_group, self.mcast_port)
        print(f'message of type {msg["type"]} sent to ({self.mcast_group},{self.mcast_port})')

    def hello_handler(self,msg):
        test_print = msg['type'] + " from: " + msg['source']
        print(test_print)

    def get_window_map(self):
        return self.window_map

    def receive(self):

        print("my ipv6: " + self.local_ip)

        while True:

            data, addr = self.sock.recvfrom(1024)

            rcv_msg = json.loads(data.decode('utf-8'))

            print(f'Message of type {rcv_msg["type"]} received from {addr}')

            #receive_handler = Receive_Handler(self.lock, rcv_msg, self.local_ip, self.mcast_group, self.mcast_port)

            #receive_handler.start()

            try:
                self.lock.acquire()
                if rcv_msg["type"] == "Request" and rcv_msg["source"] != self.local_ip:
                    self.send_data(rcv_msg)

                elif rcv_msg["type"] == "Reply":
                    if rcv_msg["destination"]!= self.local_ip:
                        self.send_data(rcv_msg)
                        print("recebi do servidor")
                    else:
                        self.window_map = rcv_msg["data"]
                        print('Mensagem para mim')

            finally:
                self.lock.release()



    def send(self):

        hello_sender = HelloSender(self.lock, self.hello_interval, self.local_ip, self.mcast_ttl, self.mcast_group, self.mcast_port)

        hello_sender.start()

        sleep(1)

    def main(self):
        self.create_socket()
        self.listen()
        self.send()
        self.receive()

def get_ip():
        ipv6 = netifaces.ifaddresses('eth0')

        return ipv6[netifaces.AF_INET6][0]['addr']
        return '::1'

host_movel = Host_Movel(localhost=get_ip(), mcast_group='ff02::abcd:1', mcast_port=6666, hello_interval=2, dead_interv=8)
host_movel.main()
