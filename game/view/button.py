import pygame
from pygame.locals import *


class MyButton(pygame.sprite.Sprite):
    rect = None
    surface = None
    
    def __init__(self, font, text, text_color, bg_color):
        super(MyButton, self)
        
        self.surface = font.render(text, True, text_color, bg_color)
        self.rect = self.surface.get_rect()
    
    def set_coords(self, x, y):
        self.rect.center = (x, y)
