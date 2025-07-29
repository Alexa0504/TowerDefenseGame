import pygame as pg


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, image_normal, image_clicked=None):
        """
        Gomb osztály Pygame-hez, ami kezeli a kattintás vizuális visszajelzését.

        Args:
            x (int): A gomb bal felső sarkának X koordinátája.
            y (int): A gomb bal felső sarkának Y koordinátája.
            image_normal (pg.Surface): A gomb alapértelmezett (nem lenyomott) képe.
            image_clicked (pg.Surface, optional): A gomb képe lenyomott állapotban.
                                                  Ha nincs megadva, az image_normal lesz használva.
        """
        super().__init__()
        self.image_normal = image_normal
        # Ha nincs megadva image_clicked, akkor az image_normal lesz használva a lenyomott állapothoz is
        self.image_clicked = image_clicked if image_clicked is not None else image_normal
        self.image = self.image_normal  # Az aktuálisan megjelenített kép
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_pressed = False  # Jelzi, hogy a gomb éppen le van-e nyomva az egérrel
        self.action = False  # Jelzi, hogy a gombra sikeresen rákattintottak-e (lenyomás és felengedés)

    def draw(self, surface):
        """
        Kirajzolja a gombot a felületre, és kezeli az egér eseményeket.

        Args:
            surface (pg.Surface): Az a felület, amire a gombot rajzolni kell.

        Returns:
            bool: True, ha a gombra rákattintottak (mouse down és mouse up történt), egyébként False.
        """
        self.action = False  # Alaphelyzetbe állítás minden képkockánál
        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]

        # Ellenőrizzük, hogy az egér a gomb felett van-e
        if self.rect.collidepoint(mouse_pos):
            if left_click == 1 and not self.is_pressed:
                # Gomb lenyomva
                self.image = self.image_clicked
                self.is_pressed = True

            if left_click == 0 and self.is_pressed:
                # Gomb felengedve, és előtte le volt nyomva (sikeres kattintás)
                self.image = self.image_normal
                self.is_pressed = False
                self.action = True  # Ekkor váltja ki az akciót

        elif self.is_pressed:
            # Ha az egér elhagyta a gombot lenyomott állapotban, engedjük el
            self.image = self.image_normal
            self.is_pressed = False

        # Ha az egér nincs a gomb felett és nincs lenyomva
        if not self.rect.collidepoint(mouse_pos) and not self.is_pressed:
            self.image = self.image_normal

        surface.blit(self.image, self.rect)
        return self.action