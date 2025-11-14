import math
import pygame
from pygame.math import Vector2


class Car:
    def __init__(self, pos: Vector2, color=(70, 130, 255)):
        self.pos = Vector2(pos)
        self.velocity = Vector2(0,0)
        self.angle = 0.0  # degrees
        self.color = color
        self.width = 30
        self.height = 50
        self.mass = 1200.0
        self.radius = max(self.width, self.height) * 0.6
        self.max_speed = 400
        self.acceleration = 700
        self.brake = 900
        self.turn_speed = 200  # degrees per second
        # friction coefficient (applied per second)
        self.friction = 0.12
        self.controller = None

    def reset(self, pos):
        self.pos = Vector2(pos)
        self.velocity = Vector2(0,0)
        self.angle = 0.0

    def update(self, dt, keys=None):
        if self.controller is not None:
            # AI controller handles input
            self.controller.step(dt)
            keys = self.controller.get_inputs()

        forward = Vector2(0, -1).rotate(self.angle)

        def _pressed(k):
            # wrappers returned by pygame.key.get_pressed do not have .get
            try:
                return keys.get(k, False)
            except Exception:
                return keys[k]

        # inputs in keys: up/down/left/right
        accel = 0
        if keys and _pressed(pygame.K_UP):
            accel += 1
        if keys and _pressed(pygame.K_DOWN):
            accel -= 1

        if accel > 0:
            self.velocity += forward * self.acceleration * dt
        elif accel < 0:
            # stronger applied braking
            self.velocity += forward * -self.brake * dt
        else:
            # apply damping proportional to dt
            self.velocity *= max(0.0, 1 - self.friction * dt)

        # clamp speed
        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # turning
        steering = 0
        if keys and _pressed(pygame.K_LEFT):
            steering -= 1
        if keys and _pressed(pygame.K_RIGHT):
            steering += 1

        # reduce steering at low speed
        steer_amount = steering * self.turn_speed * dt * (self.velocity.length() / (self.max_speed / 2 + 1))
        self.angle += steer_amount

        # move
        self.pos += self.velocity * dt

    def collide_with(self, other: "Car"):
        # simple circle-based collision resolution
        delta = other.pos - self.pos
        dist = delta.length()
        min_dist = (self.radius + other.radius)
        if dist == 0:
            # jitter to avoid divide-by-zero
            delta = Vector2(random.random() * 0.01 + 0.01, 0.0)
            dist = delta.length()

        if dist < min_dist:
            # push them apart based on mass
            overlap = min_dist - dist
            n = delta.normalize()
            total_mass = self.mass + other.mass
            self.pos -= n * (overlap * (other.mass / total_mass))
            other.pos += n * (overlap * (self.mass / total_mass))

            # simple velocity exchange along normal (elastic-ish)
            v1 = self.velocity.dot(n)
            v2 = other.velocity.dot(n)
            # 1D elastic collision
            new_v1 = (v1 * (self.mass - other.mass) + 2 * other.mass * v2) / total_mass
            new_v2 = (v2 * (other.mass - self.mass) + 2 * self.mass * v1) / total_mass
            self.velocity += (new_v1 - v1) * n
            other.velocity += (new_v2 - v2) * n

    def draw(self, surface, offset=Vector2(0,0)):
        # draw simple rectangle rotated
        rect_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rect_surf.fill(self.color)
        rotated = pygame.transform.rotate(rect_surf, self.angle)
        r = rotated.get_rect(center=(self.pos + offset))
        surface.blit(rotated, r.topleft)
