import random

from BASE_GAME_FILES.scripts.LevelSystems import Level
import BASE_GAME_FILES.scripts.PhysicsSimulation as PhysicsSimulation
import BASE_GAME_FILES.data.Assets as assets


def GenRandBodies(numBodies: int, min_x: int = -5000, max_x: int = 5000, min_y: int = -5000, max_y: int = 5000) -> list[
    PhysicsSimulation.Planet]:
    bodies = []
    for i in range(0, numBodies):
        bodies.append(PhysicsSimulation.Planet(assets.rand_key('Planet'), 10 ** (random.randint(12, 15)),
                                               [random.randint(min_x, max_x), random.randint(min_y, max_y)]))
    return bodies


levels = []


def Init_Level_Data():
    level_1_bodies = GenRandBodies(200)  # TESTNG PHYSICS SYSTEM FOR NOW

    _levels = [
        Level("Time Control / Intro", [
            PhysicsSimulation.Planet(assets.rand_key('Star'), 10e14, [700, 200]),
        ],
              playerStartPos=[100, 200],
              endGoalPos=[500, 200],
              ),
        Level("Movement", [
            PhysicsSimulation.Planet(assets.rand_key('Star'), 10e14, [1300, 700]),
        ],
              playerStartPos=[600, 700],
              endGoalPos=[1000, 700],
              ),
        Level("Pinch 1", [
            PhysicsSimulation.Planet(assets.rand_key('Star'), 10e14, [500, 200]),
        ],
              playerStartPos=[100, 200],
              endGoalPos=[700, 200],
              ),
        Level("Pinch 2", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [500, 200]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 15e14, [350, 400]),
        ],
              playerStartPos=[300, 300],
              endGoalPos=[800, 100],
              ),
        Level("Pinch 3", [
            PhysicsSimulation.Planet(assets.rand_key('Star'), 10e14, [200, 300], interaction=False, collidable=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 15e14, [400, 200]),
        ],
              playerStartPos=[400, 600],
              endGoalPos=[400, -200],
              ),
        Level("Pinch 4", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [550, 450], interaction=False, collidable=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [250, 450], interaction=False, collidable=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 2e14, [325, 525], interaction=False, collidable=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 2e14, [475, 525], interaction=False, collidable=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e15, [400, 300]),
        ],
              playerStartPos=[400, 100],
              endGoalPos=[400, 600],
              ),
        Level("Pinch 5", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [700, 0], velocity=[-.10, 0]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [-100, 600], velocity=[.10, 0]),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e15, [0, 100]),
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 10e18, [700, 400], interaction=False),
        ],
              playerStartPos=[400, 300],
              endGoalPos=[-100, 0],
              ),
        Level("Summon Planet 1", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [400, -100], interaction=False),
        ],
              playerStartPos=[400, 500],
              endGoalPos=[200, -100],
              abilityMaxActivations=[('Summon Planet Ability', 2)]
              ),
        Level("Summon Planet 2", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 30e14, [200, 400], interaction=False, collidable=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [600, 400], interaction=False, collidable=False),
        ],
              playerStartPos=[400, 400],
              endGoalPos=[500, 400],
              abilityMaxActivations=[('Summon Planet Ability', 3)]
              ),
        Level("Summon Planet 3", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [550, 350]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [250, 350]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [500, 500]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [300, 500]),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [400, 250]),
            PhysicsSimulation.Star(assets.rand_key('Star'), 40e14, [700, 200], velocity=[0, .05], interaction=False,
                                   collidable=False),
        ],
              playerStartPos=[400, 400],
              endGoalPos=[700, 450],
              abilityMaxActivations=[('Summon Planet Ability', 1)]
              ),
        Level("Summon Star 1", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [400, 400], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 400],
              abilityMaxActivations=[('Summon Planet Ability', 1),
                                     ('Summon Star Ability', 1)]
              ),
        Level("Summon Star 2", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 50e17, [450, 400], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 400],
              abilityMaxActivations=[('Summon Planet Ability', 1),
                                     ('Summon Star Ability', 4)]
              ),
        Level("Summon Black Hole", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [200, 300], velocity=[.1, -.1],
                                     interaction=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 7e14, [700, 200], velocity=[-.1, .1],
                                     interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [250, 400], velocity=[.05, .05], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [500, 300], velocity=[-.05, .05], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 15e15, [450, 200], velocity=[0, -.05], interaction=False),
        ],
              playerStartPos=[400, 700],
              endGoalPos=[400, 100],
              abilityMaxActivations=[('Summon Black Hole Ability', 1)]
              ),
        Level("Enlarge 1", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [400, 400], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 5e16, [700, 400], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 400],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Enlarge 2", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 50e16, [750, 300], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [750, 500], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 300],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Enlarge 3", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [400, 400], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [300, 200]),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 400],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Shrink 1", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 5e16, [400, 400], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [700, 400], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 400],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Shrink 2", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [400, 550], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [400, 250], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [550, 400], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e16, [250, 400], interaction=False),
        ],
              playerStartPos=[600, 0],
              endGoalPos=[400, 400],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Shrink 3", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 50e17, [900, 0], interaction=False),
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 50e18, [900, 500], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[600, 300],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 1", [
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 10e17, [200, 800], interaction=True),
        ],
              playerStartPos=[400, 700],
              endGoalPos=[400, 100],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 2", [
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 50e16, [200, 100], velocity=[0.1, -0.1],
                                     interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [600, 300], interaction=False),
        ],
              playerStartPos=[100, 500],
              endGoalPos=[100, 100],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 1),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 3", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [350, -100], interaction=False),
        ],
              playerStartPos=[400, 600],
              endGoalPos=[200, 500],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 1),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 4", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [280, 500], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [580, 500], interaction=False),
        ],
              playerStartPos=[400, 400],
              endGoalPos=[300, 500],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 2),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 5", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 20e17, [500, 500], interaction=False),
            PhysicsSimulation.Star(assets.rand_key('Star'), 10e17, [550, 200], interaction=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [300, 250], interaction=False),
            PhysicsSimulation.Planet(assets.rand_key('Planet'), 10e14, [700, 300], interaction=False),
        ],
              playerStartPos=[200, 400],
              endGoalPos=[800, 200],
              abilityMaxActivations=[('Summon Planet Ability', 2),
                                     ('Summon Star Ability', 2),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 6", [
            PhysicsSimulation.Star(assets.rand_key('Star'), 75e17, [400, 200], interaction=False),
        ],
              playerStartPos=[300, 400],
              endGoalPos=[0, -100],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 1),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 7", [
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 75e17, [500, 400], interaction=False),
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 75e17, [300, 400], interaction=False),
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 75e17, [400, 500], interaction=False),
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 75e17, [400, 300], interaction=False),
        ],
              playerStartPos=[600, 300],
              endGoalPos=[400, 400],
              abilityMaxActivations=[('Summon Planet Ability', 0),
                                     ('Summon Star Ability', 0),
                                     ('Summon Black Hole Ability', 0)]
              ),
        Level("Mixed 8", [
            PhysicsSimulation.BlackHole(assets.rand_key('Black_Hole'), 75e18, [300, -100], velocity=[0, 0.3],
                                        interaction=False),
        ],
              playerStartPos=[600, 400],
              endGoalPos=[100, 400],
              abilityMaxActivations=[('Summon Planet Ability', 1),
                                     ('Summon Star Ability', 1),
                                     ('Summon Black Hole Ability', 1)]
              ),
        Level("Random Level",
              GenRandBodies(200),
              playerStartPos=[random.randint(-400, 1000), random.randint(-400, 1000)],
              endGoalPos=[random.randint(-400, 1000), random.randint(-400, 1000)],
              abilityMaxActivations=[('Summon Planet Ability', random.randint(0, 5)),
                                     ('Summon Star Ability', random.randint(0, 5)),
                                     ('Summon Black Hole Ability',
                                      random.randint(0, 5))]
              )
    ]

    return _levels
