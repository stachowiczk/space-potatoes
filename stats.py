import json
class Stats:

    def __init__(self, game_inst):
        self.settings = game_inst.settings
        self.reset()
        self.level_set()
        self._reset_boss_hp()
        self.game_active = False
        self.game_paused = False
        try:
            file = 'highscore.json'
            with open(file) as f:
                self.high_score = json.load(f)
        except:
            self.high_score = 0


    def reset(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def level_set(self):
        self.level = 0
        #atrybut row_level dodawany jest do liczby rzędów w metodzie
        # _create_fleet
        self.row_level = 0
    def _reset_boss_hp(self):
        if self.level == 0:
            self.boss_hp = self.settings.boss_hp
        else:
            self.boss_hp = self.settings.boss_hp + self.level

    def _save_high(self):
        file = 'highscore.json'
        with open(file, 'w') as f:
            json.dump(self.high_score, f)

