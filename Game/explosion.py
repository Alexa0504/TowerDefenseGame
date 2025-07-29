import pygame as pg


class Explosion(pg.sprite.Sprite):
    def __init__(self, position, image, duration=500):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.duration = duration
        self.position = self.rect.center
        self.rect = self.image.get_rect()
        self.start_time = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.start_time >= self.duration:
            self.kill()
