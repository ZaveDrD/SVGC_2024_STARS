import os
import random
import sys
import math
import threading
import pygame
from PygameShader import *

import BASE_GAME_FILES.scripts.PhysicsSimulation as P_SIM
import BASE_GAME_FILES.scripts.GestureTrackingSim as GT_SIM
import BASE_GAME_FILES.scripts.HandTrackingSim as HT_SIM
import BASE_GAME_FILES.scripts.LevelSystems as L_SYS
import BASE_GAME_FILES.scripts.AestheticSystems as A_SYS
import BASE_GAME_FILES.scripts.MenuSystems as M_SYS
import BASE_GAME_FILES.data.MenuData as Menus
import BASE_GAME_FILES.scripts.AbilitySystems as Ab_SYS
import BASE_GAME_FILES.scripts.Utils as utils
import BASE_GAME_FILES.scripts.PlanetArtGenerator as PAG

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

        background_objects = A_SYS.generateBackgroundStars(2000, color=[255, 255, 255])

        self.backgroundAesthetics: A_SYS.BackgroundRenderer = A_SYS.BackgroundRenderer(background_objects, A.BACKGROUND_COLOR)

        self.phys_sim = None

        PAG.Generate_Art(A.initial_art_generation['Planet'], A.initial_art_generation['Meteor'],
                         A.initial_art_generation['Star'], A.initial_art_generation['Black_Hole'])

        self.assets = {
            'Planet': [i for i in os.listdir(utils.BASE_IMG_PATH) if i.__contains__("spherized_planet_procedural_art")],
            'Meteor': [i for i in os.listdir(utils.BASE_IMG_PATH) if i.__contains__("spherized_meteor_procedural_art")],
            'Star': [i for i in os.listdir(utils.BASE_IMG_PATH) if i.__contains__("spherized_star_procedural_art")],
            'Black_Hole': [i for i in os.listdir(utils.BASE_IMG_PATH) if i.__contains__("spherized_black_hole_procedural_art")]
        }

    def get_hands(self):
        while True:
            self.hands = HT_SIM.HandSim.get_hands()

    def run(self):
        self.level_loader.load_level_index(A.selected_level)  # loads initial level

        while True:
            self.backgroundAesthetics.render_background()
            self.backgroundAesthetics.render_background_objects()

            mousePX, mousePY = A.pygame.mouse.get_pos()
            mouseX, mouseY = utils.ScaleCoordinateToScreenSize([mousePX, mousePY])
            A.mouse.set_mouse_pos(mouseX, mouseY)

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
                    ability.current_cooldown = 0  # could save cooldowns as we change levels but i cbb

            for hand in HT_SIM.convertCamHandsToScreenSpaceHands(self.hands):  # MAKE INTO STARS LATER
                for lm in hand:
                    A.pygame.draw.circle(A.game_specs.renderer.layers[0].display, [255, 255, 255], center=(lm[1], lm[2]), radius=5)

            # for gesture in gestures:  # DISPLAYS WHAT GESTURES ARE BEING DONE (alL gestures)
            #     gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
            #     if len(gesturingHands) > 0:
            #         print(gesture, "Being Did'd by hands:", gesturingHands)

            self.phys_sim.applyForces(self.phys_sim.celestial_bodies)

            self.level_loader.currentLevel.playerBody.updatePhys(self.phys_sim)
            self.level_loader.currentLevel.playerBody.drawPath(prediction_length=75)
            self.level_loader.currentLevel.playerBody.checkForPlayerDeath()

            self.level_loader.currentLevel.playerBody.calc_collision_data(self.level_loader.currentLevel.endGoal)
            self.level_loader.currentLevel.playerBody.checkForLevelEnd()

            for ability in Abilities.abilities:
                ability.checkForAbilityTrigger(game_time_change_increment)

            screen_centre_pos = [A.game_specs.SIZE[0] / 4, A.game_specs.SIZE[1] / 4]  # shows the center of the screen
            # A.pygame.draw.circle(A.game_specs.renderer.layers[0].display, [0, 0, 255], screen_centre_pos, 5)

            Menus.TestMenu.open_menu()
            Menus.TestMenu.updateMenu()

            new_display = pixelation(pygame.transform.scale(utils.load_image(self.assets['Star'][0]), (350, 350)))
            A.game_specs.renderer.layers[0].display.blit(new_display, (100, 50))

            A.game_specs.renderer.render_frame()
            # A.game_specs.UI_renderer.render_frame()

            A.game_specs.clock.tick(A.TPS)


A.game_specs = A.GameSpecs()
game = Game()

Abilities.abilities = Abilities.initialise_abilities(game)
game.run()
