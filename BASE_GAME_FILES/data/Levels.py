import random

from BASE_GAME_FILES.scripts.LevelSystems import Level
import BASE_GAME_FILES.scripts.PhysicsSimulation as PhysicsSimulation
import BASE_GAME_FILES.data.Assets as assets


def GenRandBodies(numBodies: int, min_x: int = -5000, max_x: int = 5000, min_y: int = -5000, max_y: int = 5000) -> list[PhysicsSimulation.Planet]:
    bodies = []
    for i in range(0, numBodies):
        bodies.append(PhysicsSimulation.Planet(assets.rand_key('Planet'), 10 ** (random.randint(12, 15)),
                                                      [random.randint(min_x, max_x), random.randint(min_y, max_y)]))
    return bodies


levels = []


def Init_Level_Data():
    level_1_bodies = GenRandBodies(200)  # TESTNG PHYSICS SYSTEM FOR NOW

    _levels = [
        Level("Level0", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e15, [0, 0]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e15, [1000, 0])
        ],
              playerStartPos=[500, 500],
              endGoalPos=[500, -500],
        ),
        Level("Level1", level_1_bodies, playerStartPos=[0, 0], endGoalPos=[250, 250])
    ]

    return _levels
