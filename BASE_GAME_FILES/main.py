import pygame
import PhysicsSimulation
import atexit
import sys
import Actor as A
import threading
import HandTrackingSim
import math
from typing import Callable
import time

atexit.register(lambda: [pygame.quit(), sys.exit()])

pygame.display.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode([WIDTH, HEIGHT])

A.WIDTH, A.HEIGHT = WIDTH, HEIGHT
hands: list = []

gestures = {
    #   True      ->      Less Than        ->     dist < X
    #   False     ->      Greater Than     ->     dist > X

    'pinch': [
        [[None, 4], [None, 8], 50, True],
        [[None, 3], [None, 7], 40, False]
    ],
    'Finger Gun': [
        [[None, 8], [None, 12], 60, True],
        [[None, 7], [None, 11], 60, True],
        [[None, 12], [None, 16], 150, False],
        [[None, 16], [None, 20], 60, True]
    ],
    'Index Finger Touch': [
        [[0, 8], [1, 8], 60, True]
    ]
    # 'shadowWizardMoneyGang': [
    #     [[0, 8], [1, 8], 40, True],
    #     [[0, 20], [1, 20], 40, True],
    #     [[0, 4], [1, 4], 30, True]
    # ],
}


def detect_vertebraeC6(hands: list[list[list[int]]], params: list[list]) -> list[int]:
    """

    Args:
        hands: (list[list[int]]) The hand
        params: (list[list[[int, int], [int, int], int, bool, ...?]]) An array of requirements which are in the form:

            - [0]: point 1 index
                - [0]: The hand index
                - [1]: The point on the hand
            - [1]: point 2 index
                - [0]: The hand index
                - [1]: The point on the hand
            - [2]: Max/Min distance between the two points
            - [3]: True if max, false if min

    Returns:
        bool - True if the gesture is being done, else false
    """

    handsDoingGesture = []
    None_Banned_Hands = []

    for param in params:  # If ONE parameter is wrong, it's not true for that hand
        param_test_result = True

        if param[0][0] == param[1][0] and param[0][0] is not None:  # If its for only one hand
            if param[0][0] >= len(hands): return []
            if len(hands[param[0][0]]) < 21: return []

            selected_hand = hands[param[0][0]]
            distBtwPoints = abs(math.dist(selected_hand[param[0][1]], selected_hand[param[1][1]]))

            if param[3]:
                result = distBtwPoints < param[2]
            else:
                result = distBtwPoints > param[2]

            if not result: return[]

        if not param[0][0] == param[1][0] and param[0][0] is not None and param[1][0] is not None:
            if param[0][0] >= len(hands) or param[1][0] >= len(hands): return[]
            if len(hands[param[0][0]]) < 21 or len(hands[param[1][0]]) < 21: return[]

            distBtwPoints = abs(math.dist(hands[param[0][0]][param[0][1]], hands[param[1][0]][param[1][1]]))

            if param[3]:
                result = distBtwPoints < param[2]
            else:
                result = distBtwPoints > param[2]

            if not result: return[]

        if param[0][0] is None or param[1][0] is None:
            num_results_true = 0
            for hand_num, hand in enumerate(hands):
                if len(hand) < 21: return[]

                distBtwPoints = abs(math.dist(hand[param[0][1]], hand[param[1][1]]))

                if param[3]:
                    result = distBtwPoints < param[2]
                else:
                    result = distBtwPoints > param[2]

                if result:
                    if hand_num not in handsDoingGesture and hand_num not in None_Banned_Hands:
                        handsDoingGesture.append(hand_num)
                    num_results_true += 1
                else:
                    if hand_num in handsDoingGesture:
                        handsDoingGesture.remove(hand_num)
                    None_Banned_Hands.append(hand_num)

            if num_results_true == 0: return[]

    if len(handsDoingGesture) > 0:
        return handsDoingGesture
    else:
        for param in params:
            if not param[0][0] in handsDoingGesture:
                handsDoingGesture.append(param[0][0])

            if not param[1][0] in handsDoingGesture:
                handsDoingGesture.append(param[1][0])

        return handsDoingGesture


class Hand:
    def __init__(self, landmarks: list[list[int]]):
        self.landmarks = landmarks
        self.gestures = gestures


class Hands:
    def __init__(self, handList: list[Hand]):
        self.handList = handList


def get_hands():
    global hands
    while True:
        hands = HandTrackingSim.get_hands()


threading.Thread(target=get_hands).start()


class CelestialBody:
    def __init__(self, name, color, bodyType, mass, force, acceleration, velocity, pos, *args):
        self.name: str = name
        self.color: list[int] = color
        self.type: str = bodyType
        self.mass: float = mass
        self.force: float = force
        self.acceleration: float = acceleration
        self.velocity: float = velocity
        self.pos: float = pos
        self.x: float = pos[0]
        self.y: float = pos[1]
        self.fx: float = force[0]
        self.fy: float = force[1]
        self.ax = acceleration[0]
        self.ay = acceleration[1]
        self.vx = velocity[0]
        self.vy = velocity[1]

    def display(self):
        # print(f"\n{ self.name = }, { self.x = }, { self.y = }")
        pygame.draw.circle(screen, self.color, center=(
            self.x / A.SIM_SCALE + WIDTH / 2 + A.offsetX, self.y / A.SIM_SCALE + HEIGHT / 2 + A.offsetY),
                           radius=self.mass / A.SCALE_MASS_EQUIVALENCE)

    def calcNewPosition(self):
        deltaT = A.TIME_INC

        self.ax = self.fx / self.mass
        self.ay = self.fy / self.mass

        # acc = deltaV / deltaT ... deltaV = acc * deltaT

        self.vx += self.ax * deltaT
        self.vy += self.ay * deltaT

        # deltaV = deltaX / deltaT ... deltaX = deltaV * deltaT

        self.x += self.vx * deltaT
        self.y += self.vy * deltaT

        # print(f"\n{ self.name = }, \nPOSITIONS: { self.x = }, { self.y = }, \nVELOCITIES: { self.vx = }, { self.vy }, \nACCELERATION: { self.ax }, { self.ay }, \nFORCES: { self.fx = }, { self.fy }")
        self.display()


if __name__ == "__main__":
    initial_celestial_bodies = [
        CelestialBody('SUN 2', [255, 255, 255], "", 2 * 10 ** 30 * 100, [0, 0], [0, 0], [0, 0], [0, 4000000000000]),
        CelestialBody('SUN 1', [0, 0, 0], "", 20 * 10 ** 30, [0, 0], [0, 0], [0, 0], [0, -2000000000000])
    ]

    phys_sim = PhysicsSimulation.PhysicsSim(initial_celestial_bodies)

    while True:
        A.TIME_INC = A.DEFAULT_TIME_INC * A.time_mult
        A.current_time += A.TIME_INC

        A.SIM_SCALE = A.DEFAULT_SIM_SCALE * A.zoom
        A.SCALE_MASS_EQUIVALENCE = A.DEFAULT_SCALE_MASS_EQUIVALENCE * A.zoom

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            A.offsetY += A.moveControlSpeed
        if keys[pygame.K_DOWN]:
            A.offsetY -= A.moveControlSpeed
        if keys[pygame.K_LEFT]:
            A.offsetX += A.moveControlSpeed
        if keys[pygame.K_RIGHT]:
            A.offsetX -= A.moveControlSpeed

        if keys[pygame.K_EQUALS]:
            if A.zoom - A.zoomInc > 0:
                A.zoom -= A.zoomInc
            else:
                A.zoom = 10 ** -10
        if keys[pygame.K_MINUS]:
            A.zoom += A.zoomInc

        if keys[pygame.K_LEFTBRACKET]:
            A.time_mult -= A.TIME_MULT_INC
        if keys[pygame.K_RIGHTBRACKET]:
            A.time_mult += A.TIME_MULT_INC

        screen.fill("#5a82c2")

        for hand in hands:
            for lm in hand:
                # for lm_other in range(0, len(currentFrameHandLandmarks[handNum])):
                #     if lm == 0 and lm_other == (1 or 5 or 9 or 13 or 17):
                #         pygame.draw.line(screen, [255, 255, 255], [currentFrameHandLandmarks[handNum][lm][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm][2] * 3 - HEIGHT / 4], [currentFrameHandLandmarks[handNum][lm_other][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm_other][2] * 3 - HEIGHT / 4], 5)

                pygame.draw.circle(screen, [0, 0, 0], center=(
                    lm[1] * (-WIDTH / 640) + WIDTH,
                    lm[2] * (HEIGHT / 480)), radius=10)

        for gesture in gestures:
            gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
            if len(gesturingHands) > 0:
                print(gesture, "Being Did'd by hands:", gesturingHands)

        phys_sim.applyForces(phys_sim.calc_forces())

        pygame.display.update()
