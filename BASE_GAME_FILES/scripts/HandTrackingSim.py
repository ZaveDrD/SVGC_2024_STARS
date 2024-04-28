import cv2
import math

import HandTracking.HandTrackingModule as htm
from BASE_GAME_FILES.scripts.Actor import SIZE, gestures

SMOOTHING_CONSTANT: int = 7
cap = cv2.VideoCapture(0)
handDetector = htm.HandDetector()
previousHand: list = None


class HandSim:

    @staticmethod
    def get_hands() -> list[list[list[int]]]:
        global previousHand
        success, img = cap.read()  # PROBLEMATIC LINE (DECREASES PERFORMANCE BY A MILLION) -> solved by threading the func.
        img = handDetector.FindHands(img)

        hands = handDetector.ConstructLandmarkList(img)
        if previousHand is not None:
            for hand in range(0, len(hands)):
                try:
                    previousHand[hand]
                except:
                    continue
                numMoving: int = 0
                for lm in range(0, len(hands[hand])):
                    if math.dist(hands[hand][lm], previousHand[hand][lm]) < SMOOTHING_CONSTANT:
                        hands[hand][lm] = previousHand[hand][lm]
                    else:
                        numMoving += 1
                        if numMoving > 7:
                            break

        cv2.waitKey(1)
        previousHand = hands

        return hands

    @staticmethod
    def calcScreenSpaceLandmarks(landmarks: list[list[int]]) -> list[list[int]]:
        new_hand_lm = []
        for lm in landmarks:
            new_hand_lm.append([lm[0], lm[1] * (-SIZE[0] / 640) + SIZE[0], lm[2] * (SIZE[1] / 480), lm[3]])
        return new_hand_lm

    def convertCamHandsToScreenSpaceHands(self, hands: list[list[list[int]]]) -> list[list[list[int]]]:
        new_hand_list = []
        for hand in hands:
            new_hand_list.append(self.calcScreenSpaceLandmarks(hand))
        return new_hand_list


class Hand:

    def __init__(self, landmarks: list[list[int]]):
        self.landmarks = landmarks
        self.screenSpace_lm = HandSim.calcScreenSpaceLandmarks(landmarks)
        self.gestures = gestures


class Hands:
    def __init__(self, handList: list[Hand]):
        self.handList = handList
