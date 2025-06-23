import pygame

pygame.font.init()
# fonts

comic_sans = pygame.font.SysFont('Comic Sans MS', 25)
comic_sans_small = pygame.font.SysFont('Comic Sans MS', 12)
title_font = pygame.font.SysFont('Comic Sans MS', 30)
instruction_font = pygame.font.SysFont('Comic Sans MS', 40)
button_font = pygame.font.SysFont('Comic Sans MS', 40)
comic_sans_large = pygame.font.SysFont("Comic Sans MS", 80)
button_rect = pygame.Rect(800 // 2 - 100, 600 // 2 + 20, 200, 60)
button_text = button_font.render('start', True, (101, 67, 33))

