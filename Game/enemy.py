import pygame as pg
from pygame.math import Vector2
import math
import time
import random


class Enemy(pg.sprite.Sprite):
    def __init__(self, koordinatak, image1, image2, health=100):  # ket kepet hasznalok
        pg.sprite.Sprite.__init__(self)
        self.koordinatak = koordinatak
        self.position = Vector2(self.koordinatak[0])
        self.target_koordinata = 1
        self.speed = 2
        self.health = health
        self.angle = 0

        # Véletlenszerűen választunk a két méret közül
        self.is_big = random.choice([True, False])

        # Méret és életerő beállítása
        if self.is_big:
            self.scale = 1.5  # Nagyobb méret
            self.health = 150  # Több életerő
        else:
            self.scale = 1.0  # Normál méret
            self.health = 100  # Alap életerő

        # Képek méretezése
        self.original_image1 = pg.transform.scale_by(image1, self.scale)
        self.original_image2 = pg.transform.scale_by(image2, self.scale)

        self.current_image = self.original_image1
        self.original = self.current_image
        self.image = pg.transform.rotate(self.original, self.angle)

        # Animációhoz
        self.animation_speed = 0.5
        self.last_switch_time = time.time()

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        self.animate()
        self.move()
        self.rotate()

    def animate(self):
        # Képváltás időzítése
        current_time = time.time()
        if current_time - self.last_switch_time > self.animation_speed:
            self.last_switch_time = current_time
            # Kép váltogatása
            if self.current_image == self.original_image1:
                self.current_image = self.original_image2
            else:
                self.current_image = self.original_image1
            # Frissítjük az original-t is a forgatáshoz
            self.original = self.current_image

    def move(self):
        # Ha már elérte az utolsó waypointot, távolítsuk el
        if self.target_koordinata < len(self.koordinatak):
            # define target waypoint
            self.target = Vector2(self.koordinatak[self.target_koordinata])
            self.movement = self.target - self.position
        else:
            #eleri az enemy a veget a palyanak
            self.kill()


        #kiszamitom a tavolsagot, azert hogy ne ragadjon be ha iranyt kell valtoztasson
        dist=self.movement.length()

        #megnezi hogy eleg tavolsag maradt e
        if dist>=self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            #error check
            if dist != 0:
              self.position += self.movement.normalize() * dist
            #ha ezt nem irom oda akkor kidob mert eleri a 0at
            self.target_koordinata +=1

    def rotate(self):
        dist=self.target-self.position
        self.angle=math.degrees(math.atan2(-dist[1],dist[0]))
        #rotate image and update rectangle
        self.image = pg.transform.rotate(self.original,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

