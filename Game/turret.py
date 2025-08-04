import pygame as pg
from turret_data import TURRET_DATA
import constants as c


class Turret(pg.sprite.Sprite):
    """The Tower class represents a tower in the game."""

    def __init__(self, images, position):
        """Initialize the tower with images and position."""

        # super().__init__() # This is an alternative way to call the parent class constructor
        pg.sprite.Sprite.__init__(self)
        self.upgrade_level=1
        self.range = TURRET_DATA[self.upgrade_level-1].get("range")  # Range of the tower based on upgrade level
        self.damage = TURRET_DATA[self.upgrade_level - 1].get("damage")
        self.upgrade_cost = TURRET_DATA[self.upgrade_level - 1].get("upgrade_cost")
        self.upgrade_cost = 50
        self.images = images  #List of images for the tower
        self.image = self.images[0]  # The first image is the default one
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.selected = False

        #Animation attributes
        self.animating = False
        self.frame_index = 0
        self.last_update = pg.time.get_ticks()
        self.animation_speed = 100  # 0.1 sec per frame

    def update(self):

        # Update the range circle image
        self.range_img = pg.Surface((self.range * 2, self.range * 2))
        self.range_img.fill((0, 0, 0))
        self.range_img.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_img, "grey100", (self.range, self.range), self.range)
        self.range_img.set_alpha(100)  # 100 means 100/255 opacity
        self.range_rect = self.range_img.get_rect()  #The circle's rectangle

        # Set the position of the range rectangle to the center of the tower
        self.range_rect.center = self.rect.center

        if self.animating:
            now = pg.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.images):
                    self.frame_index = 0
                    self.animating = False  # The end of the animation
                # Update the image to the next frame
                self.image = self.images[self.frame_index]

    def upgrade(self):
        self.upgrade_level += 1

        # Check if the upgrade level exceeds the maximum level
        self.range = TURRET_DATA[self.upgrade_level - 1].get("range")
        self.damage = TURRET_DATA[self.upgrade_level - 1].get("damage")
        self.upgrade_cost = TURRET_DATA[self.upgrade_level - 1].get("upgrade_cost")

        # Check if the upgrade level is within the valid range
        self.image = self.images[self.upgrade_level - 1]
        # Update the range circle image based on the new upgrade level
        # Update the range circle image
        self.range_img = pg.Surface((self.range * 2, self.range * 2))
        self.range_img.fill((0, 0, 0))
        self.range_img.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_img, "grey100", (self.range, self.range), self.range)
        self.range_img.set_alpha(100)  # 100 means 100/255 opacity
        self.range_rect = self.range_img.get_rect()  #The circle's rectangle

        # Set the position of the range rectangle to the center of the tower
        self.range_rect.center = self.rect.center

    def fire(self):
        # This method is called to start the animation
        if not self.animating:
            self.animating = True
            self.frame_index = 0
            self.image = self.images[0]

    def draw(self, surface, selected=False):
        if selected:
            surface.blit(self.range_img, self.range_rect)  # Draw the range circle
        # Draw the tower image
        surface.blit(self.image, self.rect)
