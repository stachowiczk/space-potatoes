import sys
import pygame
from settings import Settings
class Menu:

    def __init__(self, game_inst):
        pygame.init()
        self.settings = game_inst.settings
        self.screen = pygame.display.set_mode((int(self.settings.screen_height/3),
                                int(self.settings.screen_width/2)))
    def menu_running(self):
        while True:
            self._check_events()
    def _check_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        self.settings.console = False
                        self.game_inst.settings_window = ""
    if __name__ == '__main__':
        settings_inst = Menu()
        setings_inst.menu_running


