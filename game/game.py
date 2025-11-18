import pygame

from .settings import WIDTH, HEIGHT, FPS
from .entities import Player, Star
from .state import PlayingState


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("1942 Vertical Shooter")
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        for _ in range(120):
            s = Star()
            self.all_sprites.add(s)
            self.stars.add(s)

        self.player = Player()
        self.all_sprites.add(self.player)

        self.score = 0
        self.state = None
        self.change_state(PlayingState())

    def reset(self):
        self.all_sprites.empty()
        self.bullets.empty()
        self.enemies.empty()
        self.stars.empty()
        for _ in range(120):
            s = Star()
            self.all_sprites.add(s)
            self.stars.add(s)
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0

    def change_state(self, state):
        self.state = state
        if hasattr(self.state, "enter"):
            self.state.enter(self)

    def run(self):
        while True:
            now = pygame.time.get_ticks()
            for event in pygame.event.get():
                self.state.handle_event(self, event)
            self.state.update(self, now)
            self.state.draw(self)
            pygame.display.flip()
            self.clock.tick(FPS)