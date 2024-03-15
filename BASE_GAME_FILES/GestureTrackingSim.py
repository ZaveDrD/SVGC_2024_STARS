import HandTracking.HandTrackingModule as htm
from math import sqrt
import cv2
import math
import time


gestures = {
    #   True      ->      Less Than        ->     dist < X
    #   False     ->      Greater Than     ->     dist > X

    'pinch': [
        [[None, 4], [None, 8], 100, True],
        [[None, 3], [None, 7], 10, False]]
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

    for param in params:
        if param[0][0] is not None and param[1][0] is not None:
            if param[0][0] >= len(hands) or param[1][0] >= len(hands): return []

            distBtwPoints = abs(math.dist(hands[param[0][0]][param[0][1]], hands[param[1][0]][param[1][1]]))
            if param[3]:
                result = distBtwPoints < param[2]
            else:
                result = distBtwPoints > param[2]

            if result:
                if param[0][0] == param[1][0]:
                    handsDoingGesture.append(param[0][0])
                else:
                    handsDoingGesture.append(param[0][0])
                    handsDoingGesture.append(param[1][0])

            return handsDoingGesture

        # Situation where its None

        for hand in hands:
            if len(hand) != 20: return []

            distBtwPoints = abs(math.dist(hand[param[0][1]], hand[param[1][1]]))
            if param[3]:
                result = distBtwPoints < param[2]
            else:
                result = distBtwPoints > param[2]

            if result:
                handsDoingGesture.append(hand.index())

        return handsDoingGesture


# def detect_continuous(hands, previous) -> dict[str, dict[str, bool]]

def main():
    cap = cv2.VideoCapture(0)
    handDetector = htm.HandDetector()

    while True:
        success, img = cap.read()

        img = handDetector.FindHands(img)

        hands = handDetector.ConstructLandmarkList(img)

        for gesture in gestures:
            gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
            if len(gesturingHands) > 0:
                print(gesture, "Being Did'd by hands:", gesturingHands)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()

