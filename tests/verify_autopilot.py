import pygame
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from game.control import AutoPilotController


class FakePlayer:
    def __init__(self, x, y, speed=5):
        self.rect = pygame.Rect(0, 0, 36, 36)
        self.rect.center = (x, y)
        self.speed = speed


class FakeEnemy:
    def __init__(self, x, y, w=30, h=30):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)


class FakeGame:
    def __init__(self, enemies):
        self.enemies = enemies


def assert_move(dx_expected=None, dy_expected=None, before=None, after=None):
    dx = after[0] - before[0]
    dy = after[1] - before[1]
    if dx_expected is not None and dx != dx_expected:
        raise AssertionError(f"dx {dx} != {dx_expected}")
    if dy_expected is not None and dy != dy_expected:
        raise AssertionError(f"dy {dy} != {dy_expected}")


def test_danger_above_moves_left_and_down():
    player = FakePlayer(240, 600)
    enemy = FakeEnemy(240, 560)
    game = FakeGame([enemy])
    ctrl = AutoPilotController()
    before = player.rect.center
    ctrl.update(player, game)
    after = player.rect.center
    # equal centerx → move left; enemy above → move down
    assert_move(dx_expected=-player.speed, dy_expected=player.speed, before=before, after=after)


def test_danger_left_moves_right():
    player = FakePlayer(240, 600)
    enemy = FakeEnemy(200, 600)
    game = FakeGame([enemy])
    ctrl = AutoPilotController()
    before = player.rect.center
    ctrl.update(player, game)
    after = player.rect.center
    assert_move(dx_expected=player.speed, dy_expected=0, before=before, after=after)


def test_no_danger_moves_toward_center():
    player = FakePlayer(100, 600)
    game = FakeGame([])
    ctrl = AutoPilotController()
    before = player.rect.center
    ctrl.update(player, game)
    after = player.rect.center
    assert_move(dx_expected=player.speed, dy_expected=0, before=before, after=after)


if __name__ == "__main__":
    pygame.init()
    try:
        test_danger_above_moves_left_and_down()
        test_danger_left_moves_right()
        test_no_danger_moves_toward_center()
        print("AutoPilot verification: OK")
    finally:
        pygame.quit()