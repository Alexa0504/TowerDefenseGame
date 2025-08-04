import pygame as pg
from pygame.math import Vector2
import math
import time


class Enemy_jellyfish(pg.sprite.Sprite):
    """The Enemy_jellyfish class represents a jellyfish enemy in the game."""

    def __init__(self, waypoint, images, health=200):
        """Initialize the jellyfish with waypoints, images, and health."""

        pg.sprite.Sprite.__init__(self)
        self.images = images  # List of images for the jellyfish animation
        self.current_image_index = 0  # Index of the current image
        self.original_image = self.images[self.current_image_index]  # The image to be rotated
        self.image = self.original_image

        self.waypoint = waypoint
        self.position = Vector2(self.waypoint[0])
        self.rect = self.image.get_rect(center=self.position)

        self.target_waypoint = 1
        self.speed = 2.5
        self.health = health
        self.angle = 0
        self.money_value = 30

        self.animation_speed = 0.1  # Change image every 0.1 seconds
        self.last_switch_time = time.time()  # Time for animation switch

    def update(self):
        """Update the enemy's state: animate, move, and rotate."""
        self.animate()
        self.move()
        self.rotate()

    def animate(self):
        """Animate the jellyfish by switching images at a set interval."""
        current_time = time.time()

        if current_time - self.last_switch_time > self.animation_speed:
            self.last_switch_time = current_time
            # Switch to the next image in the list, cycling back to the start
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.original_image = self.images[self.current_image_index]
            # Készíts egy másolatot az eredeti képről
            self.image = self.original_image.copy()

    def move(self):
        """Move the jellyfish towards the next waypoint."""
        if self.target_waypoint < len(self.waypoint):
            self.target = Vector2(self.waypoint[self.target_waypoint])
            self.movement = self.target - self.position
        else:
            self.kill()
            return  # Kilépünk a függvényből, ha nincs több waypoint

        dist = self.movement.length()

        if dist >= self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.position += self.movement.normalize() * dist
            self.target_waypoint += 1

        self.rect.center = self.position

    def rotate(self):
        """Rotate the jellyfish image to face the direction of movement."""
        if self.target_waypoint < len(self.waypoint):
            dist = self.target - self.position
            self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

            # Rotate the image and update the rectangle
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.position)

    def take_damage(self, amount):
        """Reduce the jellyfish's health by a specified amount."""
        self.health -= amount
        if self.health <= 0:
            self.kill()