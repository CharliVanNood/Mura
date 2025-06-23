import pygame

# ---------------------------------- Dead Code? ----------------------------------
class Stip():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), 10)