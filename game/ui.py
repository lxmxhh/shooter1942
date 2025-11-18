import pygame
from .settings import WHITE

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.SysFont(None, size)
    img = font.render(text, True, color)
    rect = img.get_rect()
    rect.center = (x, y)
    surface.blit(img, rect)