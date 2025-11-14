import random
import pygame
from pygame.math import Vector2


class AIController:
    def __init__(self, car, world):
        self.car = car
        self.world = world
        # generate waypoints in a circle nearby
        self.waypoints = []
        cx, cy = car.pos
        for i in range(12):
            angle = i * 360 / 12
            offset = Vector2(1, 0).rotate(angle) * (300 + random.randint(-60, 60))
            self.waypoints.append(Vector2(cx, cy) + offset)
        self.current = 0
        self.tolerance = 40
        self.inputs = set()

    def step(self, dt):
        target = self.waypoints[self.current]
        dir_vec = (target - self.car.pos)
        dist = dir_vec.length()
        if dist < self.tolerance:
            self.current = (self.current + 1) % len(self.waypoints)
            target = self.waypoints[self.current]
            dir_vec = (target - self.car.pos)

        # desired angle
        desired_angle = -dir_vec.angle_to(Vector2(0, -1))
        # difference
        diff = (desired_angle - self.car.angle + 180) % 360 - 180

        self.inputs.clear()
        # turn
        if diff < -5:
            self.inputs.add('left')
        elif diff > 5:
            self.inputs.add('right')

        # throttle
        if abs(diff) < 60:
            self.inputs.add('throttle')

    def get_inputs(self):
        # Return a sequence of booleans compatible with pygame.key.get_pressed()
        # We'll return a list of size 512 so it can be indexed by pygame constants.
        # Use a dict mapping pygame key constants to booleans so indexing
        # does not require a large list and is safer for large key codes.
        fake = {}
        if 'throttle' in self.inputs:
            fake[pygame.K_UP] = True
        if 'left' in self.inputs:
            fake[pygame.K_LEFT] = True
        if 'right' in self.inputs:
            fake[pygame.K_RIGHT] = True
        # Also provide an object compatible with pygame.key.get_pressed() lookup
        # The code in `Car` calls keys.get(k, False) which works with dicts.
        return fake
