import pygame as pg

class Tower(pg.sprite.Sprite):
    def __init__(self, images, position):
        #super().__init__() ugynaz mint a kovetkezo sor
        pg.sprite.Sprite.__init__(self)
        self.images = images  # lista: animációs képek
        self.image = self.images[0]  # kezdőkép
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Animációs állapotok
        self.animating = False
        self.frame_index = 0
        self.last_update = pg.time.get_ticks()
        self.animation_speed = 100  # ms/frame

    def update(self):
        if self.animating:
            now = pg.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.images):
                    self.frame_index = 0
                    self.animating = False  # animáció vége
                self.image = self.images[self.frame_index]

    def fire(self):
        self.animating = True
        self.frame_index = 0
        self.image = self.images[0]