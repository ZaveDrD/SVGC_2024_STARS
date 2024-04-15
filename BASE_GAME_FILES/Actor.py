import pygame
import atexit
import sys
import IHatePythonSyntax

########################################################################################################################
#############################################  SIMULATION STUFF  #######################################################
########################################################################################################################

#  CONSTANTS
SIM_SCALE = 10 ** 10 * 3
SCALE_MASS_EQUIVALENCE = SIM_SCALE * 2 ** 18  # SCALE_MASS_EQUIV is a multiple of SIM_SCALE so that SIM_SCALE actually matters

########################################################################################################################
##############################################  PLAYER MOVEMENT  #######################################################
########################################################################################################################

#  CONSTANTS
PLAYER_MOVE_SPEED = 0.5
ZOOM_MULT_INC = 0.001
PLAYER_MIN_ZOOM = 10 ** -10

#  VARIABLES
player_view_pos_x, player_view_pos_y = 0, 0
player_zoom = 1

########################################################################################################################
#####################################################  TIME  ###########################################################
########################################################################################################################

#  CONSTANTS
TICK_SPEED_INC = 1

#  VARIABLES
tick_speed = 60
current_game_time = 0
current_simulated_time = 0
current_tick = 0

########################################################################################################################
################################################  GAME SPECS  ##########################################################
########################################################################################################################

#  CONSTANTS
WIDTH, HEIGHT = 0, 0
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
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode([WIDTH, HEIGHT])


def tick(ticks):  # NEED TO CONVERT WHOLE SYSTEM TO TICKS
    print("CHECK TICK VAL")


def updateMovementParams(keys, A):
    if keys[pygame.K_UP]:
        A.player_view_pos_y += PLAYER_MOVE_SPEED
    if keys[pygame.K_DOWN]:
        A.player_view_pos_y -= PLAYER_MOVE_SPEED
    if keys[pygame.K_LEFT]:
        A.player_view_pos_x += PLAYER_MOVE_SPEED
    if keys[pygame.K_RIGHT]:
        A.player_view_pos_x -= PLAYER_MOVE_SPEED

    if keys[pygame.K_EQUALS]:
        A.player_zoom += ZOOM_MULT_INC
    if keys[pygame.K_MINUS]:
        A.player_zoom = PLAYER_MIN_ZOOM if A.player_zoom - ZOOM_MULT_INC < 0 else A.player_zoom - ZOOM_MULT_INC

    if keys[pygame.K_RIGHTBRACKET]:
        A.tick_speed += TICK_SPEED_INC
    if keys[pygame.K_LEFTBRACKET]:
        A.tick_speed -= TICK_SPEED_INC
