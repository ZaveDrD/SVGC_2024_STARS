import math
import numpy as np
from typing import Type
import Actor as A
from IHatePythonSyntax import *


class CelestialBody:
    def __init__(self, color, mass, pos, *args):
        # Aesthetic Parameters
        self.color: list[int] = color

        # Physics Parameters (Const)
        self.mass: float = mass

        # Physics Parameters (Varying)
        self.merged = False
        self.store_force_x = 0
        self.store_force_y = 0

        self.x: float = pos[0]
        self.y: float = pos[1]

        self.ax = 0
        self.ay = 0

        self.vx = 0
        self.vy = 0

        self.calc_radius()

    def calc_radius(self):
        self.radius = math.sqrt((self.mass / A.SCALE_MASS_EQUIVALENCE) / math.pi)

    def calc_pos(self):
        self.x += self.vx
        self.y += self.vy

    def calc_velocity(self, object):
        angle = self.calc_angle(object)
        force = self.calc_force(object)
        fx = force * math.cos(angle)
        fy = force * math.sin(angle)

        self.store_force_x += fx
        self.store_force_y += fy

        self.ax = fx / self.mass
        self.ay = fy / self.mass

        self.vx += self.ax
        self.vy += self.ay

    def calc_angle(self, object):
        difX, difY = object.x - self.x, object.y - self.y

        angle = math.atan(difY / difX) if difX != 0 else 0
        if difX < 0: angle += math.pi

        return angle

    def calc_force(self, object):
        distance = math.sqrt((self.x - object.x) ** 2 + (self.y - object.y) ** 2)
        return A.GRAVITATIONAL_CONSTANT * (self.mass * object.mass) / (distance ** 2)

    def calc_collision_data(self, object):
        difX, difY = object.x - self.x, object.y - self.y
        pos = math.sqrt(difX ** 2 + difY ** 2)

        if pos <= (self.radius + object.radius):
            momentumX = self.mass * self.vx + object.mass * object.vx
            momentumY = self.mass * self.vy + object.mass * object.vy

            if self.mass > object.mass:
                self.mass += object.mass
                self.vx = momentumX / self.mass
                self.vy = momentumY / self.mass

                object.merged = true
                self.calc_radius()
            else:
                object.mass += self.mass
                object.vx = momentumX / object.mass
                object.vy = momentumY / object.mass

                self.merged = true
                object.calc_radius()

    def display(self):
        if not self.merged:
            A.pygame.draw.circle(A.screen, self.color, [int(self.position_x), int(self.position_y)], int(self.radius))


class PhysicsSim:
    def __init__(self, celestial_objects: list[CelestialBody]):
        self.celestial_bodies = celestial_objects

    def add_object(self, celestial_objects: list[CelestialBody]):
        self.celestial_bodies.append(celestial_objects)

    def remove_object(self, celestial_objects: list[CelestialBody]):
        self.celestial_bodies.remove(celestial_objects)


            
