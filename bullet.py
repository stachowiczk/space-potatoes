import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):

    def __init__(self, game_inst, rel_pos):
        super().__init__()
        self.screen = game_inst.screen
        self.settings = game_inst.settings
        self.ship = game_inst.ship
        if self.settings.testmode == True:
            self.bullet_color = self.settings.colors[game_inst.color]
            self.rect = pygame.Rect(
                0, 0, self.settings.bullet_x,
                self.settings.bullet_y)
        else:
            self.image = pygame.image.load('images/potato.png')
            self.rect = self.image.get_rect(center = game_inst.ship.rect.center)
        self.rect.center = self.ship.rect.center
        self.x = float(self.rect.x) + 100
        self.y = float(self.rect.y)
        self.y_delta = rel_pos

    def update(self):
        self.x += self.settings.bullet_speed
        self.rect.x = self.x
        self.y += (self.y_delta * self.settings.bullet_speed)\
                  / self.settings.screen_height
        self.rect.y = self.y

    def draw_image(self):
        if self.settings.testmode == False:
            self.screen.blit(self.image, self.rect)
        else:
            pygame.draw.rect(self.screen, self.bullet_color, self.rect)

    """
    metoda do robienia kolorowych prostokątów
    pygame.Rect(
            0, 0, self.settings.bullet_x,
            self.settings.bullet_y
        )
    """




