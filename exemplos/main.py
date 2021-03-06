from game import Fish, Player
from network_SB import Network

# Import pygame
import pygame
from pygame.locals import *

# Generate random integer values
from random import seed
from random import randint


# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# initialize game engine
pygame.init()

window_width=1009 #612
window_height=720 #437

# Score
score_value = 0
font = pygame.font.Font('Canterbury.ttf', 32)
(sb_x, sb_y) = (10, 10)

def show_score(x, y):
    score = font.render(f"Score: {str(score_value)}", True, (0, 0, 0))
    screen.blit(score, (x, y))

step=10
clock_tick_rate=120

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Shark Bait")

clock = pygame.time.Clock()
background_image_pre = pygame.image.load("ocean_background.png").convert()
background_image = pygame.transform.rotozoom(background_image_pre, 0, 1.648)
background_image.convert_alpha()

# Dictionary to store images to pass as constructor arguments

img_dict = {}

# Load Shark Right
shark_img_pre_r = pygame.image.load('img_nobg/shark_model_right.png')
shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
shark_img_r.convert_alpha()
img_dict["right"] = shark_img_r
shark_img_r_rect = shark_img_r.get_rect()
shark_x = window_width//2
shark_y = window_height//2

# Load Shark Left
shark_img_pre_l = pygame.image.load('img_nobg/shark_model_left.png')
shark_img_l = pygame.transform.rotozoom(shark_img_pre_l, 0, 0.1)
shark_img_l.convert_alpha()
img_dict["left"] = shark_img_l

# Load Shark Up
shark_img_pre_u = pygame.image.load('img_nobg/shark_model_up.png')
shark_img_u = pygame.transform.rotozoom(shark_img_pre_u, 0, 0.1)
shark_img_u.convert_alpha()
img_dict["up"] = shark_img_u

# Load Shark Down
shark_img_pre_d = pygame.image.load('img_nobg/shark_model_down.png')
shark_img_d = pygame.transform.rotozoom(shark_img_pre_d, 0, 0.1)
shark_img_d.convert_alpha()
img_dict["down"] = shark_img_d

# Load Shark Up Right
shark_img_pre_ur = pygame.image.load('img_nobg/shark_model_up_right.png')
shark_img_ur = pygame.transform.rotozoom(shark_img_pre_ur, 0, 0.14)
shark_img_ur.convert_alpha()
img_dict["up_right"] = shark_img_ur

# Load Shark Up Left
shark_img_pre_ul = pygame.image.load('img_nobg/shark_model_up_left.png')
shark_img_ul = pygame.transform.rotozoom(shark_img_pre_ul, 0, 0.14)
shark_img_ul.convert_alpha()
img_dict["up_left"] = shark_img_ul

# Load Shark Down Right
shark_img_pre_dr = pygame.image.load('img_nobg/shark_model_down_right.png')
shark_img_dr = pygame.transform.rotozoom(shark_img_pre_dr, 0, 0.14)
shark_img_dr.convert_alpha()
img_dict["down_right"] = shark_img_dr

# Load Shark Down Left
shark_img_pre_dl = pygame.image.load('img_nobg/shark_model_down_left.png')
shark_img_dl = pygame.transform.rotozoom(shark_img_pre_dl, 0, 0.14)
shark_img_dl.convert_alpha()
img_dict["down_left"] = shark_img_dl

img_dict["bg_image"] = background_image

# Load Fishes

'''
fish_num = 5
i = 0
fish_coords = []
fish_imgs = []
fish_rects = []
while i < fish_num:
    fish_x = randint(0, window_width-15)
    fish_y = randint(0, window_height-15)
    fish_coords.append([fish_x, fish_y])
    fish_img_pre = pygame.image.load('img_nobg/fish_model.png')
    fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.06)
    fish_img.convert_alpha()
    fish_imgs.append(fish_img)
    fish_rects.append(fish_img.get_rect(x=fish_x, y=fish_y))
    i+=1
'''
fishes = Fish(5,screen)
fishes.load()

# Game Loop
pos = [shark_x, shark_y]
shark_img_last = shark_img_r
shark_img = shark_img_last
print(img_dict["right"].get_width())
print(img_dict["right"].get_heigth())
shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])
player = Player(pos, shark_img_last, shark_img, shark_rect, img_dict, screen)
while player.getDead() != True:
    player.playerLoop()
    '''
    shark_img = shark_img_last
    shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

        elif event.type == KEYDOWN:

            if event.key == K_RIGHT:
                shark_img_last = shark_img_r
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_LEFT:
                shark_img_last = shark_img_l
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])
            
            elif event.key == K_UP:
                shark_img_last = shark_img_u
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_DOWN:
                shark_img_last = shark_img_d
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            if event.key == K_UP and keys[K_RIGHT] != False:
                shark_img_last = shark_img_ur
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_UP and keys[K_LEFT] != False:
                shark_img_last = shark_img_ul
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_DOWN and keys[K_RIGHT] != False:
                shark_img_last = shark_img_dr
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_DOWN and keys[K_LEFT] != False:
                shark_img_last = shark_img_dl
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_RIGHT and keys[K_UP] != False:
                shark_img_last = shark_img_ur
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_LEFT and keys[K_UP] != False:
                shark_img_last = shark_img_ul
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_RIGHT and keys[K_DOWN] != False:
                shark_img_last = shark_img_dr
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_LEFT and keys[K_DOWN] != False:
                shark_img_last = shark_img_dl
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

        if event.type == KEYUP:

            if event.key == K_LEFT and keys[K_UP] != False:
                shark_img_last = shark_img_u
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_UP and keys[K_LEFT] != False:
                shark_img_last = shark_img_l
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_UP and keys[K_RIGHT] != False:
                shark_img_last = shark_img_r
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_RIGHT and keys[K_UP] != False:
                shark_img_last = shark_img_u
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_DOWN and keys[K_LEFT] != False:
                shark_img_last = shark_img_l
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_LEFT and keys[K_DOWN] != False:
                shark_img_last = shark_img_d
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_DOWN and keys[K_RIGHT] != False:
                shark_img_last = shark_img_r
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])

            elif event.key == K_RIGHT and keys[K_DOWN] != False:
                shark_img_last = shark_img_d
                shark_img = shark_img_last
                shark_rect = shark_img.get_rect(x=pos[0], y=pos[1])
            
    if (pos[0] + keys[K_RIGHT] - keys[K_LEFT] > 0 and pos[0] + keys[K_RIGHT] - keys[K_LEFT] < window_width-shark_img.get_width()):
        pos[0] += keys[K_RIGHT] - keys[K_LEFT]
    if (pos[1] + keys[K_DOWN] - keys[K_UP] > 0 and pos[1] + keys[K_DOWN] - keys[K_UP] < window_height-shark_img.get_height()):
        pos[1] += keys[K_DOWN] - keys[K_UP]
    
    screen.blit(background_image, [0, 0])
    screen.blit(shark_img, pos)
    '''
    '''
    for rect in fish_rects:
        if pygame.Rect.colliderect(rect, shark_rect):
            (fish_x, fish_y) = (randint(0, window_width-15), randint(0, window_height-15))
            
            index = fish_rects.index(rect)
            
            fish_rects[index] = fish_imgs[index].get_rect(x=fish_x, y=fish_y)
            fish_coords[index] = [fish_x, fish_y]
            score_value +=1

    i = 0
    while i < fish_num:
        screen.blit(fish_imgs[i], fish_coords[i])
        i+=1
    '''
    fishes.fish_loop(player.getSharkRect())

    #show_score(sb_x, sb_y)
    pygame.display.flip()
    clock.tick(clock_tick_rate)
