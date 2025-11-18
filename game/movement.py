import pygame
import random

class MovementStrategy:
    def update(self, sprite):
        raise NotImplementedError

class WobbleMovement(MovementStrategy):
    def __init__(self):
        self.phase = random.random() * 3.14

    def update(self, sprite):
        sprite.rect.y += sprite.speedy
        sprite.rect.x += int(2 * pygame.math.Vector2(1, 0).rotate_rad(self.phase).x)
        self.phase += 0.03