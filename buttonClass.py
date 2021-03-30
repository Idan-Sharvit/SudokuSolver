import pygame
from Settings import *

class Button:
    colours = {
        'blue': (27, 142, 207),
        'gray': (73, 73, 73),
        'green': (3, 162, 2),
        'cyan': (189, 189, 189)
    }
    colour = colours['gray']
    highlighted_colour = colours['cyan']
    
    def __init__(self, x, y, width, height, **kwargs) -> None:
        self.image = pygame.Surface((width, height))
        self.position = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.__dict__.update(kwargs)
        self.highlighted = False
        self.width = width
        self.height = height
    
    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False
        
    def draw(self, window):
        if self.highlighted:
            self.image.fill(self.highlighted_colour)
        else:
            self.image.fill(self.colour)
        
        if self.text:
            self.draw_text(self.text)

        window.blit(self.image, self.position)     

    def draw_text(self, text):
        font = pygame.font.SysFont("arial", 20, bold=1)
        text = font.render(text, False, BLACK)
        width, height = text.get_size()
        x = (self.width - width) // 2
        y = (self.height - height) // 2
        self.image.blit(text, (x, y))
        
