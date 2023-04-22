import pygame as pg
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    def __init__(self, game, ship):
        self.score = 0
        self.level = 0
        f = open("highscore.txt", "r")
        current_high_score = f.readline()
        temp = int(current_high_score)
        self.high_score = temp
        f.close()

        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None

        self.prep_ships(ship.ships_left)
        self.prep_score()
        self.prep_high_score()

    def increment_score(self, type):
        if type == 0:
            self.score += self.settings.alien_point0
        if type == 1:
            self.score += self.settings.alien_point1
        if type == 2:
            self.score += self.settings.alien_point2
        if type == 3:
            self.score += self.settings.ufo_point
        self.prep_score()
        self.check_high_score()

    def prep_ships(self, ships_left):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(ships_left):
            ship = Ship(game=self.game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        score_str = str(self.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = int(round(self.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score."""
        # open and read the file
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()

    def reset(self):
        self.score = 0
        self.update()

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)
