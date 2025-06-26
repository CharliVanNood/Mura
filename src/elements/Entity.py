from src.scoring import loading_score
from src.utils.vectors import Vector2
import pygame
import os
import math
import random
from src.utils.font import comic_sans
from src.config import TILESIZE

portal_sprite_path = os.path.join(os.path.dirname(__file__), '..', 'sprites', 'portal_sprite_test.webp')
portal_sprite = os.path.normpath(portal_sprite_path)
finish_sprite_path = os.path.join(os.path.dirname(__file__), '..', 'sprites', 'finish.png')

SHAPES = {"rectangle": 0, "rect": 0, "circle": 1}

class RGB:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def setFromRGB(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
        return self

    def get(self):
        return (self.r, self.g, self.b)

class Entity:
    """
    We have a few base shapes,
    0 = Rectangle
    1 = Circle
    These will dictate what collision methods are used
    """
    def __init__(self, name, shape, position):
        self.name = name
        self.velocity = Vector2(0, 0)
        self.position = Vector2(position[0], position[1])
        self.size = Vector2(1, 1)
        self.shape = shape
        self.weight = 1
        self.color = RGB(100, 0, 200)
        self.transparent = False
        self.collide = True # this indicates if an item will collide
        self.anchored = True # this indicates if an item should move or not
        self.gravity = False # this indicates if an item should have gravity
        self.gravity_direction = Vector2(0, -1) # with this being -1 it will default to falling down
        self.bouncy = False # this indicates is an item should be able to bounce
        self.grounded = False # keep track of interractions
        self.Deadly = False
        self.portal_colliding_with = None # which portal the entity is currently colliding with
        self.fatal_object_colliding_with = None
        self.teleport_cooldown = 0 # keeps track of when the entity can be teleported again
        self.jump_cooldown = True
        self.text = None

        # Sprite related properties
        self.sprite_image = None
        self.sprite_surface = None
        self.sprite_name = None
        self.sprite_animation_frame = 0
        self.sprite_animation_sequence = None
        self.sprite_offset = 0
        self.rotation = 0
        self.update_sprite()
        self.previous_rotation = 0

    def setCollide(self, collide):
        self.collide = collide
        return self
    
    def setTransparent(self, transparent):
        self.transparent = transparent
        return self

    def setVelocity(self, x, y):
        self.velocity.set(x, y)
        return self # this return is so it's possible to stack modifiers

    def addVelocity(self, x, y):
        self.velocity.add(x, y)
        return self # this return is so it's possible to stack modifiers

    def setPosition(self, x, y):
        self.position.set(x, y)
        return self # this return is so it's possible to stack modifiers

    def getCenterX(self):
        return self.position.getX() + self.size.getX() / 2

    def getCenterY(self):
        return self.position.getY() + self.size.getY() / 2

    def setSize(self, x, y):
        self.size.set(x, y)
        return self # this return is so it's possible to stack modifiers

    def setShape(self, shape):
        self.shape = shape
        return self # this return is so it's possible to stack modifiers

    def setShapeFromName(self, shape_name):
        if shape_name in SHAPES:
            self.shape = SHAPES[shape_name]
        else:
            raise Exception("Please give a valid shape, list located in elements/Entity.py")
        return self # this return is so it's possible to stack modifiers

    def setWeight(self, weight):
        self.weight = weight
        return self # this return is so it's possible to stack modifiers

    def setColor(self, r, g, b):
        self.color.setFromRGB(r, g, b)
        return self # this return is so it's possible to stack modifiers

    def setAnchored(self, anchored):
        self.anchored = anchored
        if anchored:
            self.gravity = False
        return self # this return is so it's possible to stack modifiers

    def setGravity(self, gravity):
        if gravity:
            self.gravity = True
            self.anchored = False
        else:
            self.gravity = False
        return self # this return is so it's possible to stack modifiers

    def setGravityDirection(self, x, y):
        self.gravity_direction.set(x, y)
        return self # this return is so it's possible to stack modifiers

    def setBouncy(self, bouncy):
        self.bouncy = bouncy
        return self # this return is so it's possible to stack modifiers

    def hasGravity(self):
        return self.gravity

    def hasBounciness(self):
        return self.bouncy

    def setDeadly(self, deadly):
        self.Deadly = deadly
        return self

    def isDeadly(self):
        return self.Deadly

    def set_sprite_image(self, image_path):
        """Set a custom image for the entity sprite"""
        try:
            self.sprite_image = pygame.image.load(image_path).convert_alpha()
            self.sprite_name = image_path
            self.update_sprite()
        except pygame.error as e:
            print(f"Could not load image: {image_path}. Error: {e}")
        return self
    
    def set_sprite_from_image(self, image):
        """Set a custom image for the entity sprite"""
        try:
            self.sprite_image = image
            self.sprite_name = "visuals"
            self.update_sprite()
        except pygame.error as e:
            print(f"Could not load image: {image}. Error: {e}")
        return self

    def set_animation_frames(self, animation_path, amount, rotation):
        """Set a custom image for the entity sprite"""
        try:
            # Load all frames
            self.sprite_animation_sequence = []
            for sprite in range(amount):
                image = pygame.image.load(animation_path + "/frame" + str(sprite) + ".png").convert_alpha()
                image = pygame.transform.rotate(
                    image, rotation
                )
                self.sprite_animation_sequence.append(image)

            self.sprite_animation_frame = random.randint(0, len(self.sprite_animation_sequence) - 1)
            self.sprite_image = self.sprite_animation_sequence[self.sprite_animation_frame]
            self.sprite_name = animation_path
            self.update_sprite()
        except pygame.error as e:
            print(f"Could not load frame in: {animation_path}. Error: {e}")
        return self

    def update_animation(self):
        if self.sprite_animation_sequence == None: return
        self.sprite_animation_frame += 1
        if self.sprite_animation_frame == len(self.sprite_animation_sequence): self.sprite_animation_frame = 0
        self.sprite_image = self.sprite_animation_sequence[self.sprite_animation_frame]
        if self.gravity_direction.getY() < 0:
            self.sprite_offset = math.sin(self.sprite_animation_frame / 2) - 0.7 * TILESIZE
        else:
            self.sprite_offset = math.sin(self.sprite_animation_frame / 2)
        self.update_sprite_size(1.7)

    def update_sprite_size(self, size):
        if self.sprite_image:
            self.image = pygame.transform.scale(
                self.sprite_image,
                (int(self.size.getX() * TILESIZE * size), int(self.size.getY() * TILESIZE * size))
            )
        else:
            # Als fallback maken we een gekleurde rechthoek
            self.image = pygame.Surface((int(self.size.getX() * TILESIZE), int(self.size.getY() * TILESIZE)))

    def update_sprite(self):
        if self.sprite_image:
            size_x = int(self.size.getX() * TILESIZE)
            size_y = int(self.size.getY() * TILESIZE)
            if size_x < 0 or size_y < 0: return
            self.image = pygame.transform.scale(
                self.sprite_image,
                (size_x, size_y)
            )
        else:
            # Als fallback maken we een gekleurde rechthoek
            self.image = pygame.Surface((int(self.size.getX() * TILESIZE), int(self.size.getY() * TILESIZE)))

    def rotate_sprite(self, rotation):
        if self.sprite_image:
            self.image = pygame.transform.rotate(
                self.image, -self.rotation
            )
            self.image = pygame.transform.rotate(
                self.image, rotation
            )
            self.rotation = rotation

    def clone(self):
        cloned_entity = Entity(self.name, self.shape, [self.position.getX(), self.position.getY()])
        cloned_entity.setVelocity(self.velocity.getX(), self.velocity.getY())
        cloned_entity.setSize(self.size.getX(), self.size.getY())
        cloned_entity.setWeight(self.weight)
        cloned_entity.setColor(self.color.r, self.color.g, self.color.b)
        cloned_entity.setAnchored(self.anchored)
        cloned_entity.setGravity(self.gravity)
        cloned_entity.setGravityDirection(self.gravity_direction.getX(), self.gravity_direction.getY())
        cloned_entity.setBouncy(self.bouncy)
        return cloned_entity


class Player(Entity):
    def __init__(self, name, shape, position, physics_engine):
        super().__init__(name, shape, position)
        self.velocity = Vector2(0, 0)
        self.position = Vector2(position[0], position[1])
        self.starting_position = Vector2(position[0], position[1])
        self.physics_engine = physics_engine
        self.grounded = False
        self.alive = True
        self.score = loading_score()

    def setVelocity(self, x, y):
        super().setVelocity(x, y)
        return self

    def addVelocity(self, x, y):
        super().addVelocity(x, y)
        return self  # this return is so it's possible to stack modifiers

    def setPosition(self, x, y):
        super().setPosition(x, y)
        return self  # this return is so it's possible to stack modifiers

    def get_pos(self):
        return self.position

    def setGravity(self, gravity):
        super().setGravity(self)
        return self

    def setGravityDirection(self, x, y):
        super().setGravityDirection(x, y)
        return self # this return is so it's possible to stack modifiers

    def setBouncy(self, bouncy):
        self.bouncy = bouncy
        return self  # this return is so it's possible to stack modifiers

    def hasGravity(self):
        return self.gravity

    def hasBounciness(self):
        return self.bouncy

    def setColor(self, r, g, b):
        super().setColor(r, g, b)
        return self

    def death(self):
        """Trigger player death"""
        self.alive = False
        try:
            with open('deaths.txt', "r") as f:
                deaths = int(f.read())
                deaths = deaths + 1
                with open('deaths.txt', 'w') as fw:
                    fw.write(str(deaths))
        except:
            with open('deaths.txt', 'w') as fw:
                fw.write("1")


    def respawn(self):
        """Reset player to initial state"""
        print(f"[DEBUG] Respawning to start position: {self.starting_position.getX()}, {self.starting_position.getY()}")

        self.setPosition(self.starting_position.getX(), self.starting_position.getY())
        self.setVelocity(0, 0)
        self.setGravityDirection(0, -1)
        self.alive = True
        self.fatal_object_colliding_with = False
        self.rotate_sprite(0)
        return self

    def death_test(self):
        """Test function to trigger death with X key"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            self.death()
#DEAD
    def walk(self, speed):
        """
        Deze functie zorgt dat het eerste object van de elements loopt
        :param speed: Hiermee wordt de snelheid geregeld
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.setPosition(0, speed)
        if keys[pygame.K_a]:
            self.setPosition(-speed, 0)
        if keys[pygame.K_s]:
            self.setPosition(0, -speed)
        if keys[pygame.K_d]:
            self.setPosition(speed, 0)
        if keys[pygame.K_LSHIFT] and keys[pygame.K_a]:
            self.setPosition(-speed * 2, 0)
        if keys[pygame.K_LSHIFT] and keys[pygame.K_d]:
            self.setPosition(speed * 2, 0)

    def teleport(self):
        """
        Deze functie zorgt er voor dat het blokje geteleporteerd wordt.
        key waarde 1: x=0,y=5
        key waarde 2: x=5,y=0
        key waarde 3: x=0,y=-5
        key waarde 1: x=-5,y=0
        :return:
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.setPosition(0, 5)
        if keys[pygame.K_2]:
            self.setPosition(5, 0)
        if keys[pygame.K_3]:
            self.setPosition(0, -5)
        if keys[pygame.K_4]:
            self.setPosition(-5, 0)


class Portal(Entity):
    def __init__(self, name, shape, position, destination=(0, 0)):
        super().__init__(name, shape, position)
        self.destination = Vector2(destination[0], destination[1])
        self.sprite_image = self.set_sprite_image(portal_sprite)

    # determines where the player gets teleported to
    def setDestination(self, destination):
        self.destination = Vector2(destination[0], destination[1])

    # Finish klasse voor het eindpunt van de level
class FinishFlag(Entity):
    def __init__(self, name, shape, position):
        super().__init__(name, shape, position)
        self.sprite_image = self.set_sprite_image(finish_sprite_path)
        self.tag = "finish"

class FullFinishFlag(Entity):
    def __init__(self, name, shape, position):
        super().__init__(name, shape, position)
        self.sprite_image = self.set_sprite_image(finish_sprite_path)
        self.tag = "end"
        
class Enemy(Entity):
    def __init__(self, name, shape, position):
        super().__init__("Enemy", shape, position)
        self.moving_direction = [-1, 0]

class JumpEnemy(Entity):
    def __init__(self, name, shape, position):
        super().__init__("JumpEnemy", shape, position)
        self.moving_direction = [-1, 0]
        self.gravity = True

class Text(Entity):
    def __init__(self, name, shape, position, text):
        super().__init__("Text", shape, position)
        self.distance = 5
        self.text = text
        self.visible = True


class Tooltip(Entity):
    def __init__(self,name, text, pos, dist, font = comic_sans,shape=0, padding=5, line_spacing=5, bg_color=(50, 50, 50), border_color=(255, 255, 255)):
        super().__init__("Text", shape, pos)
        self.name = name
        self.dist = dist
        self.font = font
        self.pos = Vector2(pos[0], pos[0])
        self.padding = padding
        self.line_spacing = line_spacing
        self.bg_color = bg_color
        self.border_color = border_color
        self.text = text
        self.visible = False


    def show(self, pos):
        self.visible = True
        self.pos = pos

    def hide(self):
        self.visible = False

    def get_pos(self):
        return self.pos

    def draw(self, surface):
        if not self.visible or not self.text:
            return

        lines = self.text.split('\n')
        text_surfaces = [self.font.render(line, True, (255, 255, 255)) for line in lines]

        max_width = max(surf.get_width() for surf in text_surfaces)
        total_height = sum(surf.get_height() for surf in text_surfaces) + self.line_spacing * (len(lines) - 1)

        tooltip_rect = pygame.Rect(self.position[0] + 10, self.position[1] + 10,
                                   max_width + 2 * self.padding,
                                   total_height + 2 * self.padding)

        # Achtergrond en rand
        pygame.draw.rect(surface, self.bg_color, tooltip_rect)
        pygame.draw.rect(surface, self.border_color, tooltip_rect, 1)

        # Tekst tekenen
        y_offset = tooltip_rect.y + self.padding
        for surf in text_surfaces:
            surface.blit(surf, (tooltip_rect.x + self.padding, y_offset))
            y_offset += surf.get_height() + self.line_spacing

