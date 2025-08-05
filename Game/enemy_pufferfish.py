import pygame as pg
from pygame.math import Vector2
import math
import time



class Enemy_pufferfish(pg.sprite.Sprite):
    """The Enemy_pufferfish class represents a pufferfish enemy in the game."""

    def __init__(self, waypoint, image1, image2, health=100):
        """Initialize the pufferfish with waypoints, images, and health."""

        pg.sprite.Sprite.__init__(self)
        self.waypoint = waypoint
        self.position = Vector2(self.waypoint[0]) #The first waypoint
        self.target_waypoint = 1 # Next waypoint index
        self.speed = 2 #Speed of the pufferfish
        self.health = health
        self.angle = 0 # Angle for rotation
        self.money_value = 20  # Money value for the pufferfish

        self.original_image1 = image1
        self.original_image2 = image2

        self.animation_speed = 1 # Change image every second
        self.last_switch_time = time.time() # Time for animation switch


        self.current_image = self.original_image1 # Start with the first image
        self.image = self.current_image # Set the initial image

        self.original = self.current_image # Store the original image for rotation

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        """Update the enemy's state: animate, move, and rotate."""

        self.animate()
        self.move()
        self.rotate()

    def animate(self):
        """Animate the pufferfish by switching images at a set interval."""

        #Timing of slide transitions
        current_time = time.time()
        # If more than animation_speed seconds have passed since the last switch
        # This allows for a smooth animation effect
        # If more than 1 second has passed since the last switch
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
        """Move the pufferfish towards the next waypoint."""
        # Define target waypoints
        # If the target waypoint is within the list of waypoints
        if self.target_waypoint < len(self.waypoint):
            # Set the target to the next waypoint
            self.target = Vector2(self.waypoint[self.target_waypoint])  # list
            # Calculate the movement vector from current position to target
            self.movement = self.target - self.position  # From where to where
        else:
            # If the enemy has reached the end of the path
            self.kill()

        # Calculate the distance to the target, so it doesn't get stuck
        dist = self.movement.length()

        # Check if there is enough distance left to move
        if dist >= self.speed:
            self.position += self.movement.normalize() * self.speed
        else:
            # error check
            if dist != 0:
                self.position += self.movement.normalize() * dist
            # If the enemy has reached the target waypoint, move to the next one
            self.target_waypoint += 1

    def rotate(self):
        """Rotate the pufferfish image to face the direction of movement."""

        dist = self.target - self.position # Calculate the distance vector to the target waypoint
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))
        # rotate image and update rectangle
        self.image = pg.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def take_damage(self, amount):
        """Reduce the pufferfish's health by a specified amount."""

        self.health -= amount
        if self.health <= 0:
            self.kill()
