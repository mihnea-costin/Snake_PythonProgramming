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

        if head_rect.colliderect(food_rect):
            self.score = self.score + 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if (self.head.x > self.w - BLOCK_SIZE or 
            self.head.x < 0 or 
            self.head.y > self.h - BLOCK_SIZE or 
            self.head.y < 0):
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        # check if the snake's head collides with the obstacle
        head_rect = pygame.Rect(
            self.head.x, self.head.y, 
            BLOCK_SIZE, BLOCK_SIZE)

        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(
                obstacle['x']-10, obstacle['y']-10,
                20, 20)
            if head_rect.colliderect(obstacle_rect):
                return True
    
    def _update_ui(self):
        self.display.fill(BLACK)
    
        for pt in self.snake:
            pygame.draw.rect(
                self.display, BLUE1, 
                pygame.Rect(pt.x, pt.y, 
                            BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(
                self.display, BLUE2, 
                pygame.Rect(pt.x+2, pt.y+2, 
                            BLOCK_SIZE-4, BLOCK_SIZE-4))
        
        pygame.draw.rect(
            self.display, RED, 
            pygame.Rect(
                self.food.x, self.food.y, 
                BLOCK_SIZE, BLOCK_SIZE)
                )

        # draw the obstacles from the obstacles list as circles
        for obstacle in game_obstacles:
            pygame.draw.circle(
                self.display, obstacle["color"],
                (obstacle["x"], obstacle["y"]), 10)

        score_text = font.render(
            f"Party: {self.current_party_index}", True,
            WHITE)
        self.display.blit(score_text, (10, 10))
        
        pygame.display.update()
    
    def _move(self, direction):
        if direction == Direction.LEFT:
            self.head = Point(self.head.x-BLOCK_SIZE, self.head.y)
        elif direction == Direction.RIGHT:
            self.head = Point(self.head.x+BLOCK_SIZE, self.head.y)
        elif direction == Direction.UP:
            self.head = Point(self.head.x, self.head.y-BLOCK_SIZE)
        elif direction == Direction.DOWN:
            self.head = Point(self.head.x, self.head.y+BLOCK_SIZE)
    
    def _place_food(self):
        while True:
            food_x = random.randint(0, self.w - BLOCK_SIZE)
            food_y = random.randint(0, self.h - BLOCK_SIZE)
            is_on_obstacle = False
            for obstacle in self.obstacles:
                if (food_x == obstacle["x"] and 
                    food_y == obstacle["y"]):
                    is_on_obstacle = True
                    break
            if not is_on_obstacle:
                break
        self.food = Point(food_x, food_y)
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        font = pygame.font.SysFont(font_name, int(font_size * self.w / 500))
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def get_high_score(self, list_of_scores):
        return max(list_of_scores)

if __name__ == '__main__':
    game = SnakeGame()
    game.current_party_index = 1
    num_parties = 6 # number of parties to play
    game.list_of_scores = []
    terminated = False