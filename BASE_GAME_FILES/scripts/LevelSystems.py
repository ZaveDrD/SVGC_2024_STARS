import copy

import BASE_GAME_FILES.scripts.PhysicsSimulation as PhysicsSimulation
import BASE_GAME_FILES.scripts.Actor as A
import BASE_GAME_FILES.scripts.Player as P
import BASE_GAME_FILES.data.Assets as Assets

class Level:
    def __init__(self, levelName, bodies, playerStartPos, endGoalPos, abilityMaxActivations: list[tuple[str, int]] = None, isMenu=False, usePhysics=True):
        self.levelName = levelName
        self.isMenu = isMenu
        self.usePhysics = usePhysics
        self.initial_bodies = bodies

        self.playerStartPos = playerStartPos
        self.endGoalPos = endGoalPos

        self.abilityMaxActivation = abilityMaxActivations

        self.playerBody = None
        self.endGoal = None

        self.bodies = copy.deepcopy(self.initial_bodies)

        self.levelSaveState = None

        self.actorParams = []

    def loadSavedLevelState(self):
        if self.levelSaveState is not None:
            self.levelName = self.levelSaveState.levelName
            self.isMenu = self.levelSaveState.isMenu
            self.usePhysics = self.levelSaveState.usePhysics
            self.initial_bodies = self.levelSaveState.initial_bodies
            self.bodies = copy.deepcopy(self.levelSaveState.initial_bodies)
            self.playerBody = self.levelSaveState.playerBody
            self.actorParams = copy.deepcopy(self.levelSaveState.actorParams)
            self.abilityMaxActivation = copy.deepcopy(self.levelSaveState.abilityMaxActivation)

    def load_actor_level_data(self):
        A.player_view_pos_x, A.player_view_pos_y, A.player_zoom = self.actorParams[0], self.actorParams[1], self.actorParams[2]
        A.time_change_mult, A.sim_time, A.game_time = self.actorParams[3], self.actorParams[4], self.actorParams[5]


class LevelLoader:
    def __init__(self, levels: list[Level], startLevel=0):
        self.levels = levels

        self.GameEndObject = PhysicsSimulation.GravitationField(Assets.asset_dict['Black_Hole'][0], 10e14, [0, 0], interaction=False, static=True)

        self.currentLevelIndex = startLevel
        self.currentLevel = self.levels[self.currentLevelIndex]
        self.currentLevelPhysSim = None

    def saveCurrentLevelState(self):
        self.currentLevel.initial_bodies = copy.deepcopy(self.currentLevel.bodies)
        self.currentLevel.actorParams = copy.deepcopy([A.player_view_pos_x, A.player_view_pos_y, A.player_zoom, A.time_change_mult, A.sim_time, A.game_time])
        self.currentLevel.levelSaveState = self.currentLevel

    @staticmethod
    def reset_level_data():
        A.player_view_pos_x, A.player_view_pos_y, A.player_zoom = 0, 0, 1
        A.time_change_mult, A.sim_time, A.game_time = 1, 0, 0

    def load_level_index(self, levelIndex: int, saveState=False):
        if saveState:
            self.saveCurrentLevelState()
        else:
            self.currentLevel.bodies = copy.deepcopy(self.currentLevel.initial_bodies)
            self.currentLevel.playerBody = None
            self.currentLevel.endGoal = None

        self.currentLevel = self.levels[levelIndex]
        self.currentLevelIndex = levelIndex
        self.reset_level_data()

        if self.currentLevel.levelSaveState is not None:
            self.currentLevel.loadSavedLevelState()

        if len(self.currentLevel.actorParams) > 0:
            self.currentLevel.load_actor_level_data()

        if self.currentLevel.endGoal is None:
            self.currentLevel.endGoal = copy.deepcopy(self.GameEndObject)
            self.currentLevel.endGoal.set_pos(self.currentLevel.endGoalPos)
            self.currentLevel.bodies.append(self.currentLevel.endGoal)

        if self.currentLevel.playerBody is None:
            self.currentLevel.playerBody = P.Player(self.currentLevelPhysSim, self.currentLevel.endGoal, Assets.rand_key('Star'), 10e13, self.currentLevel.playerStartPos)
            self.currentLevel.bodies.append(self.currentLevel.playerBody)

        if self.currentLevel.usePhysics: self.currentLevelPhysSim = PhysicsSimulation.PhysicsSim(self.currentLevel.bodies)
        self.currentLevel.playerBody.updatePhys(self.currentLevelPhysSim)

        A.selected_level = levelIndex+1

    def load_level_name(self, levelName: str, saveState=False):
        for levelIndex, level in enumerate(self.levels):
            if level.levelName == levelName:
                self.load_level_index(levelIndex, saveState)

    def load_level(self, level: Level, saveState=False):
        for levelIndex, e_level in enumerate(self.levels):
            if level == e_level:
                self.load_level_index(levelIndex, saveState)

    def add_level(self, level: Level):
        self.levels.append(level)

    def remove_level(self, level_index):
        self.levels.remove(self.levels[level_index])

    def reload_level(self):
        self.load_level_index(self.currentLevelIndex)

    def get_current_level(self) -> tuple:
        return self.currentLevel, self.currentLevelIndex
