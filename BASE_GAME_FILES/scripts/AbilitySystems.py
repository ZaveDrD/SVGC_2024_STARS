import math
import random

import BASE_GAME_FILES.scripts.Actor as A
import BASE_GAME_FILES.scripts.HandTrackingSim as HT_SIM
import BASE_GAME_FILES.scripts.PhysicsSimulation as P_SIM


class Ability:
    def __init__(self, abilityName: str, triggeredFunc, gestureKey: str, game, cooldown: float, unlockLevel=0):
        self.abilityName = abilityName
        self.triggerFunc = triggeredFunc
        self.gestureKey = gestureKey

        self.unlockLevel = unlockLevel
        self.game = game

        self.cooldown = cooldown
        self.current_cooldown = 0

    def checkForAbilityTrigger(self, time_change):
        if self.current_cooldown == 0:
            gesturingHands = self.game.gesture_sim.detect_vertebraeC6(HT_SIM.convertCamHandsToScreenSpaceHands(self.game.hands),
                                                                A.gestures[self.gestureKey])
            if len(gesturingHands) > 0:
                if self.triggerFunc(gesturingHands, self.game.hands, self.game.phys_sim):
                    self.resetCooldown()
        else:
            if self.current_cooldown - time_change >= 0:
                self.current_cooldown -= time_change
            else:
                self.current_cooldown = 0
            # print(self.abilityName + " is on cooldown: " + str(self.current_cooldown))

    def resetCooldown(self):
        self.current_cooldown = self.cooldown


class AbilityFunctions:
    @staticmethod
    def GrabPlanetAbility(gesturing_hands, hands, phys_sim) -> bool:
        for planetaryBody in phys_sim.celestial_bodies:  # PINCH DETECTION TO GRAB PLANETS
            if planetaryBody.merged: continue
            if not planetaryBody.interaction: continue
            for hand in gesturing_hands:
                if hand is None: break
                if hand >= len(hands): break

                pinchingHand = HT_SIM.calcScreenSpaceLandmarks(hands[hand])
                landmarkCoord = [pinchingHand[A.gestures['Pinch'][0][0][1]][1],
                                 pinchingHand[A.gestures['Pinch'][0][0][1]][2]]

                bodyPos = [planetaryBody.px, planetaryBody.py]

                # print("ATTEMPTING TO GRABBING BODY AT: " + str(landmarkCoord[0]), str(landmarkCoord[1]))

                if abs(math.dist(landmarkCoord, bodyPos)) <= planetaryBody.radius * A.player_zoom:
                    planetaryBody.set_pos_px([landmarkCoord[0], landmarkCoord[1]])
                    A.pygame.draw.line(A.game_specs.display, [0, 0, 255], landmarkCoord, bodyPos)

                    return True

    @staticmethod
    def SummonPlanetAbility(gesturing_hands, hands, phys_sim) -> bool:
        for planetaryBody in phys_sim.celestial_bodies:  # SUMMON PLANETS
            if planetaryBody.merged: continue
            if not planetaryBody.interaction: continue
            for hand in gesturing_hands:
                if hand is None: break
                if hand >= len(hands): break

                summoningHand = HT_SIM.calcScreenSpaceLandmarks(hands[hand])

                landmarkCoord = [(summoningHand[9][1] + summoningHand[12][1]) / 2,
                                 (summoningHand[9][2] + summoningHand[12][2]) / 2]

                x, y = P_SIM.CelestialBody.conv_px_to_x(landmarkCoord[0], landmarkCoord[1])
                body = P_SIM.Planet([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                                           10e13, [x, y])
                phys_sim.add_object([body])

                return True
