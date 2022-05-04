from button import Button
class Settings:

    def __init__(self):
        self.testmode = False
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 0)
        self.ship_limit = 3
        self.fullscreen = False
        self.bullet_y = 3000
        self.bullet_x = 70
        self.colors = [
            (255, 0, 0),
            (255, 128, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (255, 0, 255),
        ]
        self.bullets_limit = 4
        self.console = False
        self.boss_levels = [2, 5, 9]
        self.andrzej_left = 8
        self.boss_hp = 3
        self.difficulty_scaling = 1.2
        self.initialize_dynamic_settings()
        self.pts_multiplier = 1.5
    def initialize_dynamic_settings(self):
        self.ship_speed = 2.5
        self.bullet_speed = 5
        self.andrzej_speed = 0.50
        self.andrzej_dir = 1
        self.boss_speed = 1.2
        self.pts = 10
        self.boss_pts = 50
    def _increase_speed(self):
        self.ship_speed *= self.difficulty_scaling
        #self.bullet_speed *= self.difficulty_scaling
        self.andrzej_speed *= self.difficulty_scaling
        self.boss_speed *= self.difficulty_scaling

    def _more_points(self):
        self.pts *= self.pts_multiplier
        self.boss_pts *= self.pts_multiplier
    def setting_choose(self):
        choose = ''
        while choose != 'b' and choose != 'a':
            choose = input("press b for bullet speed and a for andrzej speed: ")
        if choose == 'b':
            self._change_bullet_speed()
        else:
            self._change_andrzej_speed()

    def _change_bullet_speed(self):
        new_speed = input('speed: ')
        try:
            if float(new_speed) != 0:
                self.bullet_speed = float(new_speed)
        except:
            pass
    def _change_andrzej_speed(self):
        new_speed = input('speed: \n give letter as input to cancel')
        try:
            if float(new_speed) != 0:
                self.andrzej_left = float(new_speed)
        except:
            pass

class PauseMenu(Button):

    def __init__(self, game_inst, msg):
        super.__init__()












