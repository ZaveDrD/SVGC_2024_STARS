# import HandTrackingSim as hsm
import pygame
import atexit
import sys
import IHatePythonSyntax


DEFAULT_SIM_SCALE = 10 ** 10 * 3
DEFAULT_SCALE_MASS_EQUIVALENCE = 10 ** 28 * 150

WIDTH, HEIGHT = 0, 0

SIM_SCALE = DEFAULT_SIM_SCALE
SCALE_MASS_EQUIVALENCE = DEFAULT_SCALE_MASS_EQUIVALENCE

offsetX, offsetY = 0, 0
moveControlSpeed = 0.5

zoom = 1
zoomInc = 1 * 10 ** -3

current_time = 0
DEFAULT_TIME_INC = 1 * 10 ** 17

TIME_INC = DEFAULT_TIME_INC
time_mult = 1
TIME_MULT_INC = 10 ** -2

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
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# handPositions = hsm.handPositions
