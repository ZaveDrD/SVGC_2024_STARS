import pygame
import PhysicsSimulation
import atexit
import sys

atexit.register(lambda:[pygame.quit(), sys.exit()])

pygame.display.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150

screen = pygame.display.set_mode([WIDTH, HEIGHT])

SIM_SCALE = 10 ** 10 * 30
SCALE_MASS_EQUIVALENCE = 10 ** 28 * 1000

current_time = 0
TIME_INC = 1 * 10 ** 19


class CelestialBody:
    def __init__(self, name, color, bodyType, mass, force, acceleration, velocity, pos, *args):
        self.name: str = name
        self.color: list[int] = color
        self.type: str = bodyType
        self.mass: float = mass
        self.force: float = force
        self.acceleration: float = acceleration
        self.velocity: float = velocity
        self.pos: float = pos
        self.x: float = pos[0]
        self.y: float = pos[1]
        self.fx: float = force[0]
        self.fy: float = force[1]
        self.ax = acceleration[0]
        self.ay = acceleration[1]
        self.vx = velocity[0]
        self.vy = velocity[1]

    def display(self):
        # print(f"\n{ self.name = }, { self.x = }, { self.y = }")
        pygame.draw.circle(screen, self.color, center=(self.x / SIM_SCALE + WIDTH / 2, self.y / SIM_SCALE + HEIGHT / 2), radius=self.mass / SCALE_MASS_EQUIVALENCE)

    def calcNewPosition(self):
        deltaT = TIME_INC

        self.ax = self.fx / self.mass
        self.ay = self.fy / self.mass

        # acc = deltaV / deltaT ... deltaV = acc * deltaT

        self.vx += self.ax * deltaT
        self.vy += self.ay * deltaT

        # deltaV = deltaX / deltaT ... deltaX = deltaV * deltaT

        self.x += self.vx * deltaT
        self.y += self.vy * deltaT

        self.display()


if __name__ == "__main__":
    celestial_bodies = [
                        CelestialBody('SUN 2', [255, 255, 255], "", 2 * 10 ** 30 * 50, [0, 0], [0, 0], [5 * 10 ** -10, 0], [0, 4000000000000]),
                        CelestialBody('SUN 1', [255, 255, 255], "", 2 * 10 ** 30 * 50, [0, 0], [0, 0], [-5 * 10 ** -10, 0], [0, -4000000000000]),
                        # CelestialBody('100kg Ball', [0, 0, 0], "", 5.97 * 10 ** 29, [0, 0], [0, 0], [0, 0], [0, 0])
                        ]

                        # CelestialBody('SUN', "", 2 * 10 ** 30, 0, [149_600_000_000, 0]),
                        # CelestialBody('EARTH', "", 5.97 * 10 ** 24, 0, [0, 0])

    phys_sim = PhysicsSimulation.PhysicsSim(celestial_bodies)

    while True:
        current_time += TIME_INC

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_UP]:
        #     circle[1] -= 0.05
        # if keys[pygame.K_DOWN]:
        #     circle[1] += 0.05
        # if keys[pygame.K_LEFT]:
        #     circle[0] -= 0.05
        # if keys[pygame.K_RIGHT]:
        #     circle[0] += 0.05

        screen.fill("#5a82c2")

        phys_sim.applyForces(phys_sim.calc_forces())

        pygame.display.update()
