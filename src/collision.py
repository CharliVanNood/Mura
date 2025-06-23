import pygame

# ---------------------------------- Dead Code? ----------------------------------
class CollisionRect():
    all_objects = []

    def __init__(self, x, y, width, height, color="Black"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.can_move = True
        self.all_objects.append(self)

    def check_collision(self):
        for obj in CollisionRect.all_objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.can_move = False
                obj.can_move = False
                return False
            self.can_move = True
            obj.can_move = True
            return True

    # Handig voor enemies die enkel achter de speler aan rennen
    def move_towards(self, target, speed):
        if self.can_move:
            # calculate distance
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5

            # move
            self.rect.x += int((dx / distance) * speed)
            self.rect.y += int((dy / distance) * speed)
            return True
        return False


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Rectangles
rect1 = CollisionRect(640,350,50,50)
rect2 = CollisionRect(0, 350, 50, 50)