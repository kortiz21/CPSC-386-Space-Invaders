import pygame as pg
from settings import Settings
import game_functions as gf

from laser import Lasers, LaserType
from ufo import Ufos
from button import Button
from alien import Aliens
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers

TEXTCOLOR_WHITE = (255, 255, 255)
TEXTCOLOR_GREEN = (0, 255, 0)


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption('SPACE INVADERS')
        self.sound = Sound(bg_music="sounds/startrek.wav")
        pg.display.update()

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        self.ship = Ship(game=self)
        self.scoreboard = Scoreboard(game=self, ship=self.ship)
        self.barriers = Barriers(game=self)
        self.aliens = Aliens(game=self)
        self.ufo = Ufos(game=self)
        self.settings.initialize_speed_settings()
        self.play_button = Button(self.settings, self.screen, (self.settings.screen_width / 2),
                                  (self.settings.screen_height / 2) + 250, "PLAY")
        self.high_scores_button = Button(self.settings, self.screen,
                                         (self.settings.screen_width / 2),
                                         (self.settings.screen_height / 2) + 300,
                                         "HIGHSCORE: " + str(self.scoreboard.high_score))

    def drawmenu(self):
        # set screen to black to clear previous game screen
        self.screen.fill(self.settings.bg_color)
        # set up fonts for menu
        font_space = pg.font.SysFont(None, 200)
        font_invader = pg.font.SysFont(None, 100)
        font_pts = pg.font.SysFont(None, 40)
        # load in alien sprites and scale
        alien0 = pg.image.load(f'images/alien00.bmp')
        alien0 = pg.transform.scale(alien0, (45, 45))
        alien1 = pg.image.load(f'images/alien10.bmp')
        alien1 = pg.transform.scale(alien1, (45, 45))
        alien2 = pg.image.load(f'images/alien20.bmp')
        alien2 = pg.transform.scale(alien2, (45, 45))
        alien3 = pg.image.load(f'images/alien30.bmp')
        alien3 = pg.transform.scale(alien3, (45, 45))
        # draw game title
        self.drawtext('SPACE', font_space, self.screen,
                      (self.settings.screen_width / 2), (self.settings.screen_height / 2) - 300, TEXTCOLOR_WHITE)
        self.drawtext('INVADERS', font_invader, self.screen,
                      (self.settings.screen_width / 2), (self.settings.screen_height / 2) - 215, TEXTCOLOR_GREEN)
        # draw first alien with points
        self.screen.blit(alien0, ((self.settings.screen_width / 2) - 115, (self.settings.screen_height / 2) - 20))
        self.drawtext(' = 10 PTS', font_pts, self.screen,
                      (self.settings.screen_width / 2), (self.settings.screen_height / 2), TEXTCOLOR_WHITE)
        # draw second alien with points
        self.screen.blit(alien1, ((self.settings.screen_width / 2) - 115, (self.settings.screen_height / 2) + 30))
        self.drawtext(' = 20 PTS', font_pts, self.screen,
                      (self.settings.screen_width / 2), (self.settings.screen_height / 2) + 50, TEXTCOLOR_WHITE)
        # draw third alien with points
        self.screen.blit(alien2, ((self.settings.screen_width / 2) - 115, (self.settings.screen_height / 2) + 80))
        self.drawtext(' = 40 PTS', font_pts, self.screen,
                      (self.settings.screen_width / 2), (self.settings.screen_height / 2) + 100, TEXTCOLOR_WHITE)
        # draw fourth alien with points
        self.screen.blit(alien3, ((self.settings.screen_width / 2) - 115, (self.settings.screen_height / 2) + 130))
        self.drawtext(' = ???', font_pts, self.screen,
                      (self.settings.screen_width / 2) - 18, (self.settings.screen_height / 2) + 150, TEXTCOLOR_WHITE)

    def drawtext(self, text, font, surface, x, y, color):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def reset(self):
        print('Resetting game...')
        self.ship.reset()
        self.aliens.reset()
        self.scoreboard.reset()
        pg.mixer.music.stop()
        pg.mixer.music.load("sounds/startrek.wav")
        pg.mixer.music.play(-1, 0.0)

    def game_over(self):
        print('All ships gone: game over!')
        self.ship.timer.index = 0
        self.sound.gameover()
        self.settings.game_active = False
        self.ship.ships_left = 3
        f = open("highscore.txt", "w")
        f.write(str(self.scoreboard.high_score))
        f.close()

    def play(self):
        # Show the "Start" screen.
        self.sound.play_bg()
        while True:     # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            if not self.settings.game_active:
                self.drawmenu()
                self.play_button.draw_button()
                self.high_scores_button.draw_button()

            gf.check_events(settings=self.settings, ship=self.ship,
                            play_button=self.play_button, high_scores_button=self.high_scores_button)
            if self.settings.game_active:
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.aliens.update()
                self.ufo.update()
                self.barriers.update()
                self.scoreboard.update()
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
