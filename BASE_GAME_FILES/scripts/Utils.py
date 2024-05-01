import pygame
import BASE_GAME_FILES.scripts.Actor as A

BASE_IMG_PATH = ""


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(A.COLOUR_KEY)
    return img


def ConvToPixelScale(sim_scale: int) -> int:
    return sim_scale / (A.SIM_SCALE / A.player_zoom)


def ConvToSimScale(px_scale: int) -> int:
    return px_scale * (A.SIM_SCALE / A.player_zoom)
