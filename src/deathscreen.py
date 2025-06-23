import pygame

from src.scoring import loading_score
from src.utils.font import comic_sans, title_font
from src.scoring import death_score

def show_death_screen(screen):
    """Displays the death screen """
    current_score = loading_score()

    WIDTH, HEIGHT = screen.get_size()

    # Dim overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # "You Died!" text
    text = title_font.render('You Died!', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(text, text_rect)

    # Score text
    score_text = comic_sans.render(f'Score: {current_score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(score_text, score_rect)

    # Respawn button
    respawn_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 60)
    pygame.draw.rect(screen, (255, 255, 255), respawn_button, border_radius=8)
    respawn_text = comic_sans.render('Respawn', True, (0, 0, 0))
    respawn_text_rect = respawn_text.get_rect(center=respawn_button.center)
    screen.blit(respawn_text, respawn_text_rect)

    # Quit button
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
    pygame.draw.rect(screen, (0, 0, 0), quit_button, border_radius=8)
    quit_text = comic_sans.render('Quit', True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)


    #death counter
    with open ("deaths.txt", 'r') as f:
        deaths = int(f.read())
    death_text = comic_sans.render(f'Deaths: {deaths}', True, (255, 255, 255))
    death_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(death_text, death_rect)
    pygame.display.update()

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if respawn_button.collidepoint(mouse_pos):
                    return "respawn"
                elif quit_button.collidepoint(mouse_pos):
                    return "quit"



def handle_player_death(window, player):
    """Handles button results from death screen and updates score"""
    if not player.alive:
        new_score = death_score(window,player)
        result = show_death_screen(window)
        if result == "respawn":
            player.respawn()
            return True
        elif result == "quit":
            exit()