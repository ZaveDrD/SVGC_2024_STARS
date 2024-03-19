import HandTracking.HandTrackingModule as htm
from math import sqrt
import cv2
import math
import time


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

