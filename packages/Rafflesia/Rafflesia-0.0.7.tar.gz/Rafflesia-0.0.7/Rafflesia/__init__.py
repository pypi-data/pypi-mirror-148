import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "0"
import pygame

pygame.init()

__version__ = "0.0.7"

from .AudioManager import *
