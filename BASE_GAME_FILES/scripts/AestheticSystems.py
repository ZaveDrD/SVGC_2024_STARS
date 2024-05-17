import math
import pygame
import random
from PygameShader import *

import BASE_GAME_FILES.scripts.Actor as A


def generateBackgroundStars(numBodies: int, min_x: int = -5000, max_x: int = 5000, min_y: int = -5000, max_y: int = 5000,
                  color: list[int] = [255, 255, 255]):
    stars = []
    for i in range(0, numBodies):
        stars.append(BackgroundObject(color, (random.randint(3, 8)) * 10 ** (random.randint(11, 12)),
                                               [random.randint(min_x, max_x), random.randint(min_y, max_y)]))
    return stars


class BackgroundObject:
    def __init__(self, color, mass, pos: list[float], *args):
        self.color = color
        self.mass = mass
        self.x = pos[0]
        self.y = pos[1]
        self.px = None
        self.py = None
        self.radius = None
        self.calc_radius()

    def calc_radius(self):
        self.radius = math.sqrt((self.mass / A.SCALE_MASS_EQUIVALENCE) / math.pi)

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

    def display(self):
        (self.px, self.py) = self.conv_x_to_px(self.x, self.y)
        pygame.draw.circle(A.game_specs.display, self.color, [self.px, self.py],
                           int(self.radius) * A.player_zoom)


class BackgroundRenderer:
    def __init__(self, objects: list[BackgroundObject], background_color):
        self.background_color = background_color
        self.objects = objects

    def render_background(self):
        A.game_specs.display.fill(self.background_color)

    def render_background_objects(self):
        for obj in self.objects:
            obj.display()


class PostProcessing_Renderer:
    def __init__(self, mainSurf: pygame.surface, effects: list[str]):
        self.effect_list = effects
        self.mainSurf = mainSurf

    @staticmethod
    def renderEffectToSurface(surface, effects: list[str], rep='SURFACE'):
        for effect in effects:
            effect = effect.replace(rep, "surface")
            eval(effect)  # IK ITS BAD IM TIRED

    def RenderEffects(self):
        self.renderEffectToSurface(self.mainSurf, self.effect_list)
