import json
import pygame as pg
from stats import Stats
class InputBox():

    def __init__(self, game_inst, x, y, w, h, text=''):
        self.screen = game_inst.screen
        self.font = pg.font.Font(None, 32)
        self.rect = pg.Rect(x, y, w, h)
        self.color = (255, 0, 0)
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.stats.game_active = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(self.screen, self.color, self.rect, 2)