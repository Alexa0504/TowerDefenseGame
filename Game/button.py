import pygame as pg


class Button:
    def __init__(self, x, y, image, single_click):
        """Initialize the button with position, image, and click behavior."""

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        # Draw the button on the surface and handle click events.
        action = False

        #Mouse position
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:  # Left mouse button pressed
                # If the mouse is over the button and the left button is pressed
                # and we haven't clicked yet, then we can perform the action
                action = True
                # If single_click is True, we only want to register the click once
                if self.single_click:
                    self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:  # Left mouse button released
            self.clicked = False

        # Draw the button image on the surface
        surface.blit(self.image, self.rect)

        return action
