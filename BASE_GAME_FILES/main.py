import pygame
import PhysicsSimulation
import atexit
import sys
import Actor as A
import threading
import HandTrackingSim
from typing import Callable
import time

atexit.register(lambda: [pygame.quit(), sys.exit()])

pygame.display.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode([WIDTH, HEIGHT])

A.WIDTH, A.HEIGHT = WIDTH, HEIGHT
hands: list = []


class Gesture:
    def __init__(self, name, detector: Callable[[list[list[list[float]]]], bool | int]) -> None:
        self.name = name
        self.detector = detector

        self.duration = 0
        self.gestureStart = None

    def __resetGesture(self):
        self.duration = 0

    def detect(self, hands: list[list[list[int]]]) -> bool | int:
        active = self.detector(hands)
        if not active:
            self.__resetGesture()
        else:
            if not self.gestureStart:
                self.gestureStart = time.time()
            self.duration = time.time() - self.gestureStart
        return active


class Hand:
    def __init__(self, landmarks: list[list[int]], gestures: list[Gesture]):
        self.landmarks = landmarks
        self.gestures = gestures

    def CheckGestures(self):
        for gesture in self.gestures:
            gesture.detect([self.landmarks])


class Hands:
    def __init__(self, handList: list[Hand], twoHandGestures: list[Gesture]):
        self.handList = handList
        self.twoHandGestures = twoHandGestures


# hands = [Hand()]


def get_hands():
    global hands
    while True:
        hands = HandTrackingSim.get_hands()
        print(f"{hands = }")


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

        phys_sim.applyForces(phys_sim.calc_forces())

        pygame.display.update()
