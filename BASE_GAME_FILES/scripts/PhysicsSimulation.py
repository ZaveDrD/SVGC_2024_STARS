import math
import pygame

from BASE_GAME_FILES.scripts.Actor import player_view_pos_x, player_view_pos_y, SCALE_MASS_EQUIVALENCE, player_zoom, GRAVITATIONAL_CONSTANT, \
    ticks_btw_calculations, screen


class CelestialBody:
    def __init__(self, color, mass, pos: list[int], velocity: list[float] = [0, 0], acceleration: list[float] = [0, 0],
                 start_force: list[int] = [0, 0], *args):
        # Aesthetic Parameters
        self.color: list[int] = color

        # Physics Parameters (Const)
        self.mass: float = mass

        # Physics Parameters (Varying)
        self.merged = False
        self.store_force_x = start_force[0]
        self.store_force_y = start_force[1]

        self.x: float = pos[0]
        self.y: float = pos[1]

        self.px = None
        self.py = None

        self.ax: float = acceleration[0]
        self.ay: float = acceleration[1]

        self.vx: float = velocity[0]
        self.vy: float = velocity[1]

        self.calc_radius()

    def set_pos(self, pos: list[float]):
        self.x = (math.floor(pos[0]) + player_view_pos_x)
        self.y = (math.floor(pos[1]) + player_view_pos_y)

    def calc_radius(self):
        self.radius = math.sqrt((self.mass / SCALE_MASS_EQUIVALENCE) / math.pi)

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
        return GRAVITATIONAL_CONSTANT * (self.mass * object.mass) / (distance ** 2) / ticks_btw_calculations

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

                object.merged = True
                self.calc_radius()
            else:
                object.mass += self.mass
                object.vx = momentumX / object.mass
                object.vy = momentumY / object.mass

                self.merged = True
                object.calc_radius()

    def display(self):
        if not self.merged:
            self.px = int(self.x) * player_zoom - player_view_pos_x
            self.py = int(self.y) * player_zoom - player_view_pos_y
            pygame.draw.circle(screen, self.color, [self.px, self.py], int(self.radius) * player_zoom)


class PhysicsSim:
    def __init__(self, celestial_objects: list[CelestialBody]):
        self.celestial_bodies = celestial_objects

    def add_object(self, celestial_objects: list[CelestialBody]):
        for obj in celestial_objects:
            self.celestial_bodies.append(obj)

    def remove_object(self, celestial_objects: list[CelestialBody]):
        for obj in celestial_objects:
            self.celestial_bodies.remove(obj)

    def applyForces(self, objects: list[CelestialBody]):
        for x in objects:
            for y in objects:
                if not x.merged and not y.merged and x != y:
                    x.calc_collision_data(y)

        for x in objects:
            x.ax = 0
            x.ay = 0
            x.store_force_x = 0
            x.store_force_y = 0

        for x in objects:
            for y in objects:
                if x != y and not x.merged and not y.merged:
                    x.calc_velocity(y)

        for x in objects:
            x.calc_pos()

        for i in objects:
            i.display()
