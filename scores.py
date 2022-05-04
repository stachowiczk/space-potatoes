from ship import Ship
from pygame.sprite import Group
import pygame.font
class Scores:

    def __init__(self, game_inst):
        self.game_inst = game_inst
        self.screen = game_inst.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_inst.settings
        self.stats = game_inst.stats
        self.text_color = (255, 0 ,0)
        self.font = pygame.font.SysFont(None, 36)
        self.prep_score()
        self.prep_high()
        self.prep_level()
        self.prep_cats()
        self.prep_cats()

    def prep_score(self):
        round_score = round(int(self.stats.score), -1)
        score_str = f'Points: {"{:,}".format(round_score)}'
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_image, self.high_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.cats.draw(self.screen)
    def check_high(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.stats._save_high()
            self.prep_high()
    def prep_high(self):
        round_high = round(int(self.stats.high_score), -1)
        high_str = f'Highscore: {"{:,}".format(round_high)}'

        self.high_image = self.font.render(high_str, True,
                                                 self.text_color)
        self.high_rect = self.high_image.get_rect()
        self.high_rect.top = 20
        self.high_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        level = self.stats.level + 1
        score_str = f'Level: {str(level)}'

        self.level_image = self.font.render(score_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = 20
        self.level_rect.bottom = self.settings.screen_height - 20

    def prep_cats(self):
        self.cats = Group()
        for cat_number in range(self.stats.ships_left):
            cat = Ship(self.game_inst)
            cat.rect.x = 20 + cat_number * cat.rect.width
            cat.rect.y = 20 + cat.rect.height
            self.cats.add(cat)

