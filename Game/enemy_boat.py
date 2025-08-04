import pygame as pg
from pygame.math import Vector2
import math


class Enemy_boat(pg.sprite.Sprite):
    def __init__(self, waypoints, image):
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.position = Vector2(self.waypoints[0])  # lista
        self.target_waypoint = 1  # Next waypoint index
        self.health = 200
        self.speed = 3
        self.angle = 0
        self.money_value = 25

        self.original_image = image
        self.image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        """Update the enemy's state: move and rotate."""

        self.move()
        self.rotate()

    def move(self):
        """Move the enemy towards the next waypoint."""

        # define target waypoints
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.position
        else:
            self.kill()

        # calculate the distance to the target waypoint
        distance = self.movement.length()
        # if the distance is greater than or equal to the speed, move towards the target
        if distance >= self.speed:
            # Normalize: How many pixels to move to left and down
            self.position += self.movement.normalize() * self.speed  # Faster because of speed
        else:
            if distance != 0:
                self.position += self.movement.normalize() * distance
            self.target_waypoint += 1
        self.rect.center = self.position

    def rotate(self):
        """Rotate the enemy image to face the direction of movement."""

        # calculate the distance vector to the target waypoint
        distance = self.target - self.position
        # Calculate the angle in degrees
        self.angle = math.degrees(math.atan2(-distance[1], distance[0]))  # Y axis is inverted in pygame
        # rotate the image and update the rectangle
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def take_damage(self, amount):
        """Reduce the enemy's health by a specified amount."""

        self.health -= amount
        if self.health <= 0:
            self.kill()
