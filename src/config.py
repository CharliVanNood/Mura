from src.elements.Entity import Entity, Player, Portal, TILESIZE, FinishFlag, FullFinishFlag, Enemy, JumpEnemy, Text, Tooltip
from src.utils.font import comic_sans
from src.bake import bake_textures

WALKING_SPEED = 0.1
TELEPORT_COOLDOWN = 2
CURRENT_MAP = "intro" # default value, gets overwritten in startscherm.py

def setMap(newMap):
    CURRENT_MAP = newMap

class World():
    def __init__(self, physics_engine, sound_engine):
        self.entities = []
        self.buttons = []
        self.stippen = []
        self.current_world = None
        self.physics_engine = physics_engine
        self.sound_engine = sound_engine

    def load_world(self, world):
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
        #self.entities.extend(visuals)
        
        visuals = bake_textures(visuals, world)
        self.entities.append(
            Entity("Visuals", 0, 
                (-62.5, -125)
            ).setColor(0, 0, 0).setSize(250, 250).setCollide(False).set_sprite_from_image(visuals)
        )
        
    # Shapes: (I put these as integers as that's more memory efficient, I hope python thinks the same)
    # 0 - rectangle
    # 1 - circle
    # ---------------------------------- Dead Code? ----------------------------------
    def init_world(self):
        print("[DEBUG] Creating world")
        self.entities =  [
            Entity("Ground", 0, (1, -1)).setColor(255, 0, 0).setSize(3, 2).setTransparent(True),
            Entity("Ground", 0, (3, -2)).setColor(255, 0, 0).setSize(8, 2).setTransparent(True),
            Entity("Ground", 0, (9, -2.5)).setColor(255, 0, 0).setSize(8, 2).setTransparent(True),
            Entity("Ground", 0, (19, -4)).setColor(255, 0, 0).setSize(8, 2).setTransparent(True),
            Entity("Ground", 0, (22, -5)).setColor(255, 0, 0).setSize(10, 10).setCollide(False).set_sprite_image("src/sprites/house_3.png"),
            Entity("Ground", 0, (23.5, -1)).setColor(255, 0, 0).setSize(7.5, 1).setTransparent(True),
            Entity("Ground", 0, (25, -22.5)).setColor(0, 0, 0).setSize(3, 20).setTransparent(True),
            Entity("Ground", 0, (27, -22)).setColor(0, 0, 0).setSize(3, 20).setTransparent(True),
            Entity("Ground", 0, (30, -21.5)).setColor(0, 0, 0).setSize(3, 20).setTransparent(True),

            Entity("Ground", 0, (-5, -5)).setColor(255, 255, 255).setSize(20, 1),
            Entity("Ground", 0, (5, -4)).setColor(255, 255, 255).setSize(2, 1.5),
            Entity("Fatal_Object", 0, (7, 7),).setColor(150, 10, 10).setDeadly(True),
            # Tooltip("to jump press SPACE")
            # Tooltip("hold shift to run")
            # Tooltip("use run and jump together to jump further")
            Entity("Ground", 0, (18, -5)).setColor(255, 255, 255).setSize(20, 1),
            Entity("Ground", 0, (45, -5)).setColor(255, 255, 255).setSize(10, 1),
            Entity("Ground", 0, (55, -5)).setColor(255, 255, 255).setSize(1, 20),
            # Tooltip("use the right arrow key to change the gravity in that direction")
            Entity("Ground", 0, (55, 15)).setColor(255, 255, 255).setSize(10, 1),
            # Tooltip("use the downwards arrow key to change the gravity back")
            Portal("portal", 0, (60, 16), (160, 25)).setColor(100, 0, 100),
            Portal("portal", 0, (160, 25), (60, 16)).setColor(100, 0, 100),
            # Tooltip("portals can take you directly to other places
            Entity("Ground", 0, (155, 24)).setColor(255, 255, 255).setSize(10, 1),
            Entity("Ground", 0, (165, 24)).setColor(255, 255, 255).setSize(1, 8),
            Entity("Ground", 0, (165, 35)).setColor(255, 255, 255).setSize(1, 15),
            # Tooltip("you can also jump while walking on a wall")
            Portal("portal", 0, (163, 45), (200, 200)).setColor(100, 0, 100),
            Entity("Ground", 0, (155, 49)).setColor(255, 255, 255).setSize(10, 1),
            Entity("Ground", 0, (150, 199)).setColor(255, 255, 255).setSize(60, 1),
            Entity("Ground", 0, (210, 199)).setColor(255, 255, 255).setSize(1, 11),
            Entity("Ground", 0, (150, 209)).setColor(255, 255, 255).setSize(60, 1),
            Entity("Ground", 0, (150, 199)).setColor(255, 255, 255).setSize(1, 10),
            Entity("Ground", 0, (190, 199)).setColor(255, 255, 255).setSize(10, 1),
            Entity("Moving_box", 0, (185, 202)).setColor(255, 255, 255).setSize(1, 1).setGravity(True).setGravityDirection(0, -1),
            # Tooltip("You can move certain object by pushing them")
            Portal("portal", 0, (160, 200), (300, 300)).setColor(100, 0, 100),
            Entity("Ground", 0, (290, 299)).setColor(255, 255, 255).setSize(20, 1),
            Entity("Ground", 0, (310, 299)).setColor(255, 255, 255).setSize(1, 10),
            Entity("Ground", 0, (290, 299)).setColor(255, 255, 255).setSize(1, 10),
            Entity("Ground", 0, (290, 309)).setColor(255, 255, 255).setSize(21, 1),


            #walls V
            Entity("Ground", 0, (-5, -5)).setColor(255, 255, 255).setSize(1, 15),
            Entity("Ground", 0, (-5, 10)).setColor(255, 255, 255).setSize(50, 1),
            Entity("Ground", 0, (45, 10)).setColor(255, 255, 255).setSize(1, 15),
            Entity("Ground", 0, (45, 25)).setColor(255, 255, 255).setSize(20, 1),
            Entity("Ground", 0, (65, 15)).setColor(255, 255, 255).setSize(1, 11),
            Entity("Ground", 0, (155, 24)).setColor(255, 255, 255).setSize(1, 25),

            # Entity("gravity_walk_test", 0, (7, 0)).setColor(100, 0, 200).setGravity(True),
            # Entity("test1", 0, (2, 0)).setColor(100, 0, 200).setGravity(True),
            # Entity("test2", 0, (2, 2)).setColor(100, 0, 200).setGravity(True).setVelocity(0, 0),
            # Entity("testBlock1WHATTTTT", 0, (2, 0)).setColor(0, 0, 127),
            # Entity("testBlock2", 0, (4, 2)).setColor(0, 0, 127),
            # Entity("testBlock3", 0, (4, 3)).setColor(0, 0, 127),
            # Entity("test3", 0, (0, 3)).setColor(200, 100, 0).setVelocity(0, 0.15).setGravity(True).setBouncy(True).setGravityDirection(1, 0),
            # Entity("test4", 0, (0, 6)).setColor(200, 100, 0).setGravity(True).setGravityDirection(-1, 0),
            # Entity("CollidingAA2", 0, (-3, 2)).setColor(255, 255, 255).setGravity(True),
            # Portal("portal", 0, (2, 4), (-2, -4)).setColor(0, 128, 0),
            # Portal("portal", 0, (-2, -4), (2, 4)).setColor(0, 200, 0),
            # Player("Player", 0, (0, -5), self.physics_engine).setColor(0, 255, 0).setGravity(True), # make sure player is drawn on top of portals
            #
            # Entity("Ground", 0, (-5, -5)).setColor(255, 255, 255).setSize(10, 1),
            # Entity("Ground", 0, (-5, -5)).setColor(255, 255, 255).setSize(1, 4),
            # Entity("Ground", 0, (-8, -2)).setColor(255, 255, 255).setSize(4, 1),
            # Entity("Ground", 0, (-8.5, -2)).setColor(255, 255, 255).setSize(1, 8),
            # Entity("Ground", 0, (5, -5)).setColor(255, 255, 255).setSize(1, 3),
            # Entity("Ground", 0, (6, -3)).setColor(255, 255, 255).setSize(4, 1),
            # Entity("Ground", 0, (7.5, -2)).setColor(255, 255, 255).setSize(1, 8),

            Player("Player", 0, (2, 1), self.physics_engine).setColor(0, 255, 0).setGravity(True).set_sprite_image("src/sprites/player_test_sprite.png"), # NOTE: Player object needs to be last so objects can be pushed

            Entity("Ground", 0, (0, -2)).setColor(255, 0, 0).setSize(5, 4).setCollide(False).set_sprite_image("src/sprites/ground_1.png"),
            Entity("Ground", 0, (1, -20)).setColor(0, 0, 0).setSize(3, 20).setCollide(False),
            Entity("Ground", 0, (2, -3)).setColor(255, 0, 0).setSize(10, 4).setCollide(False).set_sprite_image("src/sprites/ground_wide_1.png"),
            Entity("Ground", 0, (3, -21)).setColor(0, 0, 0).setSize(8, 20).setCollide(False),
            Entity("Ground", 0, (8, -3.5)).setColor(255, 0, 0).setSize(10, 4).setCollide(False).set_sprite_image("src/sprites/ground_wide_1.png"),
            Entity("Ground", 0, (9, -22)).setColor(0, 0, 0).setSize(8, 20).setCollide(False),
            Entity("Ground", 0, (18, -5)).setColor(255, 0, 0).setSize(10, 4).setCollide(False).set_sprite_image("src/sprites/ground_wide_1.png"),
            Entity("Ground", 0, (19, -23)).setColor(0, 0, 0).setSize(8, 20).setCollide(False),
            Entity("Ground", 0, (24, -4.5)).setColor(255, 0, 0).setSize(5, 4).setCollide(False).set_sprite_image("src/sprites/ground_1.png"),
            Entity("Ground", 0, (25, -22.5)).setColor(0, 0, 0).setSize(3, 20).setCollide(False),
            Entity("Ground", 0, (26, -4)).setColor(255, 0, 0).setSize(5, 4).setCollide(False).set_sprite_image("src/sprites/ground_1.png"),
            Entity("Ground", 0, (27, -22)).setColor(0, 0, 0).setSize(3, 20).setCollide(False),
            Entity("Ground", 0, (29, -3.5)).setColor(255, 0, 0).setSize(5, 4).setCollide(False).set_sprite_image("src/sprites/ground_1.png"),
            Entity("Ground", 0, (30, -21.5)).setColor(0, 0, 0).setSize(3, 20).setCollide(False),
            FinishFlag("FinishFlag", 0, (5, 1)).setColor(100, 0, 100), # Positie finis-vlag is nader te bepalen
        ]

    # ---------------------------------- Dead Code? ----------------------------------
    def init_buttons(self):
        self.buttons = []

    def get_entity(self, name):
        for entity in self.entities:
            if entity.name == name:
                return entity
