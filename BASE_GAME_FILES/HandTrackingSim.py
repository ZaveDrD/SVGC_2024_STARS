import cv2
import HandTracking.HandTrackingModule as htm
import subprocess
import math
import IHatePythonSyntax


SMOOTHING_CONSTANT: int = 7
cap = cv2.VideoCapture(0)
handDetector = htm.HandDetector()
previousHand: list = None


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
