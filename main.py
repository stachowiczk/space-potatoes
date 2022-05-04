import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Andrzej
from stats import Stats
from button import Button
from scores import Scores
from txt import TextInput
class Game:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screeen = self.check_fullscreen()
        pygame.display.set_caption('ALIENS')
        self.bg_color = (self.settings.bg_color)
        self.ship = Ship(self)
        self.stats = Stats(self)
        self.bullets = pygame.sprite.Group()
        self.console = self.settings.console
        self.color = 0
        self.andrzejs = pygame.sprite.Group()
        self._create_fleet(0)
        self.button = Button(self, "Play")
        self.scores = Scores(self)
        #self.textinput = TextInput()
        #self.box = InputBox(self, self.settings.screen_width/2,
        #                    self.settings.screen_height + 100, 200, 50)
    def check_fullscreen(self):
        """przenosi ustawienie fullscreen do settings.py"""
        if self.settings.fullscreen: #(0,0 to LEWY GÓRNY RÓG)
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
    def run_game(self):
        """main function"""
        while True:
            self._check_events()
            self._set_cursor()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_bullets()
                self._andrzejs_update()
            #self._open_console() #KEYDOWN: P self.console ==> True

            self._update_screen()

    def _check_events(self):
        """oczekuje na klawisze lub QUIT"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and not \
                    self.stats.game_active:
                self._check_play_button(self._get_mouse_pos())
            elif event.type == pygame.MOUSEBUTTONDOWN and self.stats.game_active:
                mouse_rel = self._get_bullet_direction()
                self._fire_bullet(mouse_rel)
                self._update_color()

    def _get_mouse_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        return mouse_pos

    def _check_play_button(self, mouse_pos):
        button_clicked = self.button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            if not self.stats.game_paused:
                pygame.mouse.set_visible(True)
                self.settings.initialize_dynamic_settings()
                self.stats.reset()
                self.stats.level_set()
                self.stats._reset_boss_hp()
                self.stats.game_active = True
                self.andrzejs.empty()
                self.bullets.empty()
                self._create_fleet(0)
                self.ship.center_ship()
            else:
                self.stats.game_active = True
            sleep(1)

    def _open_console(self):
        """umożliwia użytkownikowi zmianę niektórych ustawień"""
        if self.settings.console == True:
            self.settings.setting_choose()
            self.settings.console = False
    def _set_cursor(self):
        if self.stats.game_active:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            mouse_rel = self._get_bullet_direction()
            self._fire_bullet(mouse_rel)
            self._update_color()
        elif event.key == pygame.K_p and self.stats.game_active:
            self.stats.game_active = False
            self.stats.game_paused = True

        elif event.key == pygame.K_p and not self.stats.game_active:
            self.stats.game_active = True
            self.stats.game_paused = False
            sleep(1)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_w or event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _get_bullet_direction(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_y = mouse_pos[1]
        if mouse_y in range(0, int(self.settings.screen_height / 2)):
            mouse_rel = 0 - ((self.settings.screen_height / 2) - mouse_y)
        else:
            mouse_rel = mouse_y - (self.settings.screen_height / 2)
        return mouse_rel

    def _fire_bullet(self, mouse_rel):
        if len(self.bullets) < self.settings.bullets_limit:
            new_bullet = Bullet(self, mouse_rel)
            self.bullets.add(new_bullet)

    def _update_color(self):
        """sekwencyjna zmiana koloru pocisku"""
        if self.color == 6:
            self.color = 0
        else:
            self.color += 1

    def _update_bullets(self):
        """usuwa pociski poza ekranem i sprawdza kolizje"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width:
                #or
                #bullet.rect.top < 0 or
                #bullet.rect.bottom > self.settings.screen_height):
                self.bullets.remove(bullet)
        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        #if self.color < 4:
        if self.stats.level in self.settings.boss_levels and \
                self.stats.boss_hp != 0:
            collisions = pygame.sprite.groupcollide(self.bullets,
                                                        self.andrzejs,
                                                        True, False)
            if collisions:
                self.stats.boss_hp -= 1
        else:
            collisions = pygame.sprite.groupcollide(self.bullets, self.andrzejs,
                                                    True, True)
            if collisions:
                if self.stats.level in self.settings.boss_levels:
                    self.stats.score += self.settings.boss_pts
                    self.scores.prep_score()
                    self.scores.check_high()
                else:
                    for andrzejs in collisions.values():
                        self.stats.score += self.settings.pts * len(andrzejs)
                        self.scores.prep_score()
                        self.scores.check_high()
        if not self.andrzejs:
            self._next_level()

    def _next_level(self):
        self.settings._more_points()
        self.bullets.empty()
        self.stats._reset_boss_hp()
        self.stats.level += 1
        self.scores.prep_level()
        if self.stats.level % 3 == 0 and self.stats.level <= 6:
            self.settings._increase_speed()
        elif self.stats.level % 2 == 0 and self.stats.level <= 15 and not \
                self.stats.level <= 6:
            self.stats.row_level += 1
        elif self.stats.level % 3 == 0 and not self.stats.level <= 15:
            self.stats.row_level += 1
        if self.stats.level not in self.settings.boss_levels:
            self._create_fleet(self.stats.row_level)
        else:
            self._create_boss()
    def _andrzejs_update(self):
        self._check_andrzej_edges()
        self.andrzejs.update()
        if pygame.sprite.spritecollideany(self.ship, self.andrzejs):
            self._ship_hit()
        self._bottom_hit()

    def _check_andrzej_edges(self):
        """jeśli któryś andrzej dotyka krawędzi, wszystkie zmieniają kierunek"""
        for andrzej in self.andrzejs.sprites():
            if andrzej._check_edges():
                self._change_andrzej_dir()
                break

    def _change_andrzej_dir(self):
        """zmiana kierunku andrzejów + przysunięcie do gracza"""
        self.settings.andrzej_dir *= -1
        for andrzej in self.andrzejs.sprites():
            if andrzej.type == 0:
                andrzej.rect.x -= self.settings.andrzej_left
            else:
                andrzej.rect.x -= self.settings.andrzej_left * 3

    def _create_fleet(self, add_rows):
        """tworzy flotę andrzejów, ustala liczbę rzędów"""
        andrzej = Andrzej(self, 0)
        andrzej_height = andrzej.rect.height
        andrzej_width = andrzej.rect.width
        av_space_y = self.settings.screen_height - 2 * andrzej_height
        no_of_andrzejs = (av_space_y // (2 * andrzej_height)) + 1
        ship_width = self.ship.rect.width
        av_space_x = (self.settings.screen_width - (3 * andrzej_width) -
                      ship_width)
                                 #więcej = mniej rzędów
        no_rows = av_space_x // (8 * andrzej_width)
        for row_number in range(no_rows + add_rows): #add_rows jest w stats.py
            self._alternate_row_speed(row_number)
            for andrzej_number in range(int(no_of_andrzejs)):
                self._create_andrzej(andrzej_number, row_number)

    def _create_boss(self):
        andrzej = Andrzej(self, 1)
        boss_w = andrzej.rect.width
        andrzej.y = self.settings.screen_height * 0.25
        andrzej.rect.y = int(andrzej.y)
        andrzej.rect.x = self.settings.screen_width - boss_w
        self.andrzejs.add(andrzej)

    def _alternate_row_speed(self, row_number):
        """rzędy andrzejów latają w przeciwnych kierunkach"""
        if int(row_number) % 2 == 0 or int(row_number) == 0:
            self.settings.andrzej_speed *= 1.1
        else:
            self.settings.andrzej_speed *= 0.9

    def _create_andrzej(self, andrzej_number, row_number):
        """tworzy jednego andrzeja, wywoływana przy tworezeniu floty"""
        andrzej = Andrzej(self, 0)
        andrzej_height = andrzej.rect.height
        andrzej_width = andrzej.rect.width
        andrzej.y = andrzej_height + 2 * andrzej_height * andrzej_number
        andrzej.rect.y = andrzej.y#zmiana odległosci między rzędami
        andrzej.rect.x = self.settings.screen_width - \
                         andrzej.rect.width - 2 * andrzej_width * row_number
        self.andrzejs.add(andrzej)

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.scores.prep_cats()
            self.andrzejs.empty()
            self.bullets.empty()
            self._create_fleet(0)
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _bottom_hit(self):
        screen_rect = self.screen.get_rect()
        for andrzej in self.andrzejs.sprites():
            if andrzej.rect.left <= screen_rect.left:
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_image()
        self.andrzejs.draw(self.screen)
        self.scores.show_score()
        if not self.stats.game_active:
            self.button.draw_button()


        #    self.box.draw()
        pygame.display.flip()


if __name__=='__main__':
    game_inst = Game()
    game_inst.run_game()
