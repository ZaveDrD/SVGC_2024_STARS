import math
import random

import BASE_GAME_FILES.scripts.Actor as A
import BASE_GAME_FILES.scripts.HandTrackingSim as HT_SIM
import BASE_GAME_FILES.scripts.PhysicsSimulation as P_SIM
import BASE_GAME_FILES.data.Assets as Assets


class Ability:
    def __init__(self, abilityName: str, triggeredFunc, gestureKey: str, game, cooldown: float, unlockLevel=0):
        self.abilityName = abilityName
        self.triggerFunc = triggeredFunc
        self.gestureKey = gestureKey

        self.unlockLevel = unlockLevel
        self.game = game

        self.numActivations = 0

        self.cooldown = cooldown
        self.current_cooldown = 0

    def checkForAbilityTrigger(self, time_change):
        if self.current_cooldown == 0:
            gesturingHands = self.game.gesture_sim.detect_vertebraeC6(HT_SIM.convertCamHandsToScreenSpaceHands(self.game.hands),
                                                                A.gestures[self.gestureKey])
            if len(gesturingHands) > 0:
                if self.abilityName == 'Reset Ability':
                    self.ResetAbility(gesturingHands)
                    self.resetCooldown()
                elif self.triggerFunc(gesturingHands, self.game.hands, self.game.phys_sim):
                    self.numActivations += 1
                    self.resetCooldown()
        else:
            if self.current_cooldown - time_change >= 0:
                self.current_cooldown -= time_change
            else:
                self.current_cooldown = 0
            # print(self.abilityName + " is on cooldown: " + str(self.current_cooldown))

    def ResetAbility(self, gesturing_hands):
        print("RESETTING LEVEL")
        hand1 = HT_SIM.calcScreenSpaceLandmarks(self.game.hands[gesturing_hands[0]])
        hand2 = HT_SIM.calcScreenSpaceLandmarks(self.game.hands[gesturing_hands[1]])

        if hand1[3][2] < hand1[4][2] and hand2[3][2] < hand2[4][2]:
            self.game.resetLevel()

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
                landmarkCoord = [pinchingHand[A.gestures['Pinch'][0][0][1]][1] - planetaryBody.radius * A.player_zoom,
                                 pinchingHand[A.gestures['Pinch'][0][0][1]][2] - planetaryBody.radius * A.player_zoom]

                bodyPos = [planetaryBody.px, planetaryBody.py]

                # print("ATTEMPTING TO GRABBING BODY AT: " + str(landmarkCoord[0]), str(landmarkCoord[1]))

                if abs(math.dist(landmarkCoord, bodyPos)) <= planetaryBody.radius * A.player_zoom:
                    planetaryBody.set_pos_px([landmarkCoord[0], landmarkCoord[1]])
                    A.pygame.draw.line(A.game_specs.renderer.layers[0].display, [0, 0, 255], landmarkCoord, bodyPos)

                    return True

    @staticmethod
    def SummonPlanetAbility(gesturing_hands, hands, phys_sim) -> bool:
        for hand in gesturing_hands:
            if hand is None: break
            if hand >= len(hands): break

            summoningHand = HT_SIM.calcScreenSpaceLandmarks(hands[hand])

            landmarkCoord = [(summoningHand[9][1] + summoningHand[12][1]) / 2,
                             (summoningHand[9][2] + summoningHand[12][2]) / 2]

            x, y = P_SIM.CelestialBody.conv_px_to_x(0, landmarkCoord[0], landmarkCoord[1])
            body = P_SIM.Planet(Assets.rand_key('Planet'), 10e14, [x, y])
            phys_sim.add_object([body])

            return True

    @staticmethod
    def SummonStarAbility(gesturing_hands, hands, phys_sim) -> bool:
        hand1 = HT_SIM.calcScreenSpaceLandmarks(hands[gesturing_hands[0]])
        hand2 = HT_SIM.calcScreenSpaceLandmarks(hands[gesturing_hands[1]])

        landmarkCoord = [(hand1[9][1] + hand2[9][1]) / 2, (hand1[12][2] + hand1[0][2]) / 2]

        x, y = P_SIM.CelestialBody.conv_px_to_x(0, landmarkCoord[0], landmarkCoord[1])
        body = P_SIM.Star(Assets.rand_key('Star'), 25e17, [x, y])
        phys_sim.add_object([body])

        return True

    @staticmethod
    def SummonBlackHoleAbility(gesturing_hands, hands, phys_sim) -> bool:
        hand1 = HT_SIM.calcScreenSpaceLandmarks(hands[gesturing_hands[0]])
        hand2 = HT_SIM.calcScreenSpaceLandmarks(hands[gesturing_hands[1]])

        landmarkCoord = [(hand1[10][1] + hand2[10][1]) / 2, (hand1[8][2] + hand1[20][2]) / 2]

        x, y = P_SIM.CelestialBody.conv_px_to_x(0, landmarkCoord[0], landmarkCoord[1])
        body = P_SIM.BlackHole(Assets.rand_key('Black_Hole'), 75e18, [x, y])
        phys_sim.add_object([body])

        return True

    @staticmethod
    def EnlargeAbility(gesturing_hands, hands, phys_sim) -> bool:
        print("ENLARGING PLANET")
        for hand in gesturing_hands:
            if hand is None: break
            if hand >= len(hands): break

            hand_lm = HT_SIM.calcScreenSpaceLandmarks(hands[hand])

            for planetaryBody in phys_sim.celestial_bodies:  # SUMMON PLANETS

                # If planet is between hand_lm[5] and hand_lm[20], call the add_mass function for that planet
                if hand_lm[8][1] < planetaryBody.px < hand_lm[20][1] and hand_lm[8][2] < planetaryBody.py < hand_lm[5][2]:
                    planetaryBody.add_mass(planetaryBody.return_mass() * 0.1)

                    return True

    @staticmethod
    def ShrinkAbility(gesturing_hands, hands, phys_sim) -> bool:
        for hand in gesturing_hands:
            if hand is None: break
            if hand >= len(hands): break

            hand_lm = HT_SIM.calcScreenSpaceLandmarks(hands[hand])

            for planetaryBody in phys_sim.celestial_bodies:  # SUMMON PLANETS

                # If planet is between hand_lm[5] and hand_lm[20], call the add_mass function for that planet
                if hand_lm[8][1] < planetaryBody.px < hand_lm[20][1] and hand_lm[8][2] < planetaryBody.py < hand_lm[5][2]:
                    planetaryBody.add_mass(-planetaryBody.return_mass() * 0.1)

                    return True
        return False

    @staticmethod
    def ResetAbility(gesturing_hands, hands, phys_sim) -> bool:
        return True

    @staticmethod
    def MoveAbility(gesturing_hands, hands, phys_sim) -> bool:
        if len(gesturing_hands) < 1: return False
        if len(hands) < 1: return False
        hand = HT_SIM.calcScreenSpaceLandmarks(hands[gesturing_hands[0]])
        lm7 = hand[7]
        lm8 = hand[8]

        direction = ((lm8[1] - lm7[1]) / 3, (lm8[2] - lm7[2]) / 3)
        A.player_view_pos_y += direction[1] / A.player_zoom
        A.player_view_pos_x += direction[0] / A.player_zoom

        return True

    @staticmethod
    def TimeControlAbility(gesturing_hands, hands, phys_sim) -> bool:
        if len(gesturing_hands) < 1: return False
        if len(hands) < 1: return False
        hand = HT_SIM.calcScreenSpaceLandmarks(hands[gesturing_hands[0]])
        lm7 = hand[7]
        lm8 = hand[8]
        direction = ((lm8[1] - lm7[1]) / 3, (lm8[2] - lm7[2]) / 3)

        if direction[0] > 0:
            A.time_change_mult += A.TIME_CHANGE_MULT_CHANGE_RATE
        elif direction[0] < 0:
            A.time_change_mult -= A.TIME_CHANGE_MULT_CHANGE_RATE

        return True

    @staticmethod
    def ZoomInAbility(gesturing_hands, hands, phys_sim) -> bool:
        A.player_zoom = A.player_zoom_max_min[1] if A.player_zoom + A.ZOOM_MULT_INC > A.player_zoom_max_min[1] else A.player_zoom + A.ZOOM_MULT_INC

        return True

    @staticmethod
    def ZoomOutAbility(gesturing_hands, hands, phys_sim) -> bool:
        A.player_zoom = A.player_zoom_max_min[0] if A.player_zoom - A.ZOOM_MULT_INC < A.player_zoom_max_min[0] else A.player_zoom - A.ZOOM_MULT_INC

        return True