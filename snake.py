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

        self.score = 0
        self.food = None
        self._place_food()
        self.current_party = Party() # start the first party

        # init game state
        self.direction = Direction.LEFT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.direction = Direction.LEFT
        elif key[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT
        elif key[pygame.K_UP]:
            self.direction = Direction.UP
        elif key[pygame.K_DOWN]:
            self.direction = Direction.DOWN    
        
        # 2. move
        self._move(self.direction) 
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            self.current_party.is_playing = False 
            self.current_party.score = self.score 
            return game_over, self.score
        
        head_rect = pygame.Rect(self.head.x, self.head.y, 
                                BLOCK_SIZE, BLOCK_SIZE)
        food_rect = pygame.Rect(self.food.x, self.food.y, 
                                BLOCK_SIZE, BLOCK_SIZE)

    