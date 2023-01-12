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