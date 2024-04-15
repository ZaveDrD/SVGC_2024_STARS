import random
import pygame
from PhysicsSimulation import *
import sys
import Actor as A
import threading
import HandTrackingSim
import math
from GestureTrackingSim import *
import IHatePythonSyntax
import time

hands: list = []


def calcScreenSpaceLandmarks(landmarks: list[list[int]]) -> list[list[int]]:
    new_hand_lm = []
    for lm in landmarks:
        new_hand_lm.append([lm[0], lm[1] * (-A.WIDTH / 640) + A.WIDTH, lm[2] * (A.HEIGHT / 480), lm[3]])
    return new_hand_lm


def convertCamHandsToScreenSpaceHands(hands: list[list[list[int]]]) -> list[list[list[int]]]:
    new_hand_list = []
    for hand in hands:
        new_hand_list.append(calcScreenSpaceLandmarks(hand))
    return new_hand_list


class Hand:

    def __init__(self, landmarks: list[list[int]]):
        self.landmarks = landmarks
        self.screenSpace_lm = calcScreenSpaceLandmarks(landmarks)
        self.gestures = A.gestures


class Hands:
    def __init__(self, handList: list[Hand]):
        self.handList = handList


def get_hands():
    global hands
    while True:
        hands = HandTrackingSim.get_hands()
        # hands = Hands(hands_raw)


threading.Thread(target=get_hands).start()

if __name__ == "__main__":
    initial_celestial_bodies = [
        CelestialBody('SUN 2', [255, 255, 255], "", 2e30 * 100, [0, 0], [0, 0], [0, 0],
                      [25000000000000, 12000000000000])
        # CelestialBody('SUN 2', [255, 255, 255], "", 2e30 * 100, [0, 0], [0, 0], [0, 0], [0, 4000000000000])
        # CelestialBody('SUN 1', [0, 0, 0], "", 2e30, [0, 0], [0, 0], [15e-10, 0], [0, -2000000000000]),
    ]

    phys_sim = PhysicsSim(initial_celestial_bodies)

    while True:
        # Closes the application on quit
        for event in A.pygame.event.get():
            if event.type == A.pygame.QUIT:
                A.pygame.quit()
                sys.exit()

        keys = A.pygame.key.get_pressed()
        A.updateMovementParams(keys, A)

        if not A.trippy_mode: A.screen.fill("#5a82c2")

        for hand in convertCamHandsToScreenSpaceHands(hands):
            for lm in hand:
                A.pygame.draw.circle(A.screen, [0, 0, 0], center=(lm[1], lm[2]), radius=10)

        # for gesture in gestures:
        #     gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
        #     if len(gesturingHands) > 0:
        #         print(gesture, "Being Did'd by hands:", gesturingHands)

        pinchingHands = detect_vertebraeC6(convertCamHandsToScreenSpaceHands(hands), A.gestures['Pinch'])
        if len(pinchingHands) > 0:
            for planetaryBody in initial_celestial_bodies:  # PINCH DETECTION TO GRAB PLANETS

                for hand in pinchingHands:
                    if hand is None: break
                    if hand >= len(hands): break

                    pinchingHand = calcScreenSpaceLandmarks(hands[hand])
                    landmarkCoord = [pinchingHand[A.gestures['Pinch'][0][0][1]][1],
                                     pinchingHand[A.gestures['Pinch'][0][0][1]][2]]

                    plantPos = [planetaryBody.screenX, planetaryBody.screenY]

                    # print(abs(math.dist(landmarkCoord, plantPos)))
                    # print("Planet Pos", plantPos, "\n", "Landmark Pos", landmarkCoord)

                    if abs(math.dist(landmarkCoord, plantPos)) <= planetaryBody.mass / A.SCALE_MASS_EQUIVALENCE:
                        planetaryBody.updatePlanetPosition_ScreenSpace(landmarkCoord[0], landmarkCoord[1])

        planetSummoningHands = detect_vertebraeC6(convertCamHandsToScreenSpaceHands(hands), A.gestures['Summon Small Planet'])
        if len(planetSummoningHands) > 0:
            for planetaryBody in initial_celestial_bodies:  # SUMMON PLANETS
                for hand in planetSummoningHands:
                    if hand is None: break
                    if hand >= len(hands): break

                    summoningHand = calcScreenSpaceLandmarks(hands[hand])
                    print(summoningHand[9][0], summoningHand[12][0])
                    landmarkCoord = [(summoningHand[9][1] + summoningHand[12][1]) / 2,
                                     (summoningHand[9][2] + summoningHand[12][2]) / 2]
                    # print(f"{landmarkCoord = }")

                    planetPosPadding = 50

                    canPlaceBody = True

                    for body in phys_sim.sadstuff:
                        # print(f"{landmarkCoord = }\n Planet Pos = {[body.screenX, body.screenY]}\n")

                        if body.screenX - planetPosPadding <= landmarkCoord[0] <= body.screenX + planetPosPadding and \
                                body.screenY - planetPosPadding <= landmarkCoord[1] <= body.screenY + planetPosPadding:
                            canPlaceBody = False
                            continue

                    if canPlaceBody:
                        body = CelestialBody('Small Planet',
                                             [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], "",
                                             2 * 10 ** 30 * 50, [0, 0], [0, 0], [0, 0],
                                             [landmarkCoord[0] * A.SIM_SCALE, landmarkCoord[1] * A.SIM_SCALE])
                        phys_sim.add_depression(body)
                    else:
                        print("TOO CLOSE TO SPAWN PLANET")

        phys_sim.applyForces(phys_sim.calc_forces())
        A.pygame.display.update()
