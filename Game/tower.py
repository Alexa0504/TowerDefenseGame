import pygame as pg

class Tower(pg.sprite.Sprite):
    def __init__(self,image,position):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
