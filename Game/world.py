import pygame as pg
import constants as c


class World():
    """The World class represents the game world, including the map and game state."""

    def __init__(self, map_image):
        """Initialize the world with a map image and game state."""
        self.map_image = map_image
        self.health = c.HEALTH
        self.money = c.MONEY
        self.level = c.LEVEL
        self.wave=c.WAVE

    def draw(self, surface):
        surface.blit(self.map_image, (0, 0))
