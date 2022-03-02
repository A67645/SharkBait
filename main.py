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
clock_tick_rate=60

# Open a window
size = (window_width, window_height)
screen = pygame.display.set_mode(size)

# Set title to the window
pygame.display.set_caption("Shark Bait")

clock = pygame.time.Clock()
background_image = pygame.image.load("ocean_background.png").convert()

# Load Shark
img_pre = pygame.image.load('shark_model.png')
img = pygame.transform.rotozoom(img_pre, 0, 0.2)
img.convert_alpha()
shark_width = window_width//2
shark_height = window_height//2 

# Load Fishes
number = 5
i = 0
fish_coords = []
fish_img_pre = pygame.image.load('fish_model.png')
fish_img = pygame.transform.rotozoom(fish_img_pre, 0, 0.03)
fish_img.convert_alpha()
while i < number:
    fish_width = randint(0, 600)
    fish_height = randint(0, 420)
    fish_coords.append([fish_width, fish_height])
    i+=1

# Game Loop
pos = [shark_width, shark_height]
dead=False
while(dead==False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            dead = True

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                dead = True

            elif event.key == K_RIGHT and pos[0] < 420:
                pos = [pos[0]+step, pos[1]]

            elif event.key == K_LEFT and pos[0] > 0:
                pos = [pos[0]-step, pos[1]]

            elif event.key == K_UP and pos[1] > 0:
                pos = [pos[0], pos[1]-step]

            elif event.key == K_DOWN and pos[1] < 350:
                pos = [pos[0], pos[1]+step]


    screen.blit(background_image, [0, 0])
    screen.blit(img, pos)
    for coord in fish_coords:
        screen.blit(fish_img, coord)
    pygame.display.flip()
    clock.tick(clock_tick_rate)