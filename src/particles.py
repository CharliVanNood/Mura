import pygame
import random
import time
from src.utils.vectors import Vector2

class Particle:
    def __init__(self, position, color, lifetime=2.0):
        self.position = Vector2(position[0], position[1])
        self.color = color
        self.radius = random.uniform(1, 3)
        self.lifetime = lifetime
        self.creation_time = time.time()
        self.velocity = Vector2(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))

    def update(self):
        # Beweeg de particle en verlaag de lifetime
        self.velocity.add(0, 0.001)  # zwaartekracht
        self.position.addVector(self.velocity)
        return time.time() - self.creation_time < self.lifetime

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.position.getX()), int(self.position.getY())), self.radius)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def emit(self, position, color, count=20):
        for _ in range(count):
            self.particles.append(Particle(position, color, 1.5))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
