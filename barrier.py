import pygame as pg
from pygame.sprite import Sprite, Group


class Block(Sprite):
    shape = [
        '  XXXXXXX',
        ' XXXXXXXXX',
        'XXXXXXXXXXX',
        'XXXXXXXXXXX',
        'XXXXXXXXXXX',
        'XXX     XXX',
        'XX       XX']

    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


class Barriers:
    def __init__(self, game):
        self.game = game
        self.aliens_lasers = game.alien_lasers.lasers
        self.ship_lasers = game.ship_lasers.lasers
        self.settings = game.settings
        self.screen = game.screen

        self.width = self.settings.screen_width / 10
        self.height = 2.0 * self.width / 4.0
        self.top = self.settings.screen_height - 2.1 * self.height

        self.shape = Block.shape
        self.block_size = 6
        self.blocks = Group()
        self.create_multiple_obstacles(x_start=0, y_start=self.top)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'X':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, x_start, y_start):
        for n in range(4):
            offset_x = n * 2 * self.width + 1.5 * self.width
            self.create_obstacle(x_start, y_start, offset_x)

    def check_collisions(self):
        # alien_lasers hitting a barrier
        pg.sprite.groupcollide(self.blocks, self.aliens_lasers, True, True)
        # ship_lasers hitting a barrier
        pg.sprite.groupcollide(self.blocks, self.ship_lasers, True, True)

    def update(self):
        self.draw()
        self.check_collisions()

    def draw(self):
        self.blocks.draw(self.screen)
