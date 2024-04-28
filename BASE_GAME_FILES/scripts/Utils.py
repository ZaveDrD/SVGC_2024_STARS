import pygame
from Actor import SIM_SCALE, player_zoom

BASE_IMG_PATH = ""


def load_image(path):
    img = pygame.load_image(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def ConvToPixelScale(sim_scale: int) -> int:
    return sim_scale / (SIM_SCALE / player_zoom)


def ConvToSimScale(px_scale: int) -> int:
    return px_scale * (SIM_SCALE / player_zoom)
