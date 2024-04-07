import random
import pygame
import PhysicsSimulation
import atexit
import sys
import Actor as A
import threading
import HandTrackingSim
import math
import time



atexit.register(lambda: [pygame.quit(), sys.exit()])

pygame.display.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode([WIDTH, HEIGHT])

A.WIDTH, A.HEIGHT = WIDTH, HEIGHT
hands: list = []

true = True
false = False
null = None

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

        for param in self.params:  # If ONE parameter is wrong, it's not true for that hand
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
                if detect_vertebraeC6(hands, self.params[0]['gesture']):
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

                if detect_vertebraeC6(hands, params['gesture']) and\
                    abs(params['x']-hand[index[3]][0]) < 30 and abs(params['y']-hand[index[3][1]]) < 30:
                    self.hands[num][1] += 1
                    self.hands[num][2] = hand[index[3][0]][index[3][1]]
                    self.hands[num][3] = time.time()



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
        [gestures['pinch'], None, None],
        [gestures['pinch'], [0, 100, [None, 0]], [0.2, 1.4]]
        # [GESTURE, [OFFSET_X, OFFSET_Y, [HAND, LANDMARK]] (NONE -> START POSITION), [MIN_TIME, MAX_TIME] (NONE -> START)]
    ]
}


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




def calcScreenSpaceLandmarks(landmarks: list[list[int]]) -> list[list[int]]:
    new_hand_lm = []
    for lm in landmarks:
        new_hand_lm.append([lm[0], lm[1] * (-WIDTH / 640) + WIDTH, lm[2] * (HEIGHT / 480), lm[3]])
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
        self.gestures = gestures


class Hands:
    def __init__(self, handList: list[Hand]):
        self.handList = handList


def get_hands():
    global hands
    while True:
        hands = HandTrackingSim.get_hands()
        # hands = Hands(hands_raw)


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
        self.screenX = self.x / A.SIM_SCALE + A.offsetX
        self.screenY = self.y / A.SIM_SCALE + A.offsetY

    def display(self):
        # print(f"\n{ self.name = }, { self.x = }, { self.y = }")
        pygame.draw.circle(screen, self.color, center=(self.screenX, self.screenY), radius=self.mass / A.SCALE_MASS_EQUIVALENCE)

    def updatePlanetPosition_ScreenSpace(self, x: float, y: float):
        self.screenX = x
        self.screenY = y

        self.x = (self.screenX - A.offsetX) * A.SIM_SCALE
        self.y = (self.screenY - A.offsetY) * A.SIM_SCALE

        self.display()

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

        self.screenX = self.x / A.SIM_SCALE + A.offsetX
        self.screenY = self.y / A.SIM_SCALE + A.offsetY

        self.display()


if __name__ == "__main__":
    initial_celestial_bodies = [
        CelestialBody('SUN 2', [255, 255, 255], "", 2e30 * 100, [0, 0], [0, 0], [0, 0], [25000000000000, 12000000000000])
        # CelestialBody('SUN 2', [255, 255, 255], "", 2e30 * 100, [0, 0], [0, 0], [0, 0], [0, 4000000000000])
        # CelestialBody('SUN 1', [0, 0, 0], "", 2e30, [0, 0], [0, 0], [15e-10, 0], [0, -2000000000000]),
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

        for hand in convertCamHandsToScreenSpaceHands(hands):
            for lm in hand:
                # print(f"{lm = }")
                pygame.draw.circle(screen, [0, 0, 0], center=(lm[1], lm[2]), radius=10)

        # for gesture in gestures:
        #     gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
        #     if len(gesturingHands) > 0:
        #         print(gesture, "Being Did'd by hands:", gesturingHands)

        for planetaryBody in initial_celestial_bodies:  # PINCH DETECTION TO GRAB PLANETS
            pinchingHands = detect_vertebraeC6(convertCamHandsToScreenSpaceHands(hands), gestures['Pinch'])
            if len(pinchingHands) == 0: break
            for hand in pinchingHands:
                if hand is None: break
                if hand >= len(hands): break

                pinchingHand = calcScreenSpaceLandmarks(hands[hand])
                landmarkCoord = [pinchingHand[gestures['Pinch'][0][0][1]][1],
                                 pinchingHand[gestures['Pinch'][0][0][1]][2]]

                plantPos = [planetaryBody.screenX, planetaryBody.screenY]

                # print(abs(math.dist(landmarkCoord, plantPos)))
                # print("Planet Pos", plantPos, "\n", "Landmark Pos", landmarkCoord)

                if abs(math.dist(landmarkCoord, plantPos)) <= planetaryBody.mass / A.SCALE_MASS_EQUIVALENCE:
                    planetaryBody.updatePlanetPosition_ScreenSpace(landmarkCoord[0], landmarkCoord[1])

        for planetaryBody in initial_celestial_bodies:  # SUMMON PLANETS
            planetSummoningHands = detect_vertebraeC6(convertCamHandsToScreenSpaceHands(hands), gestures['Summon Small Planet'])
            if len(planetSummoningHands) == 0: break
            for hand in planetSummoningHands:
                if hand is None: break
                if hand >= len(hands): break

                summoningHand = calcScreenSpaceLandmarks(hands[hand])
                print(summoningHand[9][0], summoningHand[12][0])
                landmarkCoord = [(summoningHand[9][1] + summoningHand[12][1]) / 2, (summoningHand[9][2] + summoningHand[12][2]) / 2]
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
                    body = CelestialBody('Small Planet', [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], "", 2 * 10 ** 30 * 50, [0, 0], [0, 0], [0, 0],
                                         [landmarkCoord[0] * A.SIM_SCALE, landmarkCoord[1] * A.SIM_SCALE])
                    phys_sim.add_depression(body)
                else:
                    print("TOO CLOSE TO SPAWN PLANET")

        phys_sim.applyForces(phys_sim.calc_forces())

        pygame.display.update()
