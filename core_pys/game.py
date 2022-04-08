import pygame
from pygame.locals import *
from random import seed
from random import randint

import client

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class SharkBait:

    window_map = {"fishes" : {}, "players" : {}}
    window_width = 1009
    window_height = 720
    screen = None
    clock = None
    img_dict = {}
    orientation = [10]
    font = None
    sb_x = 10
    sb_y = 10

    def __init__(self, ww, wh, sbx, sby):
        self.window_width = ww
        self.window_height = wh
        pygame.init()
        self.screen = pygame.display.set_mode((ww, wh))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('/home/core/aer/Canterbury.ttf', 32)
        self.sb_x = sbx
        self.sb_y = sby

        # Load Background Image
        self.img_dict[0] = pygame.transform.rotozoom(pygame.image.load("/home/core/aer/ocean_background.png").convert(), 0, 1.648).convert_alpha()

        # Load Fish Image
        fish_img_pre = pygame.image.load('/home/core/aer/img_nobg/fish_model.png')
        fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
        self.img_dict[9] = fish_img.convert_alpha()

        # Load Shark Right
        shark_img_pre_r = pygame.image.load('/home/core/aer/img_nobg/shark_model_right.png')
        shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
        shark_img_r.convert_alpha()
        self.img_dict[1] = shark_img_r

        # Load Shark Left
        shark_img_pre_l = pygame.image.load('/home/core/aer/img_nobg/shark_model_left.png')
        shark_img_l = pygame.transform.rotozoom(shark_img_pre_l, 0, 0.1)
        shark_img_l.convert_alpha()
        self.img_dict[5] = shark_img_l

        # Load Shark Up
        shark_img_pre_u = pygame.image.load('/home/core/aer/img_nobg/shark_model_up.png')
        shark_img_u = pygame.transform.rotozoom(shark_img_pre_u, 0, 0.1)
        shark_img_u.convert_alpha()
        self.img_dict[7] = shark_img_u

        # Load Shark Down
        shark_img_pre_d = pygame.image.load('/home/core/aer/img_nobg/shark_model_down.png')
        shark_img_d = pygame.transform.rotozoom(shark_img_pre_d, 0, 0.1)
        shark_img_d.convert_alpha()
        self.img_dict[3] = shark_img_d

        # Load Shark Up Right
        shark_img_pre_ur = pygame.image.load('/home/core/aer/img_nobg/shark_model_up_right.png')
        shark_img_ur = pygame.transform.rotozoom(shark_img_pre_ur, 0, 0.14)
        shark_img_ur.convert_alpha()
        self.img_dict[8] = shark_img_ur

        # Load Shark Up Left
        shark_img_pre_ul = pygame.image.load('/home/core/aer/img_nobg/shark_model_up_left.png')
        shark_img_ul = pygame.transform.rotozoom(shark_img_pre_ul, 0, 0.14)
        shark_img_ul.convert_alpha()
        self.img_dict[6] = shark_img_ul

        # Load Shark Down Right
        shark_img_pre_dr = pygame.image.load('/home/core/aer/img_nobg/shark_model_down_right.png')
        shark_img_dr = pygame.transform.rotozoom(shark_img_pre_dr, 0, 0.14)
        shark_img_dr.convert_alpha()
        self.img_dict[2] = shark_img_dr

        # Load Shark Down Left
        shark_img_pre_dl = pygame.image.load('/home/core/aer/img_nobg/shark_model_down_left.png')
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

    def set_window_map(self, dict):
        self.window_map = dict

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

    def main(self):
        # self.window_map = { "fishes" : {1 : [140,120], 2 : [440,220], 3 : [335,127], 4 : [240,620], 5 : [344,523]},
        #      "players" : {1 : [100,200,0, 1], 2 : [155,255,0, 1]}
        #    }
        cli = client.Client()
        running = True
        while running:
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

            cli.orientation = self.orientation
            cli.handle()
            self.set_window_map(cli.window_map)
            self.draw()

# wm = { "fishes" : {1 : [140,120], 2 : [440,220], 3 : [335,127], 4 : [240,620], 5 : [344,523]},
#              "players" : {1 : [100,200,0, 1], 2 : [155,255,0, 1]}
#            }
game = SharkBait(1009, 720, 10, 10)
game.main()