import random
import sys
import threading
from PygameShader import *

import BASE_GAME_FILES.scripts.GestureTrackingSim as GT_SIM
import BASE_GAME_FILES.scripts.HandTrackingSim as HT_SIM
import BASE_GAME_FILES.scripts.LevelSystems as L_SYS
import BASE_GAME_FILES.scripts.AestheticSystems as A_SYS
import BASE_GAME_FILES.data.MenuData as Menus
import BASE_GAME_FILES.scripts.Utils as utils
import BASE_GAME_FILES.data.Assets as Assets

import BASE_GAME_FILES.data.Levels as Levels
import BASE_GAME_FILES.data.Abilities as Abilities

import BASE_GAME_FILES.scripts.Actor as A


def ShowDialogue(dialogueIndex: int):
    Menus.DialogueBox.close_menu()
    Menus.DialogueBox.elements[dialogueIndex].show = True
    Menus.DialogueBox.updateMenu()


class Game:

    def __init__(self):
        self.hands: list = []
        threading.Thread(target=self.get_hands).start()

        Assets.load_planets()

        Levels.levels = Levels.Init_Level_Data()

        self.gesture_sim = GT_SIM.GestureSim()
        self.hand_sim = HT_SIM.HandSim()
        self.level_loader = L_SYS.LevelLoader(Levels.levels, A.selected_level)

        background_objects = A_SYS.generateBackgroundStars(3000, color=[255, 255, 255])

        self.backgroundAesthetics: A_SYS.BackgroundRenderer = A_SYS.BackgroundRenderer(background_objects,
                                                                                       A.BACKGROUND_COLOR)

        self.phys_sim = None
        self.levelEndTime = 0

        # AESTHETIC VARIABLES
        self.animated_hand_star_frames = [pygame.image.load(f'GameArt\HandStarAnimationFrames\Star-{i + 1}.png') for i
                                          in range(8)]
        self.current_animation_frame = 0
        self.level_time = 0

    def draw_animated_png(self, display, position, frames, frame_index, size, differing=False):
        if differing:
            frame_index = (frame_index + random.randint(-2, 2)) % len(frames)
        frame = frames[frame_index]
        frame = frame.copy()
        scaled_frame = pygame.transform.scale(frame, size)
        display.blit(scaled_frame, position)

    def get_hands(self):
        while True:
            self.hands = HT_SIM.HandSim.get_hands()

    def draw_dotted_line(self, surface, color, start_pos, end_pos, width=1, dash_length=5):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if dl == 0:
            dl = 0.1
        dx = (x2 - x1) / dl
        dy = (y2 - y1) / dl
        for i in range(0, int(dl / dash_length), 2):
            start = (x1 + dx * i * dash_length, y1 + dy * i * dash_length)
            end = (x1 + dx * (i + 1) * dash_length, y1 + dy * (i + 1) * dash_length)
            pygame.draw.line(surface, color, start, end, width)

    def resetLevel(self):
        self.level_loader.load_level_index(self.level_loader.currentLevelIndex, False)
        for ability in Abilities.abilities:
            ability.numActivations = 0
        self.levelEndTime = 0

    def run(self):
        self.level_loader.load_level_index(A.selected_level)  # loads initial level

        while True:
            self.backgroundAesthetics.render_background()
            self.backgroundAesthetics.render_background_objects()

            mousePX, mousePY = A.pygame.mouse.get_pos()
            mouseX, mouseY = utils.ScaleCoordinateToScreenSize([mousePX, mousePY])
            A.mouse.set_mouse_pos(mouseX, mouseY)

            game_time_change_increment = (A.TIME_CHANGE_PER_SECOND / A.TPS)

            self.level_time += game_time_change_increment

            A.game_time += game_time_change_increment
            A.sim_time = A.game_time * A.SIM_TIME_EQUIVALENCE * A.time_change_mult

            # Closes the application on quit
            for event in A.pygame.event.get():
                if event.type == A.pygame.QUIT:
                    A.pygame.quit()
                    sys.exit()

            keys = A.pygame.key.get_pressed()

            A.updateMovementParams(keys, A)
            changeInLevel, self.phys_sim = A.updateCurrentLevel(keys, self.level_loader)

            for hand in HT_SIM.convertCamHandsToScreenSpaceHands(self.hands):  # MAKE INTO STARS LATER
                for i in range(0, len(hand)):
                    self.draw_animated_png(A.game_specs.renderer.layers[0].display, (hand[i][1] - 10, hand[i][2] - 10),
                                           self.animated_hand_star_frames, self.current_animation_frame, [24, 24],
                                           differing=True)

                if len(hand) > 4:
                    for i in range(0, 4):
                        self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                              (hand[i][1], hand[i][2]), (hand[i + 1][1], hand[i + 1][2]), 1)
                if len(hand) > 8:
                    self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                          (hand[0][1], hand[0][2]), (hand[5][1], hand[5][2]), 1)
                    self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                          (hand[1][1], hand[1][2]), (hand[5][1], hand[5][2]), 1)
                    for i in range(5, 8):
                        self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                              (hand[i][1], hand[i][2]), (hand[i + 1][1], hand[i + 1][2]), 1)
                if len(hand) > 12:
                    self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                          (hand[0][1], hand[0][2]), (hand[9][1], hand[9][2]), 1)
                    for i in range(9, 12):
                        self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                              (hand[i][1], hand[i][2]), (hand[i + 1][1], hand[i + 1][2]), 1)
                if len(hand) > 16:
                    for i in range(13, 16):
                        self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                              (hand[i][1], hand[i][2]), (hand[i + 1][1], hand[i + 1][2]), 1)
                if len(hand) > 20:
                    self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                          (hand[0][1], hand[0][2]), (hand[17][1], hand[17][2]), 1)
                    for i in range(17, 20):
                        self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                              (hand[i][1], hand[i][2]), (hand[i + 1][1], hand[i + 1][2]), 1)
                if len(hand) > 17:
                    for i in [5, 9, 13, 17]:
                        if len(hand) > i + 4:
                            self.draw_dotted_line(A.game_specs.renderer.layers[0].display, [255, 255, 255],
                                                  (hand[i][1], hand[i][2]), (hand[i + 4][1], hand[i + 4][2]), 1)

            self.phys_sim.applyForces(self.phys_sim.celestial_bodies)

            self.level_loader.currentLevel.playerBody.updatePhys(self.phys_sim)
            self.level_loader.currentLevel.playerBody.drawPath(prediction_length=10)
            self.level_loader.currentLevel.playerBody.checkForPlayerDeath()

            self.level_loader.currentLevel.playerBody.calc_collision_data(self.level_loader.currentLevel.endGoal)
            self.level_loader.currentLevel.playerBody.checkForLevelEnd()

            Menus.MissionFailedScreen.close_menu()
            Menus.MissionSuccessScreen.close_menu()

            lost = False

            if self.level_loader.currentLevel.playerBody.alive is False:
                if self.levelEndTime == 0:
                    self.levelEndTime = self.level_time
                    lost = True
                if self.level_time - self.levelEndTime > 1:
                    lost = True
                    self.level_loader.load_level_index(self.level_loader.currentLevelIndex, A.SAVE_LEVELS)
                    changeInLevel = True
                    self.levelEndTime = 0

                Menus.MissionFailedScreen.open_menu()
                Menus.MissionFailedScreen.updateMenu()

            if self.level_loader.currentLevel.playerBody.won and lost is False:
                if self.levelEndTime == 0:
                    self.levelEndTime = self.level_time
                if self.level_time - self.levelEndTime > 1:
                    if self.level_loader.currentLevelIndex == len(self.level_loader.levels) - 1:
                        self.level_loader.load_level_index(self.level_loader.currentLevelIndex + 1, A.SAVE_LEVELS)
                    else:
                        randLevel = L_SYS.Level("Random Level",
                                                Levels.GenRandBodies(200),
                                                playerStartPos=[random.randint(-400, 1000), random.randint(-400, 1000)],
                                                endGoalPos=[random.randint(-400, 1000), random.randint(-400, 1000)],
                                                abilityMaxActivations=[('Summon Planet Ability', random.randint(0, 5)),
                                                                       ('Summon Star Ability', random.randint(0, 5)),
                                                                       ('Summon Black Hole Ability',
                                                                        random.randint(0, 5))]
                                                )
                        self.level_loader.add_level(randLevel)
                        self.level_loader.load_level_index(self.level_loader.currentLevelIndex + 1, A.SAVE_LEVELS)
                    changeInLevel = True
                    self.levelEndTime = 0

                Menus.MissionSuccessScreen.open_menu()
                Menus.MissionSuccessScreen.updateMenu()

            if changeInLevel:  # RESETS ABILITIES (COULD BE USED TO CHEAT OUT COOLDOWNS BUT EH)
                self.level_time = 0

                for ability in Abilities.abilities:
                    ability.numActivations = 0
                    ability.current_cooldown = 0  # could save cooldowns as we change levels but i cbb

            for ability in Abilities.abilities:
                if ability.unlockLevel <= A.selected_level:
                    canTrigger = True
                    if self.level_loader.currentLevel.abilityMaxActivation is not None:
                        for abilityCheck in self.level_loader.currentLevel.abilityMaxActivation:
                            if ability.abilityName == abilityCheck[0]:
                                if ability.numActivations >= abilityCheck[1]:
                                    canTrigger = False

                    if canTrigger:
                        ability.checkForAbilityTrigger(game_time_change_increment)

            if self.level_loader.currentLevel.abilityMaxActivation is not None:
                for abilityCheck in self.level_loader.currentLevel.abilityMaxActivation:
                    if abilityCheck[0] == 'Summon Planet Ability':
                        if abilityCheck[1] != 0:
                            Menus.MaxAbilitiesPlanet.open_menu()
                            Menus.MaxAbilitiesPlanet.elements[
                                0].text = f"Planet: {abilityCheck[1] - Abilities.abilities[1].numActivations}"
                            Menus.MaxAbilitiesPlanet.updateMenu()
                    if abilityCheck[0] == 'Summon Star Ability':
                        if abilityCheck[1] != 0:
                            Menus.MaxAbilitiesStar.open_menu()
                            Menus.MaxAbilitiesStar.elements[
                                0].text = f"Star: {abilityCheck[1] - Abilities.abilities[6].numActivations}"
                            Menus.MaxAbilitiesStar.updateMenu()
                    if abilityCheck[0] == 'Summon Black Hole Ability':
                        if abilityCheck[1] != 0:
                            Menus.MaxAbilitiesBlackHole.open_menu()
                            Menus.MaxAbilitiesBlackHole.elements[
                                0].text = f"Black Hole: {abilityCheck[1] - Abilities.abilities[7].numActivations}"
                            Menus.MaxAbilitiesBlackHole.updateMenu()

            screen_centre_pos = [A.game_specs.SIZE[0] / 4, A.game_specs.SIZE[1] / 4]  # shows the center of the screen
            # A.pygame.draw.circle(A.game_specs.renderer.layers[0].display, [0, 0, 255], screen_centre_pos, 5)

            if A.selected_level == 1:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 1.5:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(0)
                if 1.5 < self.level_time < 2.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(1)
                if 2.5 < self.level_time < 3.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(2)
                if 3.5 < self.level_time < 4.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(3)
                if 4.5 < self.level_time < 5.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(4)
                if 5.5 < self.level_time < 6.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(5)
                if 6.5 < self.level_time < 8:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(6)

            if A.selected_level == 2:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 1.5:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(7)
                if 1.5 < self.level_time < 3.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(8)
                if 3.5 < self.level_time < 5.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(9)

            if A.selected_level == 3:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 1.5:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(11)
                if 1.5 < self.level_time < 3:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(12)
                if 3 < self.level_time < 4.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(13)

            if A.selected_level == 8:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 1.5:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(14)
                if 1.5 < self.level_time < 3:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(15)
                if 3 < self.level_time < 4.5:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(16)

            if A.selected_level == 11:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 1.5:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(17)
                if 1.5 < self.level_time < 3:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(18)

            if A.selected_level == 13:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 2:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(19)

            if A.selected_level == 14:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 2:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(20)

            if A.selected_level == 17:
                if self.level_time < .5:
                    Menus.Stars_Idle.open_menu()
                    Menus.Stars_Idle.updateMenu()
                if .5 < self.level_time < 2:
                    Menus.Stars_Idle.close_menu()

                    Menus.Stars_Talking_1.open_menu()
                    Menus.Stars_Talking_1.updateMenu()

                    ShowDialogue(21)
                if 2 < self.level_time < 3:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(22)
                if 3 < self.level_time < 4:
                    Menus.Stars_Talking_1.updateMenu()
                    ShowDialogue(23)

            A.game_specs.renderer.render_frame()

            A.game_specs.clock.tick(A.TPS)
            self.current_animation_frame = (self.current_animation_frame + 1) % len(self.animated_hand_star_frames)


A.game_specs = A.GameSpecs()
game = Game()

Abilities.abilities = Abilities.initialise_abilities(game)
game.run()
