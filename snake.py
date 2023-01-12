import random
import json
import sys 

from enum import Enum
from collections import namedtuple

import pygame

pygame.init()

font_size = 25
font_name = 'arial'
font = pygame.font.SysFont(font_name, font_size)

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
    """ A class for defining the directions"""
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    R = 5
    
Point = namedtuple('Point', 'x, y')

class Circle:
    def __init__(
            self, x, y, radius, 
            color):
        """ A class for defining a circle with its coordinates, radius and color"""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

# This code defines some colors
BLUE = pygame.Color('blue')
LIGHT_BLUE = pygame.Color('dodgerblue1')

RED = pygame.Color('red')
LIGHT_RED = pygame.Color('red1')

ORANGE = pygame.Color('orange')
DARK_ORANGE = pygame.Color('orange2')

YELLOW = pygame.Color('yellow')
LIGHT_YELLOW = pygame.Color('yellow1')

GREEN = pygame.Color('green')
LIGHT_GREEN = pygame.Color('green1')
DARK_GREEN = pygame.Color('forestgreen')

PURPLE = pygame.Color('purple')
LIGHT_PURPLE = pygame.Color('purple1')

PINK = pygame.Color('pink')
LIGHT_PINK = pygame.Color('pink1')

BLACK = pygame.Color('black')

WHITE = pygame.Color('white')

BLOCK_SIZE = 20

SNAKE_SPEED = 5

class Party:
    """This class represents a party of the snake game"""
    def __init__(self):
        """This code initializes the party"""
        self.score = 0
        self.is_playing = True

class Snake:
    """This class represents the snake game with all the initialisations"""		
    def __init__(
            self, w=game_width, h=game_height,
            obstacles=game_obstacles):
        """ This code initializes the game """

        self.w, self.h = w, h
        self.obstacles = obstacles

        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake game')
        
        self.clock = pygame.time.Clock()

        self.score = 0
        self.food = None
        self.food_placing()
        self.current_party = Party() # start the first party

        # init game state
        self.direction = Direction.LEFT
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]

    def play_step(self):
        """ This code plays a single step of the game """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # This code checks for the key pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.direction = Direction.LEFT
        elif key[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT
        elif key[pygame.K_UP]:
            self.direction = Direction.UP
        elif key[pygame.K_DOWN]:
            self.direction = Direction.DOWN   
        elif key[pygame.K_r]:
            # chooses random on the 4 directions
            self.direction = random.choice(list(Direction))
        
        # This code moves the snake
        self.move(self.direction) 
        self.snake.insert(0, self.head)

        # This code checks if the game is over
        game_over = False
        if self.collision_check():
            game_over = True
            self.current_party.is_playing = False 
            self.current_party.score = self.score 
            return game_over, self.score
        
        head_rect = pygame.Rect(self.head.x, self.head.y, 
                                BLOCK_SIZE, BLOCK_SIZE)
        food_rect = pygame.Rect(self.food.x, self.food.y, 
                                BLOCK_SIZE, BLOCK_SIZE)

        # This code checks if the snake collids the food
        if head_rect.colliderect(food_rect):
            self.score = self.score + 1 # Increase the score 
            self.food_placing()
        else:
            self.snake.pop()

        self.ui_updating()
        self.clock.tick(SNAKE_SPEED)
        # Returns game over value and the score of the party
        return game_over, self.score

    def collision_check(self):
        """This code checks if the snake collides with itself, the wall or the obstacles"""
        # This code checks if the snake collides with the wall
        if (self.head.x > self.w - BLOCK_SIZE or 
            self.head.x < 0 or 
            self.head.y > self.h - BLOCK_SIZE or 
            self.head.y < 0):
            return True

        # This code checks if the snake collides with itself
        if self.head in self.snake[1:]:
            return True

        head_rect = pygame.Rect(
            self.head.x, self.head.y, 
            BLOCK_SIZE, BLOCK_SIZE)

        # This code checks if the snake's head collides with the obstacle
        for obstacle in self.obstacles:
            obstacle_rect = pygame.Rect(
                obstacle['x']-10, obstacle['y']-10,
                20, 20)
            if head_rect.colliderect(obstacle_rect):
                return True
    
    def ui_updating(self):
        """This code updates the UI"""
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
        
        # Draw the food as a rectangle
        pygame.draw.rect(
            self.display, RED, 
            pygame.Rect(
                self.food.x, self.food.y, 
                BLOCK_SIZE, BLOCK_SIZE))

        # Draw the obstacles from the obstacles list as circles
        for obstacle in game_obstacles:
            pygame.draw.circle(
                self.display, obstacle["color"],
                (obstacle["x"], obstacle["y"]), 10)

        score_text = font.render(
            f"Party: {self.current_party_index}", True,
            WHITE)
        self.display.blit(score_text, (10,10))
        
        pygame.display.update()
    
    directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

    def move(self, direction):
        """ This code moves the snake"""
        # This code moves the snake in one of the 4 directions
        if direction == Direction.LEFT:
            self.head = Point(
                self.head.x-BLOCK_SIZE, self.head.y)
        elif direction == Direction.RIGHT:
            self.head = Point(
                self.head.x+BLOCK_SIZE, self.head.y)
        elif direction == Direction.UP:
            self.head = Point(
                self.head.x, self.head.y-BLOCK_SIZE)
        elif direction == Direction.DOWN:
            self.head = Point(
                self.head.x, self.head.y+BLOCK_SIZE)
        # This code moves the snake in a random choosen direction
        elif direction == Direction.R:
            # This code moves the snake in one of the 4 directions
            new_direction = random.choice(Direction)
            if new_direction == Direction.LEFT:
                self.head = Point(
                    self.head.x-BLOCK_SIZE, self.head.y)
            if new_direction == Direction.RIGHT:
                self.head = Point(
                    self.head.x+BLOCK_SIZE, self.head.y)
            if new_direction == Direction.UP:
                self.head = Point(
                    self.head.x, self.head.y-BLOCK_SIZE)
            if new_direction == Direction.DOWN:
                self.head = Point(
                    self.head.x, self.head.y+BLOCK_SIZE)
            
    def food_placing(self):
        """This code is placing the food randomly"""
        while True:
            food_x = random.randint(
                0, self.w-BLOCK_SIZE)
            food_y = random.randint(
                0, self.h-BLOCK_SIZE)
            is_on_obstacle = False
            for obstacle in self.obstacles:
                if (food_x == obstacle["x"] and 
                    food_y == obstacle["y"]):
                    is_on_obstacle = True
                    break
            if not is_on_obstacle:
                break
        self.food = Point(food_x, food_y)
    
    def draw_text(
            self, text, font, 
            color, surface, x, y):
        """This code draws the text on the screen"""
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        font = pygame.font.SysFont(
             font_name, int(font_size * self.w/500))
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def get_high_score(
            self, list_of_scores):
        """This code returns the highest score"""
        return max(list_of_scores)

if __name__ == '__main__':
    """This code is the main code, in which the game is played"""
    game = Snake()
    game.current_party_index = 1
    num_parties = 6 
    game.list_of_scores = []
    terminated = False
    # This code is the main loop of the game
    while num_parties > 0:
        while True:
            game_over, score = game.play_step()
            if game_over:
                # Check if there are more parties left
                if num_parties-1 > 0 and terminated == False:
                    # Add the score to the list of scores
                    game.list_of_scores.append(score)
                    # Make the screen black
                    game.display.fill(BLACK)
                    # Ask the player if they want to continue
                    party_msg = f"This party final score is {score}. Press Y to continue, N to exit"
                    game.draw_text(
                             party_msg, font, WHITE, 
                             game.display, game.w/2, game.h/2)
                    pygame.display.update()
                    # Wait for the player's response
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_y:
                                    waiting = False
                                    game.current_party_index += 1
                                    game.__init__()
                                    num_parties = num_parties - 1
                                elif event.key == pygame.K_n:
                                    waiting = False
                                    high_score = game.get_high_score(
                                        game.list_of_scores)
                                    # remove the asking to continue text
                                    game.display.fill(BLACK)
                                    final_msg = f"Game Over! This party score: {score}. High score: {high_score}"
                                    game.draw_text(
                                             final_msg, font, WHITE, 
                                             game.display, game.w/2, game.h/2)
                                    # block the keyboard
                                    pygame.event.set_blocked(pygame.KEYDOWN)
                                    terminated = True
                                    # stop = True
                                    pygame.display.update()
                                    pygame.time.delay(3000)
                else:
                    # break
                    # This displays the game over screen and the high score
                    high_score = game.get_high_score(game.list_of_scores)
                    game.display.fill(BLACK)
                    game.draw_text(f"Game Over! This party score: {score}. High score: {high_score}", font, WHITE, game.display, game.w/2, game.h/2)
                    # This blocks the keyboard
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    pygame.display.update()
                    pygame.time.delay(3000)
