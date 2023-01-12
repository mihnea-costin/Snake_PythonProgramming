import pygame
import random
import json
import sys 
from enum import Enum
from collections import namedtuple

pygame.init()

font_size = 25
font = pygame.font.SysFont('arial', font_size)
# obtain the font name
font_name = pygame.font.get_default_font()

# Check if a filename was passed as an argument
if len(sys.argv) < 2:
    print("Error: No configuration file provided")
    sys.exit()

# Read the configuration data from the file
filename = sys.argv[1]
with open(filename, 'r') as f:
    config = json.load(f)

# Set the game window size and obstacles using the configuration data
game_width = config['width']
game_height = config['height']
game_obstacles = config['obstacles']

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

class Circle:
    def __init__(
            self, x, y, radius, 
            color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

BLUE1 = pygame.Color('blue')
BLUE2 = pygame.Color('dodgerblue1')

RED = pygame.Color('red')

BLOCK_SIZE = 20

SPEED = 5

class Party:
    def __init__(self):
        self.score = 0
        self.is_playing = True

class SnakeGame:
    
    def __init__(
            self, w=game_width, h=game_height,
            obstacles=game_obstacles):

        self.w, self.h = w, h
        self.obstacles = obstacles

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake game')
        
        self.clock = pygame.time.Clock()
