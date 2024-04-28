import math
import time

from BASE_GAME_FILES.scripts.Actor import gesture_tracking_sim


class Gesture:
    pass


class StaticGesture(Gesture):
    def __init__(self, *params: list[dict[str, list[int | None]]]):
        self.params = params

    def detect(self, hands: list[list[int]]) -> bool:
        """
        A method to detect if the gesture is being done
        ## Args:
            hands: (list[list[int]]) The hand
        ## Returns:
            bool - True if the gesture is being done, else false
        """
        handsDoingGesture = []
        None_Banned_Hands = []

        for param in self.params:  # If ONE parameter is false, it's not true for that hand
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
                if param[0][0] >= len(hands) or param[1][0] >= len(hands): return []
                if len(hands[param[0][0]]) < 21 or len(hands[param[1][0]]) < 21: return []

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
            for param in self.params:
                if not param[0][0] in handsDoingGesture:
                    handsDoingGesture.append(param[0][0])

                if not param[1][0] in handsDoingGesture:
                    handsDoingGesture.append(param[1][0])

            return handsDoingGesture


class MotionGesture(Gesture):
    def __init__(self, gesture: StaticGesture, index: list[int], *others: list[dict['gesture': StaticGesture, 'offset': list[int], 'index': list[int]]]):
        start = {
            'gesture': gesture,
            'x': 0,
            'y': 0,
            'index': {
                'hand': index[0],
                'landmark': index[1]
            },
        }
        self.params = [start] + [
            {
                'gesture': i['gesture'],
                'x': i['offset'][0],
                'y': i['offset'][1],
                'index': i['index']
            }
            for i in others
        ]
        self.hands: list[list[int | list[int]]] = []
        # Hand, Level, level start time, [x, y]

    def detect(self, hands: list[list[list[int]]]) -> bool:
        for num, hand in enumerate(hands):
            if hand not in self.hands or self.hands[hand][1] == -1:
                index = self.params[0]['index']
                if gesture_tracking_sim.detect_vertebraeC6(hands, self.params[0]['gesture']):
                    self.hands.append([num, 0, hand[index[1]]])
                else:
                    hands.append([num, -1, hand[index[1]]])
            else:
                params = None
                for h in self.hands:
                    if h[0] == num:
                        params = self.params[h[1]]
                        break
                if abs(time.time() - self.hands[num][3]) >= 1.5:
                    self.hands[num][1] = -1
                    self.hands[num][2] = 0
                    self.hands[3] = [0, 0]

                if gesture_tracking_sim.detect_vertebraeC6(hands, params['gesture']) and\
                    abs(params['x']-hand[index[3]][0]) < 30 and abs(params['y']-hand[index[3][1]]) < 30:
                    self.hands[num][1] += 1
                    self.hands[num][2] = hand[index[3][0]][index[3][1]]
                    self.hands[num][3] = time.time()


class GestureSim:

    def detect_vertebraeC6(hands: list[list[list[int]]], params: list[list]) -> list[int]:
        """
        Detect Gestures
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
            if param[0][0] == param[1][0] and param[0][0] is not None:  # If its for only one hand
                if param[0][0] >= len(hands): return []
                if len(hands[param[0][0]]) < 21: return []

                selected_hand = hands[param[0][0]]
                distBtwPoints = abs(math.dist(selected_hand[param[0][1]], selected_hand[param[1][1]]))

                if param[3]:
                    result = distBtwPoints < param[2]
                else:
                    result = distBtwPoints > param[2]

                if not result: return []

            if not param[0][0] == param[1][0] and param[0][0] is not None and param[1][0] is not None:
                if param[0][0] >= len(hands) or param[1][0] >= len(hands): return []
                if len(hands[param[0][0]]) < 21 or len(hands[param[1][0]]) < 21: return []

                distBtwPoints = abs(math.dist(hands[param[0][0]][param[0][1]], hands[param[1][0]][param[1][1]]))

                if param[3]:
                    result = distBtwPoints < param[2]
                else:
                    result = distBtwPoints > param[2]

                if not result: return []

            if param[0][0] is None or param[1][0] is None:
                num_results_true = 0
                for hand_num, hand in enumerate(hands):
                    if len(hand) < 21: return []

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

                if num_results_true == 0: return []

        if len(handsDoingGesture) > 0:
            return handsDoingGesture
        else:
            for param in params:
                if not param[0][0] in handsDoingGesture:
                    handsDoingGesture.append(param[0][0])

                if not param[1][0] in handsDoingGesture:
                    handsDoingGesture.append(param[1][0])

            return handsDoingGesture
