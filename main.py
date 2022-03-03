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

window_width=612
window_height=437

step=10
clock_tick_rate=120

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Shark Bait")

clock = pygame.time.Clock()
background_image = pygame.image.load("ocean_background.png").convert()

# Load Shark Right
shark_img_pre_r = pygame.image.load('shark_model_right.png')
shark_img_r = pygame.transform.rotozoom(shark_img_pre_r, 0, 0.1)
shark_img_r.convert_alpha()
shark_img_r_rect = shark_img_r.get_rect()
shark_x = window_width//2
shark_y = window_height//2

# Load Shark Left
shark_img_pre_l = pygame.image.load('shark_model_left.png')
shark_img_l = pygame.transform.rotozoom(shark_img_pre_l, 0, 0.1)
shark_img_l.convert_alpha()
shark_img_l_rect = shark_img_l.get_rect()

# Load Shark Up
shark_img_pre_u = pygame.image.load('shark_model_up.png')
shark_img_u = pygame.transform.rotozoom(shark_img_pre_u, 0, 0.1)
shark_img_u.convert_alpha()
shark_img_u_rect = shark_img_u.get_rect()

# Load Shark Down
shark_img_pre_d = pygame.image.load('shark_model_down.png')
shark_img_d = pygame.transform.rotozoom(shark_img_pre_d, 0, 0.1)
shark_img_d.convert_alpha()
shark_img_d_rect = shark_img_d.get_rect()

# Load Fishes
fish_num = 5
i = 0
fish_coords = {}
fish_imgs = []
fish_rects = []
while i < fish_num:
    fish_x = randint(0, 600)
    fish_y = randint(0, 420)
    fish_coords[i] = [fish_x, fish_y]
    fish_img_pre = pygame.image.load('fish_model.png')
    fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.02)
    fish_img.convert_alpha()
    fish_imgs.append(fish_img)
    fish_rects.append(fish_img.get_rect())
    i+=1

# Game Loop
pos = [shark_x, shark_y]
dead=False
shark_img = shark_img_r
shark_rect = shark_img_r_rect
while(dead==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

    keys = pygame.key.get_pressed()

    pos[0] += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    pos[1] += keys[pygame.K_DOWN] - keys[pygame.K_UP]

    if event.type == KEYDOWN:
        if event.key == K_RIGHT:
            shark_img = shark_img_r
            shark_rect = shark_img_r_rect

        elif event.key == K_LEFT:
            shark_img = shark_img_l
            shark_rect = shark_img_l_rect
        
        elif event.key == K_UP:
            shark_img = shark_img_u
            shark_rect = shark_img_u_rect

        elif event.key == K_DOWN:
            shark_img = shark_img_d
            shark_rect = shark_img_d_rect

        i = 0

    screen.blit(background_image, [0, 0])
    screen.blit(shark_img, pos)
    i = 0
    while i < fish_num:
        screen.blit(fish_imgs[i], fish_coords[i])
        i+=1
    pygame.display.flip()
    clock.tick(clock_tick_rate)