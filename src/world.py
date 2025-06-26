from src.elements.Entity import Entity, Player, Portal, TILESIZE, FinishFlag, FullFinishFlag, Enemy, JumpEnemy, Text, Tooltip
from src.utils.font import comic_sans
from src.bake import bake_textures
from src.elements.Button import Button

class World():
    def __init__(self, physics_engine, sound_engine):
        self.entities = []
        self.buttons = []
        self.stippen = []
        self.current_world = None
        self.physics_engine = physics_engine
        self.sound_engine = sound_engine
        self.editor = False

    def load_world(self, world):
        if world == "EDITOR":
            self.entities = [
                Entity("PlayerSpawn", 0, (0, 0)).setColor(255, 0, 0).set_sprite_image("src/sprites/player_test_sprite.png"),
                Player("Player", 0, (0, 0), self.physics_engine).setSize(0.1, 0.1).setColor(255, 255, 255)
            ]
            self.buttons = [
                Button(10, 10, "Add Ground")
            ]
            self.current_world = world
            self.editor = True
            return

        self.current_world = world

        world_data = ""
        with open("src/worlds/" + world) as f:
            world_data = f.read()
        world_data = world_data.replace("\n", "")

        player = None
        colliders = []
        visuals = []
        self.entities = []
        
        for item in world_data.split("@"):
            if item == "": continue
            item_attributes = item.split(":")
            if item_attributes[0] == "P":
                player = Player(
                    "Player", 0, (
                        float(item_attributes[1]), float(item_attributes[2])
                    ), self.physics_engine).setGravity(True).set_sprite_image("src/sprites/player_test_sprite.png"
                )
            elif item_attributes[0] == "G1":
                colliders.append(
                    Entity("GroundCollider", 0, (
                        float(item_attributes[1]) + 1, float(item_attributes[2]) + 1
                    )).setColor(255, 0, 0).setSize(
                        float(item_attributes[3]) * 5 - 2, float(item_attributes[4]) * 4 - 2
                    ).setTransparent(True)
                )
                visuals.append(
                    Entity("Ground", 0, (
                        float(item_attributes[1]), float(item_attributes[2])
                    )).setColor(255, 0, 0).setSize(
                        float(item_attributes[3]) * 5, float(item_attributes[4]) * 4
                    ).setCollide(False).set_sprite_image("src/sprites/ground_1.png")
                )
                if item_attributes[5] == "ED":
                    visuals.append(
                        Entity("Extends", 0, 
                            (float(item_attributes[1]) + 1, float(item_attributes[2]) + float(item_attributes[4]) * 2 - 100)
                        ).setColor(0, 0, 0).setSize(float(item_attributes[3]) * 5 - 2, 100).setCollide(False).set_sprite_image("src/sprites/blank.png")
                    )
                elif item_attributes[5] == "EU":
                    visuals.append(
                        Entity("Extends", 0, 
                            (float(item_attributes[1]) + 1, float(item_attributes[2]) + float(item_attributes[4]) * 2)
                        ).setColor(0, 0, 0).setSize(float(item_attributes[3]) * 5 - 2, 100).setCollide(False).set_sprite_image("src/sprites/blank.png")
                    )
            elif item_attributes[0] == "GW1":
                colliders.append(
                    Entity("GroundCollider", 0, (
                        float(item_attributes[1]) + 1, float(item_attributes[2]) + 1
                    )).setColor(255, 0, 0).setSize(
                        float(item_attributes[3]) * 10 - 2, float(item_attributes[4]) * 4 - 2
                    ).setTransparent(True)
                )
                visuals.append(
                    Entity("Ground", 0, (
                        float(item_attributes[1]), float(item_attributes[2])
                    )).setColor(255, 0, 0).setSize(
                        float(item_attributes[3]) * 10, float(item_attributes[4]) * 4
                    ).setCollide(False).set_sprite_image("src/sprites/ground_wide_1.png")
                )
                if item_attributes[5] == "ED":
                    visuals.append(
                        Entity("Extends", 0, 
                            (float(item_attributes[1]) + 1, float(item_attributes[2]) + float(item_attributes[4]) * 2 - 100)
                        ).setColor(0, 0, 0).setSize(float(item_attributes[3]) * 10 - 2, 100).setCollide(False).set_sprite_image("src/sprites/blank.png")
                    )
                elif item_attributes[5] == "EU":
                    visuals.append(
                        Entity("Extends", 0, 
                            (float(item_attributes[1]) + 1, float(item_attributes[2]) + float(item_attributes[4]) * 2)
                        ).setColor(0, 0, 0).setSize(float(item_attributes[3]) * 10 - 2, 100).setCollide(False).set_sprite_image("src/sprites/blank.png")
                    )
            elif item_attributes[0] == "GW1NC":
                visuals.append(
                    Entity("Ground", 0, (
                        float(item_attributes[1]), float(item_attributes[2])
                    )).setColor(255, 0, 0).setSize(
                        float(item_attributes[3]) * 10, float(item_attributes[4]) * 4
                    ).setCollide(False).set_sprite_image("src/sprites/ground_wide_1.png")
                )
                if item_attributes[5] == "ED":
                    visuals.append(
                        Entity("Extends", 0, 
                            (float(item_attributes[1]) + 1, float(item_attributes[2]) + float(item_attributes[4]) * 2 - 100)
                        ).setColor(0, 0, 0).setSize(float(item_attributes[3]) * 10 - 2, 100).setCollide(False).set_sprite_image("src/sprites/blank.png")
                    )
                elif item_attributes[5] == "EU":
                    visuals.append(
                        Entity("Extends", 0, 
                            (float(item_attributes[1]) + 1, float(item_attributes[2]) + float(item_attributes[4]) * 2)
                        ).setColor(0, 0, 0).setSize(float(item_attributes[3]) * 10 - 2, 100).setCollide(False).set_sprite_image("src/sprites/blank.png")
                    )
            elif item_attributes[0] == "T":
                colliders.append(
                    Portal("portal", 0, 
                        (float(item_attributes[1]), float(item_attributes[2])), 
                        (float(item_attributes[3]), float(item_attributes[4]))
                    ).setCollide(False)
                )
            elif item_attributes[0] == "F":
                colliders.append(
                    Entity("Fatal_Object", 0,
                           (float(item_attributes[1]), float(item_attributes[2]))
                    ).setSize(float(item_attributes[3]), float(item_attributes[4])).setColor(150, 10, 10).setDeadly(True).setCollide(False)
                )
            elif item_attributes[0] == "E":
                colliders.append(
                    FinishFlag("End", 0,
                           (float(item_attributes[1]), float(item_attributes[2]))
                    ).setCollide(False)
                )
            elif item_attributes[0] == "I":
                colliders.append(
                    FullFinishFlag("FullEnd", 0,
                           (float(item_attributes[1]), float(item_attributes[2]))
                    ).setCollide(False)
                )
            elif item_attributes[0] == "W": # temporary wall to test gravity controls
                colliders.append(
                    Entity("Wall", 0,
                           (float(item_attributes[1]), float(item_attributes[2]))
                    ).setSize(float(item_attributes[3]), float(item_attributes[4])).setColor(0, 0, 0)
                )
            elif item_attributes[0] == "A": # why is it A? E for enemy was already take, so a for AI
                enemy = Enemy("Enemy", 0,
                           (float(item_attributes[1]), float(item_attributes[2]))
                    ).setColor(255, 0, 0).setDeadly(True).setCollide(False).setGravity(True)
                if item_attributes[3] == "D":
                    enemy.setGravityDirection(0, -1)
                    enemy.set_animation_frames("src/sprites/wanderer", 35, 0)
                elif item_attributes[3] == "U":
                    enemy.setGravityDirection(0, 1)
                    enemy.set_animation_frames("src/sprites/wanderer", 35, 180)
                elif item_attributes[3] == "L":
                    enemy.setGravityDirection(-1, 0)
                    enemy.set_animation_frames("src/sprites/wanderer", 35, 90)
                elif item_attributes[3] == "R":
                    enemy.setGravityDirection(1, 0)
                    enemy.set_animation_frames("src/sprites/wanderer", 35, 270)
                colliders.append(enemy)
            elif item_attributes[0] == "B": # why is it B? A for AI was already taken, so it's B
                jump_enemy = JumpEnemy("JumpEnemy", 0, (float(item_attributes[1]), float(item_attributes[2]))).setColor(0, 255, 0).setDeadly(True).setCollide(False)
                jump_enemy.setGravity(True)
                if item_attributes[3] == "D":
                    jump_enemy.setGravityDirection(0, -1)
                    jump_enemy.set_animation_frames("src/sprites/wanderer", 35, 0)
                elif item_attributes[3] == "U":
                    jump_enemy.setGravityDirection(0, 1)
                    jump_enemy.set_animation_frames("src/sprites/wanderer", 35, 180)
                elif item_attributes[3] == "L":
                    jump_enemy.setGravityDirection(-1, 0)
                    jump_enemy.set_animation_frames("src/sprites/wanderer", 35, 90)
                elif item_attributes[3] == "R":
                    jump_enemy.setGravityDirection(1, 0)
                    jump_enemy.set_animation_frames("src/sprites/wanderer", 35, 270)
                colliders.append(jump_enemy)
            elif item_attributes[0] == "S": # why is it S? T for teleport was already take, so s for shout, this shouts some text to the screen ig
                if len(item_attributes) == 5:
                    colliders.append(
                        Tooltip("Tooltip", str(item_attributes[4]),
                            (float(item_attributes[1]), float(item_attributes[2])), float(item_attributes[3]),comic_sans
                        ).setCollide(False)
                    )
                else:
                    colliders.append(
                        Tooltip("Tooltip", str(item_attributes[3]),
                            (float(item_attributes[1]), float(item_attributes[2])), 5,comic_sans
                        ).setCollide(False)
                    )

        if player == None:
            print("[ERROR] NO PLAYER FOUND :C")
            return

        self.entities.extend(colliders)
        self.entities.append(player)
        
        visuals = bake_textures(visuals, world)
        self.entities.append(
            Entity("Visuals", 0, 
                (-62.5, -125)
            ).setColor(0, 0, 0).setSize(250, 250).setCollide(False).set_sprite_from_image(visuals)
        )

    def get_entity(self, name):
        for entity in self.entities:
            if entity.name == name:
                return entity
