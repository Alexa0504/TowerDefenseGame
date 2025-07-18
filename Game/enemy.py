import pygame as pg
from pygame.math import Vector2
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self,waypoints,image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints=waypoints
        self.position=Vector2(self.waypoints[0])
        #kovetkezo lepes
        self.target_waypoint=1
        self.speed=2
        self.angle=0
        self.original:image=image
        self.image = pg.transform.rotate(self.original,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # Ha már elérte az utolsó waypointot, távolítsuk el
        if self.target_waypoint >= len(self.waypoints):
            self.kill()
            return

        #define target waypoint
        self.target=Vector2(self.waypoints[self.target_waypoint])
        self.movement=self.target-self.position

        #kiszamitom a tavolsagot
        dist=self.movement.length()

        if dist>=self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            if dist != 0:
              self.position += self.movement.normalize() * dist
            self.target_waypoint +=1

    def rotate(self):
        dist=self.target-self.position
        self.angle=math.degrees(math.atan2(-dist[1],dist[0]))
#rotate image and update rectangle
        self.image = pg.transform.rotate(self.original,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

