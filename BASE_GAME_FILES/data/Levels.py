import random

from BASE_GAME_FILES.scripts.LevelSystems import Level
import BASE_GAME_FILES.scripts.PhysicsSimulation as PhysicsSimulation


def GenRandBodies(numBodies: int, min_x: int = -5000, max_x: int = 5000, min_y: int = -5000, max_y: int = 5000,
                  color: list[int] = [255, 255, 255]) -> list[PhysicsSimulation.CelestialBody]:
    bodies = []
    for i in range(0, numBodies):
        bodies.append(PhysicsSimulation.CelestialBody(color, 10 ** (random.randint(12, 15)),
                                    [random.randint(min_x, max_x), random.randint(min_y, max_y)]))
    return bodies


level_1_bodies = GenRandBodies(200, color=[255, 255, 255])  # TESTNG PHYSICS SYSTEM FOR NOW

levels = [
    Level("Level0", [
        PhysicsSimulation.CelestialBody([255, 255, 255], 10e15, [0, 0])
    ]),
    Level("Level0", level_1_bodies)
]