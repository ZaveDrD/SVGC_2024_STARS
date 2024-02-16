import HandTrackingSim as hsm

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

handPositions = hsm.handPositions
