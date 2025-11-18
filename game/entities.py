import pygame
import random

from .settings import WIDTH, HEIGHT, WHITE, YELLOW, RED, GREEN, BLUE
from .movement import WobbleMovement
from .control import AutoPilotController


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, GREEN, [(18, 0), (0, 36), (36, 36)])
        pygame.draw.rect(self.image, BLUE, (14, 10, 8, 16))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 5
        self.shot_delay = 180
        self.last_shot = 0
        self.lives = 3
        self.controller = AutoPilotController()

    def update(self, game=None):
        if self.controller:
            self.controller.update(self, game)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def try_shoot(self, now, all_group, bullet_group):
        if now - self.last_shot >= self.shot_delay:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_group.add(bullet)
            bullet_group.add(bullet)
            self.last_shot = now


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self, game=None):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, movement=None):
        super().__init__()
        size = random.randint(26, 34)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 0, size, size), border_radius=6)
        pygame.draw.rect(self.image, WHITE, (size // 3, size // 3, size // 3, size // 3))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speedy = random.randint(2, 4)
        self.speedx = random.choice([-1, 0, 1]) * random.randint(0, 2)
        self.movement = movement or WobbleMovement()

    def update(self, game=None):
        self.movement.update(self)
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speedx = -self.speedx
            self.rect.x += self.speedx
        if self.rect.top > HEIGHT:
            self.kill()


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(1, 3)
        self.image = pygame.Surface((size, size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.speedy = random.randint(1, 3)

    def update(self, game=None):
        self.rect.y += self.speedy
        if self.rect.top >= HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, WIDTH)
            self.speedy = random.randint(1, 3)