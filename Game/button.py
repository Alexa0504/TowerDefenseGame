import pygame as pg


class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        # kattintas
        action = False

        # eger pozicio
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:  # csak bal klikk a 0
                action = True  # ha kattintok akkor igazza valik
                # ha egszer lehet kattintani a gombra
                if self.single_click:
                    self.clicked = True

        if pg.mouse.get_pressed()[
            0] == 0:  # ha a bal klikk es ennyi, vagyis ha mar egsyer klikkeltunk lehet tobbszor is
            self.clicked = False

        # kirajzolom a gombot a screenre
        surface.blit(self.image, self.rect)

        return action
