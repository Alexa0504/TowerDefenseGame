import pygame as pg

class Tower(pg.sprite.Sprite):
    def __init__(self, images, position):
        #super().__init__() ugynaz mint a kovetkezo sor
        pg.sprite.Sprite.__init__(self)
        self.range=90
        self.images = images  # lista: animációs képek
        self.image = self.images[0]  # kezdőkép
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.selected=False

        # Animációs állapotok
        self.animating = False
        self.frame_index = 0
        self.last_update = pg.time.get_ticks()
        self.animation_speed = 100  # 0.1 másodperc


    def update(self):

        # Frissítem a range_img-et
        self.range_img = pg.Surface((self.range * 2, self.range * 2))
        self.range_img.fill((0, 0, 0))
        self.range_img.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_img, "grey100", (self.range, self.range), self.range)
        self.range_img.set_alpha(100)# a 100 a félig áttetszőt jelenti
        self.range_rect = self.range_img.get_rect()#a körnek is lesz rect-je így kitudom majd rajzolni

        # A közepe a toronyé lesz
        self.range_rect.center = self.rect.center


        if self.animating:
            now = pg.time.get_ticks()
            if now - self.last_update > self.animation_speed:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.images):
                    self.frame_index = 0
                    self.animating = False  # animáció vége
                # beállítom a torony aktuális képét az animációs fázishoz
                self.image = self.images[self.frame_index]

    def fire(self):
        #csak akkor kezd el uj animaciot ha eppen nem animal így nem akadozik
        if not self.animating:
            self.animating = True
            self.frame_index = 0
            self.image = self.images[0]


    def draw(self, surface, selected=False):
        if selected:
            surface.blit(self.range_img, self.range_rect)# range kirajzolása, blit a kép felületre másolása
        # torony kirajzolása
        surface.blit(self.image, self.rect)