import pygame
import sys
import os
from src.utils.font import comic_sans, comic_sans_large

SELECTED_MAP = 'level1'

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption('TEAM INSPIRATIELOOS')
clock = pygame.time.Clock()

scaleX = WIDTH / 1920
scaleY = HEIGHT / 1080

ORANGE = (100, 100, 100)
DARK_BROWN= (50, 50, 50)

title_font = comic_sans_large
button_font = comic_sans
button_rect = pygame.Rect(WIDTH // 2 - 100 * scaleX, HEIGHT // 2 + 100 * scaleY, 200 * scaleX, 60 * scaleY)
edit_button_rect = pygame.Rect( WIDTH // 2 - 100 * scaleX, HEIGHT // 2 + 180 * scaleY, 200 * scaleX, 60 * scaleY)
quit_button_rect = pygame.Rect( WIDTH // 2 - 100 * scaleX, HEIGHT // 2 + 260 * scaleY, 200 * scaleX, 60 * scaleY)

world_buttons = []

play_button_hover = False
edit_button_hover = False
quit_button_hover = False

naam_font = comic_sans
namen = ["Ceren", "Charli", "Jens", "Mathijs", "Myla"]

dragging_scrollbar = False
scrollbar_click_offset = 0


scroll_offset = 0
SCROLL_SPEED = 20 * scaleY
SCROLL_AREA_TOP = HEIGHT // 2 + 100 * scaleY
SCROLL_AREA_HEIGHT = 400 * scaleY

def startScreen(sound_engine):
    global SELECTED_MAP, world_buttons
    world_buttons.clear()  # reset voor herstart

    i = 0
    for world in os.listdir("src/worlds"):
        y_pos = SCROLL_AREA_TOP + 100 * scaleY * i
        world_buttons.append([
            pygame.Rect(WIDTH // 2 + 150 * scaleX, y_pos, 200 * scaleX, 60 * scaleY),
            comic_sans,
            world,
            i == 0, False
        ])
        if i == 0:
            SELECTED_MAP = world
        i += 1

    start_screen(sound_engine)
    return SELECTED_MAP

# Namen van de auteurs op startscherm.
def auteurs():
    x_rechts = 15 * scaleX
    y_boven =  15 * scaleY
    for i, naam in enumerate(namen):
        naam_text = naam_font.render(naam, True, (50, 50, 50))
        naam_rect = naam_text.get_rect(topleft=(x_rechts, y_boven + i * 35 * scaleY))
        screen.blit(naam_text, naam_rect)

# Startscherm wordt getekend.
def draw_start_screen():
    global play_button_hover, edit_button_hover, quit_button_hover

    screen.fill(DARK_BROWN)
    
    background_image = pygame.image.load("src/sprites/start.png").convert_alpha()
    background_image = pygame.transform.scale(
        background_image,
        (WIDTH, HEIGHT)
    )
    background_rect = background_image.get_rect(topleft=(0, 0))
    screen.blit(background_image, background_rect)

    background_image = pygame.image.load("src/sprites/mura.png").convert_alpha()
    background_image = pygame.transform.scale(
        background_image,
        (500 * scaleX, 400 * scaleY)
    )
    background_rect = background_image.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(background_image, background_rect)

    if play_button_hover:
        pygame.draw.rect(screen, (255,255,255), button_rect)
    else:
        pygame.draw.rect(screen, (200,200,200), button_rect)
    button_text = button_font.render('Start', True, DARK_BROWN)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    # edit button
    if edit_button_hover:
        pygame.draw.rect(screen, (255,255,255), edit_button_rect)
    else:
        pygame.draw.rect(screen, (200,200,200), edit_button_rect)
    edit_text = button_font.render('Editor', True, DARK_BROWN)
    screen.blit(edit_text, edit_text.get_rect(center=edit_button_rect.center))

    # quit button
    if quit_button_hover:
        pygame.draw.rect(screen, (255,255,255), quit_button_rect)
    else:
        pygame.draw.rect(screen, (200,200,200), quit_button_rect)
    quit_text = button_font.render('Quit', True, DARK_BROWN)
    screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))

    scrollbar_height = SCROLL_AREA_HEIGHT * (SCROLL_AREA_HEIGHT / (len(world_buttons) * 100 * scaleY))
    scrollbar_pos = scroll_offset / (len(world_buttons) * 100 * scaleY) * SCROLL_AREA_HEIGHT
    pygame.draw.rect(screen, (200, 200, 200), (
        WIDTH // 2 + 360 * scaleX,
        SCROLL_AREA_TOP + scrollbar_pos,
        10 * scaleX,
        scrollbar_height
    ))

    scroll_area_rect = pygame.Rect(
        WIDTH // 2 + 150 * scaleX,
        SCROLL_AREA_TOP,
        200 * scaleX,
        SCROLL_AREA_HEIGHT
    )

    # Maak een aparte surface voor de scrollbare inhoud
    scroll_surface = pygame.Surface((scroll_area_rect.width, scroll_area_rect.height), pygame.SRCALPHA)
    scroll_surface.fill(DARK_BROWN)

    for button in world_buttons:
        rect = button[0].copy()
        rect.y -= scroll_offset  # toepassen scroll
        local_rect = rect.move(-scroll_area_rect.x, -SCROLL_AREA_TOP)  # relatieve positie binnen scroll_surface

        if scroll_surface.get_rect().colliderect(local_rect):
            if button[3]:
                pygame.draw.rect(scroll_surface, (255, 255, 255), local_rect)
                button_text = button[1].render(button[2], True, DARK_BROWN)
            elif button[4]:
                pygame.draw.rect(scroll_surface, (200, 200, 200), local_rect)
                button_text = button[1].render(button[2], True, DARK_BROWN)
            else:
                pygame.draw.rect(scroll_surface, ORANGE, local_rect)
                button_text = button[1].render(button[2], True, DARK_BROWN)
            scroll_surface.blit(button_text, button_text.get_rect(center=local_rect.center))

    # Plak de scrollbare inhoud op het hoofdscherm (alleen zichtbaar binnen scroll_area_rect)
    screen.blit(scroll_surface, scroll_area_rect.topleft)

    auteurs()
    pygame.display.flip()


def start_screen(sound_engine):
    global SELECTED_MAP, scroll_offset
    global play_button_hover, edit_button_hover, quit_button_hover

    sound_engine.play_music("music/8up9down.mp3")
    dragging_scrollbar = False
    scrollbar_click_offset = 0

    waiting = True
    while waiting:
        draw_start_screen()

        # Bereken scrollbar eigenschappen
        total_height = len(world_buttons) * 100 * scaleY
        max_offset = max(0, total_height - SCROLL_AREA_HEIGHT)
        scrollbar_height = SCROLL_AREA_HEIGHT * (SCROLL_AREA_HEIGHT / total_height) if total_height > 0 else SCROLL_AREA_HEIGHT
        scrollbar_pos = scroll_offset / total_height * SCROLL_AREA_HEIGHT if total_height > 0 else 0

        scrollbar_rect = pygame.Rect(
            WIDTH // 2 + 360 * scaleX,
            SCROLL_AREA_TOP + scrollbar_pos,
            10 * scaleX,
            scrollbar_height
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False
                elif edit_button_rect.collidepoint(event.pos):
                    print("EDITING :D")
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif scrollbar_rect.collidepoint(event.pos):
                    dragging_scrollbar = True
                    scrollbar_click_offset = event.pos[1] - scrollbar_rect.y
                else:
                    selected_level = False
                    for button in world_buttons:
                        rect = button[0].copy()
                        rect.y -= scroll_offset
                        if rect.collidepoint(event.pos):
                            selected_level = button
                    if selected_level:
                        for button in world_buttons:
                            button[3] = False
                        selected_level[3] = True
                        SELECTED_MAP = selected_level[2]

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_scrollbar = False

            elif event.type == pygame.MOUSEMOTION:
                play_button_hover = False
                edit_button_hover = False
                quit_button_hover = False

                if dragging_scrollbar:
                    # Bereken nieuwe scrollbar-positie
                    new_y = event.pos[1] - scrollbar_click_offset
                    relative_scroll = (new_y - SCROLL_AREA_TOP) / SCROLL_AREA_HEIGHT
                    scroll_offset = relative_scroll * total_height
                    scroll_offset = max(0, min(scroll_offset, max_offset))
                else:
                    if button_rect.collidepoint(event.pos):
                        play_button_hover = True
                    elif edit_button_rect.collidepoint(event.pos):
                        edit_button_hover = True
                    elif quit_button_rect.collidepoint(event.pos):
                        quit_button_hover = True
                    else:
                        for button in world_buttons:
                            rect = button[0].copy()
                            rect.y -= scroll_offset
                            button[4] = rect.collidepoint(event.pos)

            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * SCROLL_SPEED
                scroll_offset = max(0, min(scroll_offset, max_offset))

        clock.tick(60)
    
    sound_engine.stop_music()


