import random
import sys
import math
import threading
import pygame

import BASE_GAME_FILES.scripts.PhysicsSimulation as P_SIM
import BASE_GAME_FILES.scripts.GestureTrackingSim as GT_SIM
import BASE_GAME_FILES.scripts.HandTrackingSim as HT_SIM
import BASE_GAME_FILES.scripts.LevelSystems as L_SYS
import BASE_GAME_FILES.scripts.AbilitySystems as A_SYS
import BASE_GAME_FILES.scripts.Utils as utils

import BASE_GAME_FILES.data.Levels as Levels
import BASE_GAME_FILES.data.Abilities as Abilities

import BASE_GAME_FILES.scripts.Actor as A


class Game:

    def __init__(self):
        self.hands: list = []
        threading.Thread(target=self.get_hands).start()

        self.gesture_sim = GT_SIM.GestureSim()
        self.hand_sim = HT_SIM.HandSim()
        self.level_loader = L_SYS.LevelLoader(Levels.levels, A.selected_level)
        self.phys_sim = None

        self.assets = {

        }

    def get_hands(self):
        while True:
            self.hands = HT_SIM.HandSim.get_hands()

    def run(self):
        self.level_loader.load_level_index(A.selected_level)  # loads initial level

        while True:
            A.game_specs.display.fill(A.BACKGROUND_COLOR)

            game_time_change_increment = (A.TIME_CHANGE_PER_SECOND / A.TPS) * A.time_change_mult

            A.game_time += game_time_change_increment
            A.sim_time = A.game_time * A.SIM_TIME_EQUIVALENCE

            # Closes the application on quit
            for event in A.pygame.event.get():
                if event.type == A.pygame.QUIT:
                    A.pygame.quit()
                    sys.exit()

            keys = A.pygame.key.get_pressed()

            A.updateMovementParams(keys, A)
            changeInLevel, self.phys_sim = A.updateCurrentLevel(keys, self.level_loader)

            if changeInLevel:  # RESETS ABILITIES (COULD BE USED TO CHEAT OUT COOLDOWNS BUT EH)
                for ability in Abilities.abilities:
                    ability.current_cooldown = 0

            for hand in HT_SIM.convertCamHandsToScreenSpaceHands(self.hands):  # MAKE INTO STARS LATER
                for lm in hand:
                    A.pygame.draw.circle(A.game_specs.display, [255, 255, 255], center=(lm[1], lm[2]), radius=5)

            # for gesture in gestures:  # DISPLAYS WHAT GESTURES ARE BEING DONE (alL gestures)
            #     gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
            #     if len(gesturingHands) > 0:
            #         print(gesture, "Being Did'd by hands:", gesturingHands)

            self.phys_sim.applyForces(self.phys_sim.celestial_bodies)
            self.level_loader.currentLevel.playerBody.updatePhys(self.phys_sim)
            self.level_loader.currentLevel.playerBody.drawPath(prediction_length=50)

            for ability in Abilities.abilities:
                ability.checkForAbilityTrigger(game_time_change_increment)

            # screen_centre_pos = [A.game_specs.SIZE[0] / 4, A.game_specs.SIZE[1] / 4]  # shows the center of the screen
            # A.pygame.draw.circle(A.game_specs.display, [0, 0, 255], screen_centre_pos, 5)

            A.game_specs.screen.blit(pygame.transform.scale(A.game_specs.display, A.game_specs.screen.get_size()),
                                     (0, 0))
            A.pygame.display.update()
            A.game_specs.clock.tick(A.TPS)


game = Game()

A.game_specs = A.GameSpecs()
Abilities.abilities = Abilities.initialise_abilities(game)
game.run()
