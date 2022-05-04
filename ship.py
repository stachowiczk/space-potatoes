import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self, game_inst):
        super().__init__()
        self.screen = game_inst.screen
        self.screen_rect = game_inst.screen.get_rect()
        self.settings = game_inst.settings
        self.image = pygame.image.load('images/cat.png') #można obrócić
        self.rect = self.image.get_rect()

        self.rect.y = self.settings.screen_height/2
        self.rect.x = 20
        self.moving_up = False
        self.moving_down = False

        self.y = float(self.rect.y)
    def update(self):
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.rect.bottom < self.settings.screen_height:
            self.y += self.settings.ship_speed
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.y = self.settings.screen_height/2
        self.y = float(self.rect.y)


