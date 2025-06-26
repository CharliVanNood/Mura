import pygame
from src.config import WALKING_SPEED

def check_mouse_hit(mouse_x, mouse_y, obj_x1, obj_y1, obj_x2, obj_y2):
    return mouse_x > obj_x1 and mouse_x < obj_x2 and mouse_y > obj_y1 and mouse_y < obj_y2

def check_buttons_hover(physics_engine, mouse_x, mouse_y):
    for button in physics_engine.world.buttons:
        button["hover"] = check_mouse_hit(mouse_x, mouse_y, button["pos"][0], button["pos"][1], button["pos"][0] + button["pos"][2], button["pos"][1] + button["pos"][3])
        if not button["active"] and button["hover"]: button["color"] = (150, 150, 150)
        elif not button["active"]: button["color"] = (200, 200, 200)

def check_buttons_clicked(physics_engine, mouse_x, mouse_y):
    for button in physics_engine.world.buttons:
        if check_mouse_hit(mouse_x, mouse_y, button["pos"][0], button["pos"][1], button["pos"][0] + button["pos"][2], button["pos"][1] + button["pos"][3]):
            button["active"] = True
            button["color"] = (100, 100, 100)

# check player input and react accordingly
def handle_player_input(events, physics_engine, sound_engine, particle_system, render):
    player = physics_engine.world.get_entity("Player")
    for e in events:
        keys = pygame.key.get_pressed()
        if e.type == pygame.QUIT:
            return False

        if e.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_buttons_hover(physics_engine, mouse_x, mouse_y)

        # particle test above player
        if keys[pygame.K_u]:
            render.emit_particles(player, particle_system, (0, 255, 0), 20)

    physics_engine.walk(player, WALKING_SPEED * render.deltatime)
    physics_engine.jump(player, sound_engine)
    physics_engine.change_gravity(player)
    return True


def pause(events, paused):
    for e in events:
        if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
            return not paused
    return paused