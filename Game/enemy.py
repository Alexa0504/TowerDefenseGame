import pygame as pg
from pygame.math import Vector2
import math
import time
import random
#from main import explosion_group, bumm_img, Explosion


class Enemy(pg.sprite.Sprite):
    def __init__(self, waypoint, image1, image2, health=100):  # ket kepet hasznalok a halakra
        pg.sprite.Sprite.__init__(self)
        self.waypoint = waypoint
        self.position = Vector2(self.waypoint[0])
        self.target_waypoint = 1
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
        #masodpercenkent egyszer valt
        self.animation_speed = 1
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
        #Ha eltelt több, mint 1 másodperc a képváltás óta
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
        # Ha már elérte az utolsó utvonalpontot, távolítsuk el, addig is irányvektort számítunk
        if self.target_waypoint < len(self.waypoint):
            # a target a következő utvonalpontra utal
            self.target = Vector2(self.waypoint[self.target_waypoint])#Vektorként tárolja nem tupleként
            self.movement = self.target - self.position#Honnan hová, irányvektor
        else:
            #eleri az enemy a veget a palyanak
            self.kill()
        #else:
            # ellenség eléri a pálya végét → robbanás és eltűnés
            #explosion = Explosion(self.position, [bumm_img])  # bumm_img-t át kell adni valahogy
            #explosion_group.add(explosion)
           # self.kill()


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
            self.target_waypoint +=1

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

