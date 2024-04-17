import math

import aes.core.para
import pygame
import atexit
import sys
from IHatePythonSyntax import *

########################################################################################################################
#############################################  SIMULATION STUFF  #######################################################
########################################################################################################################

#  CONSTANTS
SIM_SCALE = 10 ** 10 * 3
SCALE_MASS_EQUIVALENCE = 10 ** 11  # this many kg of weight = 1m^2 of size
GRAVITATIONAL_CONSTANT = 6.67408 * (10 ** (-11))

#  UNITS:
#       SIMULATION SCALE : SCALE IN SIM_SCALE, ie. num * SIM_SCALE or num * SCALE_MASS_EQUIVALENCE
#       PIXEL SCALE      : THE SCALE OF THE PIXELS ON THE SCREEN


########################################################################################################################
##############################################  PLAYER MOVEMENT  #######################################################
########################################################################################################################

#  CONSTANTS
PLAYER_MOVE_SPEED = 7.5
ZOOM_MULT_INC = 0.01
PLAYER_MIN_ZOOM = 10 ** -10

#  VARIABLES
player_view_pos_x, player_view_pos_y = 0, 0
player_zoom = 1

########################################################################################################################
#####################################################  TIME  ###########################################################
########################################################################################################################

SIM_TIME_EQUIVALENCE = 1e11
TIME_CHANGE_PER_SECOND = 1
TIME_CHANGE_MULT_CHANGE_RATE = .2

TPS = 60

time_change_mult = 1
ticks_btw_calculations = SIM_TIME_EQUIVALENCE ** (1 / time_change_mult) / TPS  # WORKS BUT IS A BIT CHEATY, JUST DIVIDES THE FORCES TO APPEAR AS IF SLOWER

sim_time = 0
game_time = 0

########################################################################################################################
################################################  GAME SPECS  ##########################################################
########################################################################################################################

#  CONSTANTS
TRIPPY_MODE = False

atexit.register(lambda: [pygame.quit(), sys.exit()])

gestures = {
    #   True      ->      Less Than        ->     dist < X
    #   False     ->      Greater Than     ->     dist > X

    'Pinch': [
        [[None, 4], [None, 8], 50, True],
        [[None, 3], [None, 7], 40, False]
    ],
    'Finger Gun': [
        [[None, 8], [None, 12], 60, True],
        [[None, 7], [None, 11], 60, True],
        [[None, 12], [None, 16], 150, False],
        [[None, 16], [None, 20], 60, True]
    ],
    'Summon Small Planet': [
        [[None, 4], [None, 12], 50, True],
        [[None, 3], [None, 11], 40, False],
        [[None, 8], [None, 10], 60, False]
    ],
    # 'shadowWizardMoneyGang': [
    #     [[0, 8], [1, 8], 40, True],
    #     [[0, 20], [1, 20], 40, True],
    #     [[0, 4], [1, 4], 30, True]
    # ],
}

motion_gestures = {
    'OuiOuiMonAmiJeMapeleLafayette': [
        [[]],
        [gestures['Pinch'], None, None],
        [gestures['Pinch'], [0, 100, [None, 0]], [0.2, 1.4]]
        # [GESTURE, [OFFSET_X, OFFSET_Y, [HAND, LANDMARK]] (NONE -> START POSITION), [MIN_TIME, MAX_TIME] (NONE -> START)]
    ]
}

pygame.display.init()
SIZE = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()


def updateMovementParams(keys, A):
    if keys[pygame.K_UP]:
        A.player_view_pos_y -= PLAYER_MOVE_SPEED
    if keys[pygame.K_DOWN]:
        A.player_view_pos_y += PLAYER_MOVE_SPEED
    if keys[pygame.K_LEFT]:
        A.player_view_pos_x -= PLAYER_MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        A.player_view_pos_x += PLAYER_MOVE_SPEED

    if keys[pygame.K_EQUALS]:
        A.player_zoom += ZOOM_MULT_INC
    if keys[pygame.K_MINUS]:
        A.player_zoom = PLAYER_MIN_ZOOM if A.player_zoom - ZOOM_MULT_INC < 0 else A.player_zoom - ZOOM_MULT_INC

    if keys[pygame.K_RIGHTBRACKET]:
        A.time_change_mult += TIME_CHANGE_MULT_CHANGE_RATE
    if keys[pygame.K_LEFTBRACKET]:
        A.time_change_mult -= TIME_CHANGE_MULT_CHANGE_RATE

    if A.time_change_mult == 0:
        A.ticks_btw_calculations = 0.01
    else:
        A.ticks_btw_calculations = SIM_TIME_EQUIVALENCE ** (1 / A.time_change_mult) / TPS


def ConvToPixelScale(sim_scale: int) -> int:
    return sim_scale / (SIM_SCALE / player_zoom)


def ConvToSimScale(px_scale: int) -> int:
    return px_scale * (SIM_SCALE / player_zoom)
