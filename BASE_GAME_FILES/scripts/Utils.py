import pygame
import cv2
import math
import numpy as np
import os
import BASE_GAME_FILES.scripts.Actor as A

BASE_IMG_PATH = ""
Colour = A.pygame.Color


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(A.COLOUR_KEY)
    return img


def ConvToPixelScale(sim_scale: int) -> int:
    return sim_scale / (A.SIM_SCALE / A.player_zoom)


def ConvToSimScale(px_scale: int) -> int:
    return px_scale * (A.SIM_SCALE / A.player_zoom)


def ScaleCoordinateToScreenSize(px: list[float]) -> tuple:
    ratioX = A.game_specs.renderer.layers[0].display.get_size()[0] / A.game_specs.screen.get_size()[0]
    ratioY = A.game_specs.renderer.layers[0].display.get_size()[1] / A.game_specs.screen.get_size()[1]
    return px[0] * ratioX, px[1] * ratioY


def save_warped_img(filename: str):
    img = cv2.imread(filename)

    # set gain
    gain = 1.5

    # set background color
    bgcolor = (0,0,0)

    # get dimensions
    h, w = img.shape[:2]
    xcent = w / 2
    ycent = h / 2
    rad = min(xcent,ycent)

    # set up the x and y maps as float32
    map_x = np.zeros((h, w), np.float32)
    map_y = np.zeros((h, w), np.float32)
    mask = np.zeros((h, w), np.uint8)

    # create map with the spherize distortion formula --- arcsin(r)
    # xcomp = arcsin(r)*x/r; ycomp = arsin(r)*y/r
    for y in range(h):
        Y = (y - ycent)/ycent
        for x in range(w):
            X = (x - xcent)/xcent
            R = math.hypot(X,Y)
            if R == 0:
                map_x[y, x] = x
                map_y[y, x] = y
                mask[y,x] = 255
            elif R > 1:
                map_x[y, x] = x
                map_y[y, x] = y
                mask[y,x] = 0
            elif gain >= 0:
                map_x[y, x] = xcent*X*math.pow((2/math.pi)*(math.asin(R)/R), gain) + xcent
                map_y[y, x] = ycent*Y*math.pow((2/math.pi)*(math.asin(R)/R), gain) + ycent
                mask[y,x] = 255
            elif gain < 0:
                gain2 = -gain
                map_x[y, x] = xcent*X*math.pow((math.sin(math.pi*R/2)/R), gain2) + xcent
                map_y[y, x] = ycent*Y*math.pow((math.sin(math.pi*R/2)/R), gain2) + ycent
                mask[y,x] = 255

    # do the remap  this is where the magic happens
    result = cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101, borderValue=(0, 0, 0))

    # process with mask
    result2 = result.copy()
    result2[mask==0] = bgcolor

    # save results
    cv2.imwrite(os.path.join(BASE_IMG_PATH, (filename[:-4:]+"_spherized.png")), result2)

