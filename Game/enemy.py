import pygame as pg
from pygame.math import Vector2
import math
import time
import random



class Enemy(pg.sprite.Sprite):
    """The Enemy class represents a generic enemy in the game."""

    def __init__(self, waypoint, image1, image2, health=100): #Two images for the fishes
        """Initialize the enemy with waypoints, images, and health."""

        pg.sprite.Sprite.__init__(self)
        self.waypoint = waypoint
        self.position = Vector2(self.waypoint[0])
        self.target_waypoint = 1
        self.speed = 1.5
        self.health = health
        self.angle = 0
        self.money_value = 10

        # Randomly choose between two sizes
        self.is_big = random.choice([True, False])

        #Size and health adjustments based on the size
        # If the enemy is big, it has more health and a larger scale
        # If the enemy is small, it has less health and a normal scale
        if self.is_big:
            self.scale = 1.5  # Bigger size
            self.health = 150  # More health
        else:
            self.scale = 1.0  # Normal size
            self.health = 100  #Basic health

        # Picture scaling
        # Scale the images based on the chosen size
        self.original_image1 = pg.transform.scale_by(image1, self.scale)
        self.original_image2 = pg.transform.scale_by(image2, self.scale)

        self.current_image = self.original_image1
        self.original = self.current_image
        self.image = pg.transform.rotate(self.original, self.angle)

        # Animation attributes
        # It switches once every second
        self.animation_speed = 1
        self.last_switch_time = time.time()

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        """Update the enemy's state: animate, move, and rotate."""

        self.animate()
        self.move()
        self.rotate()

    def animate(self):
        """Animate the enemy by switching images at a set interval."""


        current_time = time.time() # Get the current time in seconds
        #If more than one second has passed since the last image change
        if current_time - self.last_switch_time > self.animation_speed:
            self.last_switch_time = current_time
            # Switch between the two images
            if self.current_image == self.original_image1:
                self.current_image = self.original_image2
            else:
                self.current_image = self.original_image1
            # Update the image to the current image
            self.original = self.current_image

    def move(self):
        """Move the enemy towards the next waypoint."""

        # If it has already reached the last waypoint, we remove it; otherwise, we calculate a direction vector.
        if self.target_waypoint < len(self.waypoint):
            # Define target waypoints->target is the next waypoint
            self.target = Vector2(self.waypoint[self.target_waypoint])
            # Direction vector from current position to target
            self.movement = self.target - self.position  #From where to where

        else:
            # If the enemy has reached the end of the path, we remove it
            self.kill()

        # calculate the distance to the target waypoint
        dist = self.movement.length()

        # Check if there is enough distance left to move
        # If the distance is greater than or equal to the speed, move towards the target
        if dist >= self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            # error check
            if dist != 0:
                self.position += self.movement.normalize() * dist
            # If the enemy has reached the target waypoint, move to the next one
            self.target_waypoint += 1

    def rotate(self):
        """Rotate the enemy image to face the direction of movement."""

        dist = self.target - self.position
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # rotate image and update rectangle
        self.image = pg.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def take_damage(self, amount):
        """Reduce the enemy's health by a specified amount."""

        self.health -= amount
        if self.health <= 0:
            self.kill()
