import pygame as pg
from pygame.math import Vector2
import math
import time
import random


class Enemy(pg.sprite.Sprite):
    def __init__(self,waypoint,image,health=100):
        pg.sprite.Sprite.__init__(self)
        self.waypoint=waypoint
        self.position=Vector2(self.waypoint[0])
        self.target_waypoint=1
        self.speed=3
        self.health=health
        self.angle=0

        self.original_image=image

        self.animation_speed = 1
        self.last_switch_time = time.time()

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # Ha már elérte az utolsó utvonalpontot, távolítsuk el, addig is irányvektort számítunk
        if self.target_waypoint < len(self.waypoint):
            # a target a következő utvonalpontra utal
            self.target = Vector2(self.waypoint[self.target_waypoint])  # Vektorként tárolja nem tupleként
            self.movement = self.target - self.position  # Honnan hová, irányvektor
        else:
            # eleri az enemy a veget a palyanak
            self.kill()

        # kiszamitom a tavolsagot, azert hogy ne ragadjon be ha iranyt kell valtoztasson
        dist = self.movement.length()

        # megnezi hogy eleg tavolsag maradt e
        if dist >= self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            # error check
            if dist != 0:
                self.position += self.movement.normalize() * dist
            # ha ezt nem irom oda akkor kidob mert eleri a 0at
            self.target_waypoint += 1

    def rotate(self):
        dist = self.target - self.position
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # rotate image and update rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

