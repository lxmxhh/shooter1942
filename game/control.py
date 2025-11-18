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
    def __init__(self):
        self._dx = 0
        self._dy = 0
        self._last_decide = 0
        self.margin = 70
        self.deadzone = 12
        self.decision_interval_ms = 60

    def update(self, player, game):
        now = pygame.time.get_ticks()
        if now - self._last_decide < self.decision_interval_ms:
            player.rect.x += self._dx
            player.rect.y += self._dy
            return

        dx = 0
        dy = 0
        danger = None
        min_d = 1e9
        for e in game.enemies:
            r = e.rect.inflate(self.margin, self.margin)
            if r.colliderect(player.rect):
                d = abs(player.rect.centerx - e.rect.centerx) + abs(player.rect.centery - e.rect.centery)
                if d < min_d:
                    min_d = d
                    danger = e
        if danger:
            diff_x = player.rect.centerx - danger.rect.centerx
            if abs(diff_x) < self.deadzone:
                dx = -player.speed if player.rect.centerx <= danger.rect.centerx else player.speed
            elif diff_x < 0:
                dx = -player.speed
            else:
                dx = player.speed

            if abs(diff_x) < 40:
                diff_y = player.rect.centery - danger.rect.centery
                if diff_y <= 0:
                    dy = -player.speed
                else:
                    dy = player.speed
        else:
            cx = player.rect.centerx
            mid = WIDTH // 2
            if cx < mid - self.deadzone:
                dx = player.speed
            elif cx > mid + self.deadzone:
                dx = -player.speed

        self._dx, self._dy = dx, dy
        self._last_decide = now
        player.rect.x += dx
        player.rect.y += dy