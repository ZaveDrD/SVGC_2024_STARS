import math
import pygame

import BASE_GAME_FILES.scripts.Actor as A


class CelestialBody:
    def __init__(self, color, mass, pos: list[float], velocity: list[float] = [0, 0], acceleration: list[float] = [0, 0],
                 start_force: list[int] = [0, 0], static=False, interaction=True, *args):
        # Aesthetic Parameters
        self.color: list[int] = color

        # Physics Parameters (Const)
        self.mass: float = mass
        self.collision = True
        self.static = static
        self.interaction = interaction

        # Physics Parameters (Varying)
        self.merged = False
        self.merged_to = None

        self.store_force_x = start_force[0]
        self.store_force_y = start_force[1]

        self.x: float = pos[0]
        self.y: float = pos[1]

        self.px = self.x
        self.py = self.y

        self.ax: float = acceleration[0]
        self.ay: float = acceleration[1]

        self.vx: float = velocity[0]
        self.vy: float = velocity[1]

        self.radius = None
        self.calc_radius()

    def set_pos_px(self, pos: list[float]):
        self.x, self.y = self.conv_px_to_x(math.ceil(pos[0]), math.ceil(pos[1]))
        self.display()

    def set_pos(self, pos: list[float]):
        self.x, self.y = pos[0], pos[1]
        self.display()

    def calc_radius(self):
        self.radius = math.sqrt((self.mass / A.SCALE_MASS_EQUIVALENCE) / math.pi)

    def calc_pos(self):
        self.x += self.vx
        self.y += self.vy

    def predict_pos(self, pos, v) -> tuple:
        x, y, vx, vy = pos[0], pos[1], v[0], v[1]
        x += vx
        y += vy
        return x, y

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

    def predict_velocity(self, store_force, a, v, object) -> tuple:
        vx, vy = v[0], v[1]
        ax, ay = a[0], a[1]

        angle = self.calc_angle(object)
        force = self.predict_force(object)
        fx = force * math.cos(angle)
        fy = force * math.sin(angle)

        store_force[0] += fx
        store_force[1] += fy

        ax = fx / self.mass
        ay = fy / self.mass

        vx += ax
        vy += ay

        return vx, vy

    @staticmethod
    def conv_x_to_px(x, y) -> tuple:
        body_pos = [int(x), int(y)]

        screenCentreOffset = [A.game_specs.SIZE[0] / 4, A.game_specs.SIZE[1] / 4]

        screen_centre_pos = [(screenCentreOffset[0] + A.player_view_pos_x),
                             (screenCentreOffset[1] + A.player_view_pos_y)]

        distance = [body_pos[0] - screen_centre_pos[0], body_pos[1] - screen_centre_pos[1]]

        px = A.player_zoom * distance[0] + screenCentreOffset[0]
        py = A.player_zoom * distance[1] + screenCentreOffset[1]

        # print("CONV X -> PX:\nx:", x, ":", px, "\ny:", y, ":", py)

        return px, py

    @staticmethod
    def conv_px_to_x(px, py) -> tuple:
        screenCentreOffset = [A.game_specs.SIZE[0] / 4, A.game_specs.SIZE[1] / 4]

        screen_centre_pos = [(screenCentreOffset[0] + A.player_view_pos_x),
                             (screenCentreOffset[1] + A.player_view_pos_y)]

        x = (px + A.player_zoom * (screen_centre_pos[0]) - screenCentreOffset[0]) / A.player_zoom
        y = (py + A.player_zoom * (screen_centre_pos[1]) - screenCentreOffset[1]) / A.player_zoom

        return x, y

    def calc_angle(self, object):
        difX, difY = object.x - self.x, object.y - self.y

        angle = math.atan(difY / difX) if difX != 0 else 0
        if difX < 0: angle += math.pi

        return angle

    def calc_force(self, object):
        distance = math.sqrt((self.x - object.x) ** 2 + (self.y - object.y) ** 2)
        return A.GRAVITATIONAL_CONSTANT * (self.mass * object.mass) / (distance ** 2) / A.ticks_btw_calculations

    def predict_force(self, object):
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

                object.merged = True
                object.merged_to = self

                self.calc_radius()
            else:
                object.mass += self.mass
                object.vx = momentumX / object.mass
                object.vy = momentumY / object.mass

                self.merged = True
                self.merged_to = object

                object.calc_radius()

    def display(self):
        if not self.merged:
            (self.px, self.py) = self.conv_x_to_px(self.x, self.y)
            pygame.draw.circle(A.game_specs.renderer.layers[0].display, self.color, [self.px, self.py], int(self.radius) * A.player_zoom)


class Planet(CelestialBody):
    def __init__(self, color, mass, pos: list[float], velocity: list[float] = [0, 0], acceleration: list[float] = [0, 0],
                 start_force: list[int] = [0, 0], static=False, interaction=True,  *args):
        super().__init__(color, mass, pos, velocity, acceleration, start_force, static, interaction)


class Spacecraft(CelestialBody):
    def __init__(self, color, mass, pos: list[float], velocity: list[float] = [0, 0], acceleration: list[float] = [0, 0],
                 start_force: list[int] = [0, 0], static=False, interaction=True,  *args):
        super().__init__(color, mass, pos, velocity, acceleration, start_force, static, interaction)


class GravitationField(CelestialBody):
    def __init__(self, color, mass, pos: list[float], velocity: list[float] = [0, 0], acceleration: list[float] = [0, 0],
                 start_force: list[int] = [0, 0], static=False, interaction=True,  *args):
        super().__init__(color, mass, pos, velocity, acceleration, start_force, static, interaction)
        self.collision = False


class PhysicsSim:
    def __init__(self, celestial_objects: list[CelestialBody]):
        self.celestial_bodies: list[CelestialBody] = celestial_objects

    def add_object(self, celestial_objects: list[CelestialBody]):
        for obj in celestial_objects:
            self.celestial_bodies.append(obj)

    def remove_object(self, celestial_objects: list[CelestialBody]):
        for obj in celestial_objects:
            self.celestial_bodies.remove(obj)

    @staticmethod
    def applyForces(objects: list[CelestialBody]):
        for x in objects:
            for y in objects:
                if not x.merged and not y.merged and x != y and x.collision and y.collision:
                    x.calc_collision_data(y)

        for x in objects:
            if not x.static:
                x.ax = 0
                x.ay = 0
                x.store_force_x = 0
                x.store_force_y = 0

        for x in objects:
            for y in objects:
                if x != y and not x.merged and not y.merged and not x.static and not y.static:
                    x.calc_velocity(y)

        for x in objects:
            if not x.static:
                x.calc_pos()

        for i in objects:
            i.display()

    def predict_path(self, body: CelestialBody, v, pos) -> tuple:
        ax = 0
        ay = 0
        store_force_x = 0
        store_force_y = 0

        vx, vy = v[0], v[1]
        x, y = pos[0], pos[1]

        for other_body in self.celestial_bodies:
            if other_body != body and not body.merged and not other_body.merged:
                vx, vy = body.predict_velocity([store_force_x, store_force_y], [ax, ay], [vx, vy], other_body)

        x, y = body.predict_pos([x, y], [vx, vy])

        return x, y, vx, vy
