import pygame
from src.fps import get_fps, render_fps
from src.utils.font import comic_sans_small, comic_sans
from src.config import TILESIZE
from src.utils.vectors import Vector2
from src.elements.Entity import Tooltip, Entity, Player
import math
import time

class Render():
    def __init__(self, window, physics_engine):
        self.window = window
        self.physics_engine = physics_engine
        self.camera_position = Vector2(0, 0)
        self.deltatime = 1

    # updates current fps and renders it on screen
    def update_fps(self):
        fps, self.deltatime = get_fps()
        fps_label = render_fps(fps)
        self.window.blit(fps_label, (0, 0))

    # ---------------------------------- Dead Code? ----------------------------------
    def draw_buttons(self):
        for button in self.physics_engine.world.buttons:
            pygame.draw.rect(self.window, button["color"], button["pos"])

    # updates and draws UI: FPS counter, names & buttons
    def draw_UI(self):
        self.update_fps()
        self.draw_buttons()

    def toggle_tooltips(self):
        for tooltip in self.physics_engine.world.entities:
            if tooltip.name == "Tooltip":
                player_pos = Player.get_pos()
                dx = player_pos[0] - tooltip.pos[0]
                dy = player_pos[1] - tooltip.pos[1]
                distance = math.hypot(dx, dy)

                if distance < 100:
                    tooltip.show(tooltip.pos)
                else:
                    tooltip.hide()

    # draws all world elements
    def draw_world_entities(self):
        #draw_start = time.time()
        #draw_amount = 0
        screen_width = self.window.get_width()
        screen_height = self.window.get_height()
        screen_width_half = screen_width / 2
        screen_height_half = screen_height / 2
        window = self.window
        camera_position_x = self.camera_position.getX() + screen_width_half
        camera_position_y = self.camera_position.getY() + screen_height_half
        for entity in self.physics_engine.world.entities:
            if entity.transparent: continue

            # Bereken camera offset en pas rect aan
            draw_x = entity.position.getX() * TILESIZE + camera_position_x
            draw_y = (0 - entity.position.getY() * TILESIZE - entity.size.getY() * TILESIZE) + \
                        camera_position_y

            if draw_x + entity.size.getX() * TILESIZE < 0: continue
            elif draw_x > screen_width: continue
            if draw_y + entity.size.getY() * TILESIZE < 0: continue
            elif draw_y > screen_height: continue

            if entity.sprite_image is not None or entity.text is not None:
                # Teken sprite op aangepaste positie
                if entity.text is None:
                    window.blit(entity.image, (draw_x, draw_y + entity.sprite_offset))
                elif entity.visible:
                    text = comic_sans.render(entity.text, False, (255, 255, 255))
                    window.blit(text, (draw_x, draw_y))
                #draw_amount += 1
            else:
                pygame.draw.rect(window, entity.color.get(), (draw_x, draw_y,
                    entity.size.getX() * TILESIZE, entity.size.getY() * TILESIZE
                ))
                #draw_amount += 1
        #print("Updated Screen in", str((time.time() - draw_start) * 1000) + "MS with", draw_amount, "elements")

    # ---------------------------------- Dead Code? ----------------------------------
    def draw_red_dots(self):
        for stip in self.physics_engine.world.stippen:
            stip.draw(self.window)

    def update_camera_position(self):
        player = self.physics_engine.world.get_entity("Player")
        self.camera_position.add(
            (-self.camera_position.getX() - player.position.getX() * TILESIZE) * 0.05, 
            (-self.camera_position.getY() - -(player.position.getY() + 5) * TILESIZE) * 0.05
        )

    # draw all game entities and other interactive elements
    def draw_game_elements(self):
        self.update_camera_position()
        self.draw_world_entities()
        # draws the red dots on top of all other elements, will be removed at some point
        self.draw_red_dots()

    def draw_background(self, background, background_width, background_height, window_width, window_height):
        player = self.physics_engine.world.get_entity("Player")

        # apply the parallax effect, where the background moves slower than the player
        # the number 0.1 means the background moves at 10% of the player's speed
        parallax_offset_x = -player.position.getX() * TILESIZE * 0.1
        parallax_offset_y = player.position.getY() * TILESIZE * 0.1

        # calculate the position of the background
        bg_x = (window_width - background_width) // 2 + parallax_offset_x
        bg_y = (window_height - background_height) // 2 + parallax_offset_y

        # make sure the background stops moving when the edge is reached
        min_offset_x = window_width - background_width
        min_offset_y = window_height - background_height
        bg_x = max(min(bg_x, 0), min_offset_x)
        bg_y = max(min(bg_y, 0), min_offset_y)

        self.window.blit(background, (bg_x, bg_y))

    def emit_particles(self, entity, particle_system, color=(255, 255, 255), count=20):
        # X: midden van de speler
        draw_x = (entity.position.getX() + entity.size.getX() / 2) * TILESIZE + self.window.get_width() / 2 + self.camera_position.getX()

        # Y: net boven de speler (dus bovenaan de sprite), met een kleine offset omhoog (-10 pixels)
        draw_y = (0 - (entity.position.getY() + entity.size.getY())) * TILESIZE + self.window.get_height() / 2 + self.camera_position.getY()

        particle_system.emit((draw_x, draw_y), color, count)
