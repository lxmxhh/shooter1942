import pygame
from .settings import WIDTH, HEIGHT


class Controller:
    def update(self, player, game):
        raise NotImplementedError


class ManualController(Controller):
    def update(self, player, game):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player.speed
        player.rect.x += dx
        player.rect.y += dy


class AutoPilotController(Controller):
    def update(self, player, game):
        dx = 0
        dy = 0
        margin = 60
        danger = None
        min_d = 1e9
        for e in game.enemies:
            r = e.rect.inflate(margin, margin)
            if r.colliderect(player.rect):
                d = abs(player.rect.centerx - e.rect.centerx) + abs(player.rect.centery - e.rect.centery)
                if d < min_d:
                    min_d = d
                    danger = e
        if danger:
            if player.rect.centerx <= danger.rect.centerx:
                dx = -player.speed
            else:
                dx = player.speed
            if abs(player.rect.centerx - danger.rect.centerx) < 40:
                if player.rect.centery <= danger.rect.centery:
                    dy = -player.speed
                else:
                    dy = player.speed
        else:
            if player.rect.centerx < WIDTH // 2 - 5:
                dx = player.speed
            elif player.rect.centerx > WIDTH // 2 + 5:
                dx = -player.speed
        player.rect.x += dx
        player.rect.y += dy