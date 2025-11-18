import sys
import pygame

from .settings import WIDTH, HEIGHT, BLACK, WHITE, RED, GRAY
from .ui import draw_text
from .factory import Spawner
from .control import ManualController, AutoPilotController


class GameState:
    def enter(self, game):
        pass

    def handle_event(self, game, event):
        raise NotImplementedError

    def update(self, game, now):
        raise NotImplementedError

    def draw(self, game):
        raise NotImplementedError


class PlayingState(GameState):
    def enter(self, game):
        self.spawner = Spawner(game.all_sprites, game.enemies, delay=500)

    def handle_event(self, game, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                if isinstance(game.player.controller, ManualController):
                    game.player.controller = AutoPilotController()
                else:
                    game.player.controller = ManualController()

    def update(self, game, now):
        game.player.try_shoot(now, game.all_sprites, game.bullets)
        self.spawner.update(now)
        game.all_sprites.update(game)
        hits = pygame.sprite.groupcollide(game.enemies, game.bullets, True, True)
        game.score += len(hits) * 10
        if pygame.sprite.spritecollide(game.player, game.enemies, True):
            game.player.lives -= 1
            if game.player.lives <= 0:
                game.change_state(GameOverState())

    def draw(self, game):
        screen = game.screen
        screen.fill(BLACK)
        game.all_sprites.draw(screen)
        draw_text(screen, f"Score: {game.score}", 24, 70, 20, WHITE)
        draw_text(screen, f"Lives: {game.player.lives}", 24, WIDTH - 80, 20, WHITE)


class GameOverState(GameState):
    def handle_event(self, game, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game.reset()
                game.change_state(PlayingState())

    def update(self, game, now):
        game.all_sprites.update(game)

    def draw(self, game):
        screen = game.screen
        screen.fill(BLACK)
        game.all_sprites.draw(screen)
        draw_text(screen, "GAME OVER", 48, WIDTH // 2, HEIGHT // 2 - 20, RED)
        draw_text(screen, "Press Enter to Restart", 24, WIDTH // 2, HEIGHT // 2 + 30, GRAY)
        draw_text(screen, "Score: {}".format(game.score), 24, 70, 20, WHITE)
        draw_text(screen, "Lives: 0", 24, WIDTH - 80, 20, WHITE)