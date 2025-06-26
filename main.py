from time import sleep

import pygame
import os
import math

print(f"[DEBUG] Current directory: {os.getcwd()}")

from src.fps import render_fps
from src.test import run_tests
from src.world import World
from src.render import Render
from src.interactions import handle_player_input, pause
from src.physics import PhysicsEngine
from src.sound import SoundEngine
from src.elements.Entity import Player, Tooltip
from src.deathscreen import handle_player_death
from src.startscherm import startScreen
from src.optionsmenu import handle_options_menu
from src.particles import ParticleSystem
from src.utils.font import comic_sans_large, comic_sans

# initialize game
pygame.init()
sound_engine = SoundEngine()
SELECTED_MAP = startScreen(sound_engine)
pygame.display.set_caption('MURA')

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window.fill((0, 0, 0))

clock = pygame.time.Clock()
physics_engine = PhysicsEngine(sound_engine)

def cache_levels():
    # Level caching code
    sound_engine.play_music("music/intro.wav")
    WIDTH, HEIGHT = window.get_size()
    scaleX = WIDTH / 1920
    scaleY = HEIGHT / 1080
    x_offset = 15 * scaleX
    y_offset =  15 * scaleY
    i = 0

    background_image = pygame.image.load("src/sprites/start.png").convert_alpha()
    background_image = pygame.transform.scale(
        background_image,
        (WIDTH, HEIGHT)
    )
    background_rect = background_image.get_rect(topleft=(0, 0))
    window.blit(background_image, background_rect)

    world_name = comic_sans.render("Creating Level Caches", True, (0, 0, 0))
    world_rect = world_name.get_rect(topleft=(x_offset, y_offset))
    window.blit(world_name, world_rect)
    pygame.display.flip()

    for world in os.listdir("src/worlds"):
        physics_engine.world.load_world(world)
        world_name = comic_sans.render(world + " Has been cached", True, (50, 50, 50))
        world_rect = world_name.get_rect(topleft=(x_offset, y_offset + i * 30 * scaleY + 40))
        window.blit(world_name, world_rect)
        pygame.display.flip()
        i += 1

    world_name = comic_sans.render("Joining World", True, (0, 0, 0))
    world_rect = world_name.get_rect(topleft=(x_offset, y_offset + i * 30 * scaleY + 40))
    window.blit(world_name, world_rect)
    pygame.display.flip()

    rect_color = (0, 0, 0, int(256 / 16))
    rect_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, rect_color, rect_surface.get_rect())
    volume = 1
    for i in range(int(256 / 4)):
        window.blit(rect_surface, (0, 0))
        pygame.display.flip()
        volume -= 1 / (256 / 16)
        sound_engine.set_volume(volume)
        sleep(0.05)
    sound_engine.stop_music()
    sound_engine.set_volume(0.5)

if SELECTED_MAP != "EDITOR":
    cache_levels()

physics_engine.world.load_world(SELECTED_MAP)
physics_engine.player = physics_engine.world.get_entity("Player")
particle_system = ParticleSystem()

# load and scale background
window_width, window_height = window.get_size()
background = pygame.image.load("src/sprites/background_1.png").convert()
zoom_factor = 1.2
background_width = int(window_width * zoom_factor)
background_height = int(window_height * zoom_factor)
background = pygame.transform.scale(background, (background_width, background_height))

# Initialize the renderer
render = Render(window, physics_engine)

fps_label = render_fps(0)

# play music
sound_engine.play_music("music/play_loop.wav", loops=-1)

# main game loop
running = True
paused = False
show_options_menu = False
while running:
    clock.tick(60)
    events = pygame.event.get()
    paused = pause(events, paused)
    if not paused:
        window.fill((100, 100, 100))

        physics_engine.update(render.deltatime)
        physics_engine.check_teleport()
        physics_engine.check_death()
        physics_engine.toggle_tooltips()
        physics_engine.update_enemy_positions()

        if physics_engine.player and not physics_engine.player.alive:
            running = handle_player_death(window, physics_engine.player)

        # handle player input and determine if the game should keep running
        running = handle_player_input(events, physics_engine, sound_engine, particle_system, render)

        # options menu toggling
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_options_menu = not show_options_menu
                    paused = show_options_menu
        
        # options menu handling
        if show_options_menu:
            choice = handle_options_menu(window, sound_engine)
            if choice == "resume":
                show_options_menu = False
                paused = False
            elif choice == "main_menu":
                SELECTED_MAP = startScreen(sound_engine)
                sound_engine.play_music("music/play_loop.wav", loops=-1)
                physics_engine.world.load_world(SELECTED_MAP)
                physics_engine.player = physics_engine.world.get_entity("Player")
                show_options_menu = False
                paused = False
            elif choice == "exit":
                running = False

        run_tests(window, physics_engine.player)

        render.draw_background(background, background_width, background_height, window_width, window_height)
        render.draw_game_elements()
        render.draw_UI()
        particle_system.update()
        particle_system.draw(window)


    if physics_engine.level_finished:

        if physics_engine.finish_time is None:
            physics_engine.finish_time = pygame.time.get_ticks()
        # Zet de vlag weer op False, zodat het niet opnieuw wordt uitgevoerd.
        physics_engine.level_finished = False
    pygame.display.flip()

pygame.quit()
