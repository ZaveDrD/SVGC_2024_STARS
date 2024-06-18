import pygame
import atexit
import sys

import BASE_GAME_FILES.scripts.Renderer as RenderModule

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

#  VARIABLES
player_view_pos_x, player_view_pos_y = 0, 0
player_zoom = 1
player_zoom_max_min = [0.25, 5]


def updateMovementParams(keys, A):
    if keys[pygame.K_UP]:
        A.player_view_pos_y -= PLAYER_MOVE_SPEED / A.player_zoom
    if keys[pygame.K_DOWN]:
        A.player_view_pos_y += PLAYER_MOVE_SPEED / A.player_zoom
    if keys[pygame.K_LEFT]:
        A.player_view_pos_x -= PLAYER_MOVE_SPEED / A.player_zoom
    if keys[pygame.K_RIGHT]:
        A.player_view_pos_x += PLAYER_MOVE_SPEED / A.player_zoom

    if keys[pygame.K_EQUALS]:
        A.player_zoom = A.player_zoom_max_min[1] if A.player_zoom + ZOOM_MULT_INC > A.player_zoom_max_min[1] else A.player_zoom + ZOOM_MULT_INC
    if keys[pygame.K_MINUS]:
        A.player_zoom = A.player_zoom_max_min[0] if A.player_zoom - ZOOM_MULT_INC < A.player_zoom_max_min[0] else A.player_zoom - ZOOM_MULT_INC

    if keys[pygame.K_RIGHTBRACKET]:
        A.time_change_mult += TIME_CHANGE_MULT_CHANGE_RATE
    if keys[pygame.K_LEFTBRACKET]:
        A.time_change_mult -= TIME_CHANGE_MULT_CHANGE_RATE

    if A.time_change_mult <= 0:
        A.ticks_btw_calculations = 0
    else:
        A.ticks_btw_calculations = SIM_TIME_EQUIVALENCE ** (1 / A.time_change_mult) / TPS


def updateCurrentLevel(keys, levelLoader) -> tuple:
    hasChanged = False
    if keys[pygame.K_PERIOD]:
        if levelLoader.currentLevelIndex + 1 < len(levelLoader.levels):
            levelLoader.load_level_index(levelLoader.currentLevelIndex + 1, SAVE_LEVELS)
            hasChanged = True
    elif keys[pygame.K_COMMA]:
        if levelLoader.currentLevelIndex - 1 >= 0:
            levelLoader.load_level_index(levelLoader.currentLevelIndex - 1, SAVE_LEVELS)
            hasChanged = True
    return hasChanged, levelLoader.currentLevelPhysSim


########################################################################################################################
#####################################################  TIME  ###########################################################
########################################################################################################################

SIM_TIME_EQUIVALENCE = 1e11
TIME_CHANGE_PER_SECOND = 1
TIME_CHANGE_MULT_CHANGE_RATE = .2

TPS = 60

time_change_mult = 1
ticks_btw_calculations = SIM_TIME_EQUIVALENCE ** (
            1 / time_change_mult) / TPS  # WORKS BUT IS A BIT CHEATY, JUST DIVIDES THE FORCES TO APPEAR AS IF SLOWER

sim_time = 0
game_time = 0

########################################################################################################################
################################################  GAME SPECS  ##########################################################
########################################################################################################################

#  VARIABLES
selected_level = 0

atexit.register(lambda: [pygame.quit(), sys.exit()])

########################################################################################################################
############################################  HAND-TRACKING STUFF  #####################################################
########################################################################################################################

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

########################################################################################################################
################################################  AESTHETICS  ##########################################################
########################################################################################################################

USE_POST_PROCESSING = True
NUM_LAYERS: int = 5
UI_LAYERS: int = 5

initial_art_generation = {
    "Planet": 15,
    "Meteor": 0,
    "Star": 10,
    "Black_Hole": 1
}

global_post_processing_effects = [
    #  USE 'SURFACE' IN PLACE OF WHERE 'A.game_specs.display' WOULD USUALLY BE
    "shader_bloom_fast1(SURFACE, smooth_=5, threshold_=240, flag_=pygame.BLEND_RGB_ADD, saturation_=True)",
    "pixelation(SURFACE)"
]


########################################################################################################################
################################################  GAME SETUP  ##########################################################
########################################################################################################################

BACKGROUND_COLOR = (0, 0, 0, 255)
COLOUR_KEY = (0, 0, 0)

SAVE_LEVELS = False


class Mouse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def set_mouse_pos(self, x, y):
        self.x, self.y = x, y


mouse = Mouse(0, 0)


class GameSpecs:
    def __init__(self):
        pygame.init()

        self.SIZE = pygame.display.get_desktop_sizes()[0][0] - 25, pygame.display.get_desktop_sizes()[0][1] - 75

        pygame.display.set_caption("SVGC 2024 - Stars")
        self.screen = pygame.display.set_mode(self.SIZE)

        self.renderer: RenderModule.Renderer = RenderModule.Renderer(NUM_LAYERS, global_post_processing_effects, self, USE_POST_PROCESSING)
        self.UI_renderer: RenderModule.Renderer = RenderModule.Renderer(UI_LAYERS, [], self, False)

        self.clock = pygame.time.Clock()


game_specs: GameSpecs = None
