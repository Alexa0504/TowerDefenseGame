import pygame as pg
import constants as c


class World():
    def __init__(self, map_image):
        self.map_image = map_image
        self.health = c.HEALTH
        self.money = c.MONEY
        self.level = c.LEVEL
        self.wave=c.WAVE

    def draw(self, surface):
        surface.blit(self.map_image, (0, 0))
