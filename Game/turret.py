import pygame as pg
from turret_data import TURRET_DATA
import constants as c


class Turret(pg.sprite.Sprite):
    """The Tower class represents a tower in the game."""

    def __init__(self, all_images, position):
        """Initialize the turret with its images and position."""

        pg.sprite.Sprite.__init__(self)
        self.upgrade_level = 0  # Starting upgrade level
        # Store all images for different upgrade levels
        self.all_images = all_images # A dictionary where keys are upgrade levels and values are lists of images
        self.images = self.all_images[self.upgrade_level] # List of images for the current upgrade level
        self.image = self.images[0] # The first image in the list is the default image
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Initialize stats based on the current upgrade level
        self.set_stats()

        # Animation attributes
        self.animating = False
        self.frame_index = 0
        self.last_update = pg.time.get_ticks()
        self.animation_speed = 100

    def set_stats(self):
        """Sets the turret's stats based on the current upgrade level."""
        """Sets the turret's range and damage based on the upgrade level."""
        stats = TURRET_DATA[self.upgrade_level] # A dictionary containing stats for the current upgrade level
        self.range = stats["range"] # The range of the turret
        self.damage = stats["damage"] # The damage dealt by the turret

    def upgrade(self):
        """Upgrades the turret to the next level if available."""

        if self.upgrade_level + 1 < len(TURRET_DATA): # Check if there is a next upgrade level
            self.upgrade_level += 1 # Increment the upgrade level
            self.images = self.all_images[self.upgrade_level] # Update the images to the next level's images
            self.image = self.images[0] # Reset to the first image of the new level
            self.set_stats()  # Update stats after upgrade
            return True #The upgrade was successful
        return False # No further upgrades available, return False

    def update(self):
        """Update the turret's state: animate if necessary."""

        now = pg.time.get_ticks()
        if self.animating:
            # If the turret is animating, update the frame based on the animation speed
            # Check if enough time has passed to update the frame
            if now - self.last_update > self.animation_speed: #Consistent frame rate
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.images): #If the frame index reaches the end of the images list
                    # Reset the frame index and stop animating
                    self.frame_index = 0
                    self.animating = False
                # Update the turret's image to the current frame
                self.image = self.images[self.frame_index]


    def fire(self):
        """Starts the firing animation of the turret."""

        # Check if the turret is not already animating
        # This prevents the turret from starting a new animation if it's already in one
        if not self.animating:
            self.animating = True
            self.frame_index = 0
            self.last_update = pg.time.get_ticks()

    def draw(self, surface, selected=False):
        """Draws the turret on the given surface, optionally showing its range if selected."""

        if selected:
            # Draw the range of the turret
            range_surface = pg.Surface((self.range * 2, self.range * 2), pg.SRCALPHA) # Create a transparent surface for the range
            # Draw a circle on the range surface with a semi-transparent color
            pg.draw.circle(range_surface, (100, 100, 255, 100), (self.range, self.range), self.range)
           # Blit the range surface onto the main surface at the turret's center position
            surface.blit(range_surface, (self.rect.centerx - self.range, self.rect.centery - self.range))

        # Draw the turret image on the surface
        surface.blit(self.image, self.rect)