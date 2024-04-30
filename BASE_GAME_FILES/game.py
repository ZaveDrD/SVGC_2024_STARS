import random
import sys
import math
import threading

import BASE_GAME_FILES.scripts.PhysicsSimulation as P_SIM
import BASE_GAME_FILES.scripts.GestureTrackingSim as GT_SIM
import BASE_GAME_FILES.scripts.HandTrackingSim as HT_SIM
import BASE_GAME_FILES.scripts.LevelSystems as L_SIM
import BASE_GAME_FILES.data.Levels as Levels
import BASE_GAME_FILES.scripts.Utils as utils

import BASE_GAME_FILES.scripts.Actor as A

hands: list = []


def get_hands():
    global hands
    while True:
        hands = HT_SIM.HandSim.get_hands()


threading.Thread(target=get_hands).start()


class Game:

    def __init__(self):
        A.game_specs = A.GameSpecs()

        self.gesture_sim = GT_SIM.GestureSim()
        self.hand_sim = HT_SIM.HandSim()
        self.level_loader = L_SIM.LevelLoader(Levels.levels, A.selected_level)

        self.assets = {

        }

    def run(self):
        self.level_loader.load_level_index(A.selected_level)  # loads initial level

        while True:
            A.game_time += (A.TIME_CHANGE_PER_SECOND / A.TPS) * A.time_change_mult
            A.sim_time = A.game_time * A.SIM_TIME_EQUIVALENCE

            # Closes the application on quit
            for event in A.pygame.event.get():
                if event.type == A.pygame.QUIT:
                    A.pygame.quit()
                    sys.exit()

            keys = A.pygame.key.get_pressed()
            A.updateMovementParams(keys, A)

            phys_sim = A.updateCurrentLevel(keys, self.level_loader)

            for hand in HT_SIM.convertCamHandsToScreenSpaceHands(hands):  # MAKE INTO STARS LATER
                for lm in hand:
                    A.pygame.draw.circle(A.game_specs.screen, [0, 0, 0], center=(lm[1], lm[2]), radius=10)

            # for gesture in gestures:  # DISPLAYS WHAT GESTURES ARE BEING DONE (alL gestures)
            #     gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
            #     if len(gesturingHands) > 0:
            #         print(gesture, "Being Did'd by hands:", gesturingHands)

            pinchingHands = self.gesture_sim.detect_vertebraeC6(HT_SIM.convertCamHandsToScreenSpaceHands(hands), A.gestures['Pinch'])
            if len(pinchingHands) > 0:
                for planetaryBody in phys_sim.celestial_bodies:  # PINCH DETECTION TO GRAB PLANETS
                    if planetaryBody.merged: continue
                    for hand in pinchingHands:
                        if hand is None: break
                        if hand >= len(hands): break

                        pinchingHand = HT_SIM.calcScreenSpaceLandmarks(hands[hand])
                        landmarkCoord = [pinchingHand[A.gestures['Pinch'][0][0][1]][1],
                                         pinchingHand[A.gestures['Pinch'][0][0][1]][2]]

                        bodyPos = [planetaryBody.px, planetaryBody.py]

                        if abs(math.dist(landmarkCoord, bodyPos)) <= planetaryBody.radius * A.player_zoom:
                            planetaryBody.set_pos([landmarkCoord[0], landmarkCoord[1]])

            planetSummoningHands = self.gesture_sim.detect_vertebraeC6(
                HT_SIM.convertCamHandsToScreenSpaceHands(hands), A.gestures['Summon Small Planet'])
            if len(planetSummoningHands) > 0:
                for planetaryBody in phys_sim.celestial_bodies:  # SUMMON PLANETS
                    if planetaryBody.merged: continue
                    for hand in planetSummoningHands:
                        if hand is None: break
                        if hand >= len(hands): break

                        summoningHand = HT_SIM.calcScreenSpaceLandmarks(hands[hand])

                        landmarkCoord = [(summoningHand[9][1] + summoningHand[12][1]) / 2,
                                         (summoningHand[9][2] + summoningHand[12][2]) / 2]

                        planetPosPadding = 50
                        canPlaceBody = True

                        for body in phys_sim.celestial_bodies:
                            if planetaryBody.merged: continue

                            if body.px - (body.radius * A.player_zoom) - planetPosPadding <= landmarkCoord[0] <= body.px + (body.radius * A.player_zoom) + planetPosPadding and \
                                    body.py - (body.radius * A.player_zoom) - planetPosPadding <= landmarkCoord[1] <= body.py + (body.radius * A.player_zoom) + planetPosPadding:
                                canPlaceBody = False
                                continue

                        if canPlaceBody:
                            body = P_SIM.CelestialBody([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                                                                   10e14, [landmarkCoord[0], landmarkCoord[1]])
                            phys_sim.add_object([body])
                        else:
                            print("TOO CLOSE TO SPAWN PLANET")

            phys_sim.applyForces(phys_sim.celestial_bodies)

            A.game_specs.screen.blit(A.game_specs.display, (0, 0))
            A.pygame.display.update()
            A.game_specs.clock.tick(A.TPS)


game = Game()
game.run()
