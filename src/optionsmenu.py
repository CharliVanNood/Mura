import pygame

def handle_options_menu(screen, sound_engine):
    font = pygame.font.SysFont('Comic Sans MS', 40)

    options = ["Return to Game", "Return to Main Menu", "Exit Game", "Volume Up", "Volume Down"]
    selected = 0

    screen_width, screen_height = screen.get_size()
    line_height = 60  # space between lines
    total_menu_height = len(options) * line_height
    top_y = (screen_height - total_menu_height) // 2  # vertical centering

    while True:
        screen.fill((50, 50, 50))

        # print buttons
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected else (130, 130, 130)
            text_surface = font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, top_y + i * line_height))
            screen.blit(text_surface, text_rect)
        
        # volume indicator
        current_volume = sound_engine.get_volume()
        current_volume = "Volume: " + str(round(current_volume * 100)) + "%"
        volume_surface = font.render((current_volume), True, (255, 255, 255))
        volume_rect = volume_surface.get_rect(center=(screen_width // 2, screen_height * 0.75))
        screen.blit(volume_surface, volume_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if options[selected] == "Return to Game":
                        return "resume"
                    elif options[selected] == "Volume Up":
                        sound_engine.adjust_volume(0.1)
                    elif options[selected] == "Volume Down":
                        sound_engine.adjust_volume(-0.1)
                    elif options[selected] == "Return to Main Menu":
                        return "main_menu"
                    elif options[selected] == "Exit Game":
                        return "exit"