from random import randint, choice
import pygame as pg
from pygame.sprite import Sprite, GroupSingle


class Ufo(Sprite):
    def __init__(self, game, spawn):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load('images/alien30.bmp'), (60, 58))
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.sb = game.scoreboard
        pointlist = [50, 100, 150, 200, 300]
        self.ufo_point = choice(pointlist)
        self.settings.ufo_point = self.ufo_point
        self.type = 3
        if spawn == 'right':
            self.x = self.settings.screen_width + 50
            self.speed = -2
        else:
            self.x = -50
            self.speed = 2
        self.rect = self.image.get_rect(topleft=(self.x, 0))
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.sound.ufo_oscillating()

    def hit(self):
        self.sb.increment_score(self.type)
        self.display_points()

    def display_points(self):
        font = pg.font.SysFont(None, 100)
        text = font.render(str(self.ufo_point), True, (0, 255, 0), (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center
        self.screen.blit(text, text_rect)
        print(str(self.ufo_point))

    def update(self):
        self.rect.x += self.speed
        self.draw()

    def draw(self):
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(self.image, rect)


class Ufos:
    def __init__(self, game):
        self.game = game
        self.sb = game.scoreboard
        self.ufos = GroupSingle()
        self.extra_spawn_time = randint(500, 1000)
        self.ship_lasers = game.ship_lasers.lasers  # a laser Group
        self.screen = game.screen
        self.settings = game.settings
        self.ship = game.ship

    def ufo_timer(self):
        self.extra_spawn_time -= 0.5
        if self.extra_spawn_time <= 0:
            spawn = choice(['right', 'left'])
            ufo = Ufo(game=self.game, spawn=spawn)
            self.ufos.add(ufo)
            self.extra_spawn_time = randint(500, 1000)

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.ufos, self.ship_lasers, False, True)
        if collisions:
            for ufo in collisions:
                ufo.hit()
                ufo.kill()

    def update(self):
        self.check_collisions()
        self.ufo_timer()
        for ufo in self.ufos.sprites():
            ufo.update()

    def draw(self):
        for ufo in self.ufos.sprites():
            ufo.draw()
