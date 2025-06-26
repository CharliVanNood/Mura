import pygame
import os
from src.config import TELEPORT_COOLDOWN
from src.world import World
from src.fps import get_time_delta
from src.elements.Entity import Player, Entity
from src.startscherm import startScreen
import math

class PhysicsEngine:
    def __init__(self, sound_engine):
        self.world = World(self, sound_engine)
        self.level_finished = False
        self.finish_time = None
        self.player = self.world.get_entity("Player")
        self.deltatime = 1
        self.sound_engine = sound_engine

    def update(self, deltatime):
        self.deltatime = deltatime
        for entity in self.world.entities:
            if entity.anchored:
                continue
            if not entity.collide and not entity.name == "JumpEnemy":
                continue
            
            if entity.shape == 0:
                list_colliding_with = self.getCollisionsAA(entity, self.world.entities)
            else:
                list_colliding_with = self.getCollisionsAA(entity, self.world.entities)
                colliding_with = self.getCollisionsBB(entity, self.world.entities)

            for other in list_colliding_with:
                if hasattr(other, "tag") and other.tag == "finish":
                    SELECTED_MAP = self.world.current_world
                    levels  = os.listdir("src/worlds")
                    for level in levels:
                        if not level.startswith("level"):
                            continue
                        if level == self.world.current_world:
                            if levels.index(level) + 1 <= len(levels) - 1:
                                SELECTED_MAP = levels[levels.index(level) + 1]
                                if SELECTED_MAP == "smiley":
                                    self.sound_engine.stop_music()
                                    self.sound_engine.play_music("music/eclipse.mp3")
                                break
                    self.world.load_world(SELECTED_MAP)
                    self.player = self.world.get_entity("Player")
                    self.level_finished = True
                if hasattr(other, "tag") and other.tag == "end":
                    SELECTED_MAP = startScreen(self.sound_engine)
                    self.sound_engine.play_music("music/play_loop.wav", loops=-1)
                    self.world.load_world(SELECTED_MAP)
                    self.player = self.world.get_entity("Player")


            #check if entity is affected by gravity
            if len(list_colliding_with) == 0 and entity.hasGravity():
                # add the direction of gravity, this is times 0.01 else it would be accelerating too fast
                gravity_x = entity.gravity_direction.getX() * deltatime * 0.01
                gravity_y = entity.gravity_direction.getY() * deltatime * 0.01
                entity.addVelocity(gravity_x, gravity_y)
            else:
                colliding_full = False
                for colliding_with in list_colliding_with:
                    if colliding_with.collide:
                        colliding_full = True
                        break
                if not colliding_full:
                    gravity_x = entity.gravity_direction.getX() * deltatime * 0.01
                    gravity_y = entity.gravity_direction.getY() * deltatime * 0.01
                    entity.addVelocity(gravity_x, gravity_y)

            for colliding_with in list_colliding_with:
                # updates entities that are colliding with a portal
                if colliding_with.name == "portal":
                    entity.portal_colliding_with = colliding_with
                if colliding_with.name == "Fatal_Object" or colliding_with.name == "Enemy" or colliding_with.name == "JumpEnemy":
                    entity.fatal_object_colliding_with = colliding_with

                if not colliding_with.collide: continue

                if entity.position.getY() > colliding_with.position.getY() and entity.gravity_direction.getY() < 0:
                    entity.grounded = True
                elif entity.position.getY() < colliding_with.position.getY() and entity.gravity_direction.getY() > 0:
                    entity.grounded = True
                if entity.position.getX() > colliding_with.position.getX() and entity.gravity_direction.getX() < 0:
                    entity.grounded = True
                elif entity.position.getX() < colliding_with.position.getX() and entity.gravity_direction.getX() > 0:
                    entity.grounded = True

                if entity.hasBounciness():
                    # apply the bounce, which is the inverse of the current velocity with some loss of force
                    if entity.position.getY() > colliding_with.position.getY():
                        entity.velocity.setY(-entity.velocity.getY() * 0.8)
                else:
                    if entity.gravity_direction.getY() < 0:
                        # if the object is above another object stop moving
                        if entity.position.getY() > colliding_with.position.getY() and entity.gravity_direction.getY() != 0:
                            entity.velocity.setY(0)
                        if entity.position.getX() > colliding_with.position.getX() and entity.gravity_direction.getX() != 0:
                            entity.velocity.setX(0)

                        # if moving up while under a different object, bounce off
                        if entity.position.getY() < colliding_with.position.getY() and entity.velocity.getY() > 0:
                            entity.velocity.setY(-entity.velocity.getY())
                    elif entity.gravity_direction.getY() > 0:
                        # if the object is above another object stop moving
                        if entity.position.getY() < colliding_with.position.getY() and entity.gravity_direction.getY() != 0:
                            entity.velocity.setY(0)
                        if entity.position.getX() > colliding_with.position.getX() and entity.gravity_direction.getX() != 0:
                            entity.velocity.setX(0)

                        # if moving up while under a different object, bounce off
                        if entity.position.getY() > colliding_with.position.getY() and entity.velocity.getY() < 0:
                            entity.velocity.setY(-entity.velocity.getY())
                    elif entity.gravity_direction.getX() < 0:
                        # if the object is above another object stop moving
                        if entity.position.getY() > colliding_with.position.getY() and entity.gravity_direction.getY() != 0:
                            entity.velocity.setY(0)
                        if entity.position.getX() > colliding_with.position.getX() and entity.gravity_direction.getX() != 0:
                            entity.velocity.setX(0)

                        # if moving up while under a different object, bounce off
                        if entity.position.getX() < colliding_with.position.getX() and entity.velocity.getX() > 0:
                            entity.velocity.setX(-entity.velocity.getX())
                    elif entity.gravity_direction.getX() > 0:
                        # if the object is above another object stop moving
                        if entity.position.getY() < colliding_with.position.getY() and entity.gravity_direction.getY() != 0:
                            entity.velocity.setY(0)
                        if entity.position.getX() > colliding_with.position.getX() and entity.gravity_direction.getX() != 0:
                            entity.velocity.setX(0)

                        # if moving up while under a different object, bounce off
                        if entity.position.getX() > colliding_with.position.getX() and entity.velocity.getX() < 0:
                            entity.velocity.setX(-entity.velocity.getX())
                
                # get the distance between the interracting items
                intersection_distance = self.distance(
                    entity, colliding_with
                )
                intersection_distance_x = self.getIntersectionX(entity, colliding_with)
                intersection_distance_y = self.getIntersectionY(entity, colliding_with)

                # make sure items aren't inside of eachother, else move them out (for circles)
                if entity.shape == 1:
                    # this code checks if the circles colliding are intersecting based on the size and position
                    # if the position plus the actual size divided by 2 is intersecting,
                    # get the position of the intersection and move there
                    # this way you will never have intersecting items unless the object is positioned after this check
                    # unlike the rectangles it takes the distance between the two objects and just gets the multiplier between the differences
                    # this means that it will just push them away in the direction relative to eachother
                    if intersection_distance < entity.size.getX() / 2 + colliding_with.size.getX() / 2:
                        new_distance_multiplier = 1 / intersection_distance

                        subtracted_vectors = entity.clone().position.subtractVector(colliding_with.position)

                        entity.position.add(
                            (subtracted_vectors.getY() - subtracted_vectors.getY() / new_distance_multiplier),
                            (subtracted_vectors.getX() - subtracted_vectors.getX() / new_distance_multiplier)
                        )

                        # if this prints, it might indicate some items are glitching through eachother
                        if intersection_distance < (entity.size.getX() / 2 + colliding_with.size.getX() / 2) * 0.9:
                            print(f"potential bug, intersecting by {intersection_distance}")
                else:
                    if entity.name == "JumpEnemy" and (colliding_with.name == "Player" or colliding_with.name == "Portal"):
                        continue

                    # this code checks if the rectangles colliding are intersecting based on the size and position
                    # if the position plus the actual size divided by 2 is intersecting,
                    # get the position of the intersection and move there
                    # this way you will never have intersecting items unless the object is positioned after this check
                    change_x = intersection_distance_x - (entity.size.getX() / 2 + colliding_with.size.getX() / 2)
                    change_y = intersection_distance_y - (entity.size.getY() / 2 + colliding_with.size.getY() / 2)

                    if change_x > change_y and entity.position.getX() >= colliding_with.position.getX():
                        entity.position.add(
                            -change_x,
                            0
                        )
                    elif change_x > change_y:
                        entity.position.add(
                            change_x,
                            0
                        )

                    if change_x < change_y and entity.position.getY() >= colliding_with.position.getY():
                        entity.position.add(
                            0,
                            -change_y
                        )
                    elif change_x < change_y:
                        entity.position.add(
                            0,
                            change_y
                        )
            
            # add the velocity to position
            entity.position.addVector(entity.velocity)

            # some slight air resistance, makes sure entities stop moving over time, this is more when dragging along something
            if len(list_colliding_with) > 0:
                colliding_full = False
                for colliding_with in list_colliding_with:
                    if colliding_with.collide:
                        colliding_full = True
                        break
                if not colliding_full:
                    gravity_x = entity.gravity_direction.getX() * 0.01 * deltatime
                    gravity_y = entity.gravity_direction.getY() * 0.01 * deltatime
                    entity.addVelocity(gravity_x, gravity_y)

                if colliding_full:
                    entity.velocity.multiply(0.75, 0.75)
                else:
                    entity.velocity.multiply(0.975, 0.975)
            else:
                entity.velocity.multiply(0.975, 0.975)

    def toggle_tooltips(self):
        for entity in self.world.entities:
            player = self.world.get_entity("Player")
            if entity.name == "Tooltip":
                tooltip = entity
                dx = player.position.getX() - (tooltip.position.getX() + 4)
                dy = player.position.getY() - tooltip.position.getY()
                distance = math.hypot(dx, dy)

                if distance < tooltip.dist:
                    tooltip.show(tooltip.pos)
                else:
                    tooltip.hide()
    # checks if, and teleports entities that are colliding with a portal
    def check_teleport(self):
        for entity in self.world.entities:
            if entity.portal_colliding_with:
                if entity.teleport_cooldown <= 0:
                    entity.setPosition(entity.portal_colliding_with.destination.x, entity.portal_colliding_with.destination.y)
                    entity.grounded = False     # make sure the player can't jump when teleported to mid-air
                    entity.teleport_cooldown = TELEPORT_COOLDOWN    # set a 3 second teleport cooldown
            entity.portal_colliding_with = None
            entity.teleport_cooldown -= get_time_delta()

    def check_death(self):
        for entity in self.world.entities:
            if entity.fatal_object_colliding_with and entity.name == "Player":
                Player.death(entity)
    
    def update_enemy_positions(self):
        for entity in self.world.entities:
            if entity.name == "Enemy" or entity.name == "JumpEnemy":
                # check if the entity is standing on something, if not return
                # create a temporary object to check if it collides with something
                if entity.gravity_direction.getY() < 0:
                    tempEntity = Entity("Enemy", 0, (
                            entity.position.getX() + 0.5, entity.position.getY() - 0.1 - 0.5
                        )).setSize(0.1, 0.1).setColor(255, 0, 0)
                else:
                    tempEntity = Entity("Enemy", 0, (
                            entity.position.getX() + 0.5, entity.position.getY() - 0.1 + 1.5
                        )).setSize(0.1, 0.1).setColor(255, 0, 0)

                entity.update_animation()

                if entity.name == "JumpEnemy":
                    if entity.grounded:
                        entity.jump_cooldown = True

                    if not self.is_clipping(tempEntity) and entity.jump_cooldown:
                        #entity.moving_direction[0] = -entity.moving_direction[0]
                        entity.addVelocity(0, 0.3)
                        entity.setPosition(entity.position.getX(), entity.position.getY() + 0.1)
                        entity.jump_cooldown = False
                        entity.grounded = False
                    elif self.is_clipping(tempEntity):
                        entity.jump_cooldown = True
                elif not self.is_clipping(tempEntity):
                    entity.moving_direction[0] = -entity.moving_direction[0]
                    entity.position.add(0.1 * self.deltatime * entity.moving_direction[0], 0)

                # check if the entity can move right
                if entity.moving_direction[0] > 0:
                    # create a temporary object to check if it collides with something
                    tempEntity = Entity("Enemy", 0, (
                            entity.position.getX() - 0.1 + 1.5, entity.position.getY() + 0.5
                        )).setSize(0.1, 0.1).setColor(255, 0, 0)
                    if not self.is_clipping(tempEntity):
                        entity.position.add(0.1 * self.deltatime, 0)
                    else:
                        entity.moving_direction[0] = -entity.moving_direction[0]
                
                # check if the entity can move left
                elif entity.moving_direction[0] < 0:
                    # create a temporary object to check if it collides with something
                    tempEntity = Entity("Enemy", 0, (
                        entity.position.getX() - 0.1 - 0.25, entity.position.getY() + 0.5
                    )).setSize(0.1, 0.1).setColor(255, 0, 0)
                    if not self.is_clipping(tempEntity):
                        entity.position.add(-0.1 * self.deltatime, 0)
                    else:
                        entity.moving_direction[0] = -entity.moving_direction[0]



    def clamp(self, value, min, max):
        if value > max: return max
        if value < min: return min
        return value
    
    def distance(self, entity_1, entity_2):
        # first subtract the vectors to get the difference between them
        subtracted_vectors = entity_1.clone().position.subtractVector(entity_2.position)

        # now take the magnitude also known as size of a vector, in this case the size of the difference
        return subtracted_vectors.magnitude()

    def getCollisionsBB(self, entity, entities):
        colliding_with = []

        for entity_checking in entities:
            distance = self.distance(entity, entity_checking)

            # there's a check to see if it's 0, when it is, it means it's the same object, else it'd likely never be 0, and rather 0.00001
            if distance < entity.size.getX() / 2 + entity_checking.size.getX() / 2 and not distance == 0:
                colliding_with.append(entity_checking)

        return colliding_with

    def getIntersectionX(self, entity, entity_checking):
        return abs(entity.getCenterX() - entity_checking.getCenterX())

    def getIntersectionY(self, entity, entity_checking):
        return abs(entity.getCenterY() - entity_checking.getCenterY())
    
    def getCollisionsAA(self, entity, entities):
        colliding_with = []

        for entity_checking in entities:
            if self.getIntersectionX(entity, entity_checking) < (entity.size.getX() / 2 + entity_checking.size.getX() / 2) and \
                self.getIntersectionY(entity, entity_checking) < (entity.size.getY() / 2 + entity_checking.size.getY() / 2) and \
                not self.distance(entity, entity_checking) == 0:
                colliding_with.append(entity_checking)
        
        return colliding_with
        

    def walk(self, player, speed):
        """
        Deze functie zorgt dat het eerste object van de elements loopt
        :param speed: Hiermee wordt de snelheid geregeld
        """

        keys = pygame.key.get_pressed()
        #if keys[pygame.K_w]:
        #    tempEntity = Entity("Player", 0, (
        #                player.position.getX() + 0.5, player.position.getY() + speed + 1.5
        #            )).setSize(0.1, 0.1).setColor(255, 0, 0)
        #    if not self.is_clipping(tempEntity): player.position.add(0, speed)

        if keys[pygame.K_a]:
            tempEntity = Entity("Player", 0, (
                        player.position.getX() - speed - 0.25, player.position.getY() + 0.5
                    )).setSize(0.1, 0.1).setColor(255, 0, 0)
            if not self.is_clipping(tempEntity):  player.position.add(-speed, 0)

        #if keys[pygame.K_s]:
        #    tempEntity = Entity("Player", 0, (
        #                player.position.getX() + 0.5, player.position.getY() - speed - 0.5
        #            )).setSize(0.1, 0.1).setColor(255, 0, 0)
        #    if not self.is_clipping(tempEntity): player.position.add(0, -speed)

        if keys[pygame.K_d]:
            tempEntity = Entity("Player", 0, (
                        player.position.getX() - speed + 1.5, player.position.getY() + 0.5
                    )).setSize(0.1, 0.1).setColor(255, 0, 0)
            if not self.is_clipping(tempEntity): player.position.add(speed, 0)

        #if keys[pygame.K_LSHIFT] and keys[pygame.K_w]:
        #    tempEntity = Entity("Player", 0, (
        #                player.position.getX() + 0.5, player.position.getY() + speed * 1.2 + 1.5
        #            )).setSize(0.1, 0.1).setColor(255, 0, 0)
        #    if not self.is_clipping(tempEntity): player.position.add(0, speed * 1.2)

        if keys[pygame.K_LSHIFT] and keys[pygame.K_a]:
            tempEntity = Entity("Player", 0, (
                        player.position.getX() - speed * 1.2 - 0.25, player.position.getY() + 0.5
                    )).setSize(0.1, 0.1).setColor(255, 0, 0)
            if not self.is_clipping(tempEntity):  player.position.add(-speed * 1.2, 0)

        #if keys[pygame.K_LSHIFT] and keys[pygame.K_s]:
        #    tempEntity = Entity("Player", 0, (
        #                player.position.getX() + 0.5, player.position.getY() - speed * 1.2 - 0.5
        #            )).setSize(0.1, 0.1).setColor(255, 0, 0)
        #    if not self.is_clipping(tempEntity): player.position.add(0, -speed * 1.2)

        if keys[pygame.K_LSHIFT] and keys[pygame.K_d]:
            tempEntity = Entity("Player", 0, (
                        player.position.getX() - speed * 1.2 + 1.5, player.position.getY() + 0.5
                    )).setSize(0.1, 0.1).setColor(255, 0, 0)
            if not self.is_clipping(tempEntity): player.position.add(speed * 1.2, 0)

    def is_clipping(self, entity):
        list_colliding_with = self.getCollisionsAA(entity, self.world.entities)
        colliding_full = False
        for colliding_with in list_colliding_with:
            if colliding_with.collide and colliding_with != self.player:
                colliding_full = True
                break
        if not colliding_full:
            return False
        return True

    @staticmethod
    def change_gravity(entity):
        """
        Deze functie controleert welke pijltjestoets is ingedrukt en geeft de bijbehorende richting terug
        :return: De richting van de zwaartekracht ("Left", "Right", "Up", "Down" of None)
        """
        keys = pygame.key.get_pressed()
        if entity.grounded:
            entity.grounded = False
            # Removed because of level design
            # if keys[pygame.K_LEFT]:
            #     entity.setGravityDirection(-1,0)
            # if keys[pygame.K_RIGHT]:
            #     entity.setGravityDirection(1,0)
            if keys[pygame.K_UP]:
                entity.setGravityDirection(0,1)
                entity.rotate_sprite(180)
            if keys[pygame.K_DOWN]:
                entity.setGravityDirection(0,-1)
                entity.rotate_sprite(0)

    # ---------------------------------- Dead Code? ----------------------------------
    def teleport(self, entity):
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
            entity.setPosition(0, 5)
        if keys[pygame.K_2]:
            entity.setPosition(5, 0)
        if keys[pygame.K_3]:
            entity.setPosition(0, -5)
        if keys[pygame.K_4]:
            entity.setPosition(-5, 0)

    def jump(self, entity, sound_engine):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            #colliding_object = self.getCollisionsAA(entity, self.world.entities)
            if entity.grounded:
                entity.grounded = False
                entity.addVelocity(
                    -entity.gravity_direction.getX() * 0.284,
                    -entity.gravity_direction.getY() * 0.284
                )
                entity.setPosition(
                    entity.position.getX() + -entity.gravity_direction.getX() * 0.1,
                    entity.position.getY() + -entity.gravity_direction.getY() * 0.1
                )
                sound_engine.playSound("effects/jump1.wav", 1)
