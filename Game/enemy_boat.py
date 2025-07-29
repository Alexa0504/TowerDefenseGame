import pygame as pg
from pygame.math import Vector2
import math


class Enemy_boat(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.position = Vector2(self.waypoints[0])  # lista
        self.target_waypoint = 1  # következő lépés
        self.health = 200
        self.speed = 3
        self.angle = 0
        self.original_image = image  # megtartjuk az eredeti képet
        self.image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        self.move()
        self.rotate()

    def move(self):
        # define target waypoints
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.position
        else:
            # az enemy a path vegere ert
            self.kill()

        # távolság kiszámítása
        distance = self.movement.length()
        # Ha megmaradt távolság nagyobb mint az ellenség gyorsasága
        if distance >= self.speed:
            # normalize azt csinalja hogy mennyi pixelt megyunk balra es le
            self.position += self.movement.normalize() * self.speed  # speed miatt gyorsabban megy
        else:
            if distance != 0:
                self.position += self.movement.normalize() * distance  # mit csinal
            self.target_waypoint += 1
        self.rect.center = self.position

    def rotate(self):
        # kiszámolja a távolságot
        distance = self.target - self.position
        # kiszámolja a szöget
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))  # y koordináta meg van fordulva a pygame-be
        # a kép forgatása és frissítése
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()
