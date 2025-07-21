import pygame as pg

class World():
    def __init__(self,map_image):
        self.map_image = map_image

    def draw(self,surface):
        surface.blit(self.map_image,(0,0))