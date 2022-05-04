import pygame
from pygame.sprite import Sprite

class Andrzej(Sprite):

    def __init__(self, game_inst, type):
        super().__init__()
        self.screen = game_inst.screen
        self.settings = game_inst.settings
        self.type = type
        if self.type == 0:
            self.image = pygame.image.load('images/moron.png')
            self.speed = self.settings.andrzej_speed
            self.rect = self.image.get_rect()
            self.rect.x = self.settings.screen_width - (2 * self.rect.width)
            self.rect.y = self.rect.height
        else:
            self.image = pygame.image.load('images/kitkus.png')
            self.rect = self.image.get_rect()
            self.speed = self.settings.boss_speed
            self.rect.x = self.settings.screen_width - self.rect.width
            self.rect.y = self.rect.height * 0.3
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.y += (self.speed * self.settings.andrzej_dir)
        self.rect.y = self.y

    def _check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True









