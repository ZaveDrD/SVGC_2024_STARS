import pygame
import PhysicsSimulation
import atexit
import sys

atexit.register(lambda: [pygame.quit(), sys.exit()])

pygame.display.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150

screen = pygame.display.set_mode([WIDTH, HEIGHT])

DEFAULT_SIM_SCALE = 10 ** 10 * 3
DEFAULT_SCALE_MASS_EQUIVALENCE = 10 ** 28 * 150

SIM_SCALE = DEFAULT_SIM_SCALE
SCALE_MASS_EQUIVALENCE = DEFAULT_SCALE_MASS_EQUIVALENCE

offsetX, offsetY = 0, 0
moveControlSpeed = 0.5

zoom = 1
zoomInc = 1 * 10 ** -3

current_time = 0
DEFAULT_TIME_INC = 1 * 10 ** 17

TIME_INC = DEFAULT_TIME_INC
time_mult = 1
TIME_MULT_INC = 10 ** -2


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
        pygame.draw.circle(screen, self.color, center=(self.x / SIM_SCALE + WIDTH / 2 + offsetX, self.y / SIM_SCALE + HEIGHT / 2 + offsetY), radius=self.mass / SCALE_MASS_EQUIVALENCE)

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

        print(f"\n{ self.name = }, \nPOSITIONS: { self.x = }, { self.y = }, \nVELOCITIES: { self.vx = }, { self.vy }, \nACCELERATION: { self.ax }, { self.ay }, \nFORCES: { self.fx = }, { self.fy }")
        self.display()


if __name__ == "__main__":
    celestial_bodies = [
            CelestialBody('SUN 2', [255, 255, 255], "", 2 * 10 ** 30 * 100, [0, 0], [0, 0], [0, 0], [0, 4000000000000]),
            CelestialBody('SUN 1', [0, 0, 0], "", 2 * 10 ** 30, [0, 0], [0, 0], [-5 * 10 ** -10, 0], [0, -2000000000000]),
                        ]

                        # CelestialBody('SUN', "", 2 * 10 ** 30, 0, [149_600_000_000, 0]),
                        # CelestialBody('EARTH', "", 5.97 * 10 ** 24, 0, [0, 0])

    phys_sim = PhysicsSimulation.PhysicsSim(celestial_bodies)

    while True:
        TIME_INC = DEFAULT_TIME_INC * time_mult
        current_time += TIME_INC

        SIM_SCALE = DEFAULT_SIM_SCALE * zoom
        SCALE_MASS_EQUIVALENCE = DEFAULT_SCALE_MASS_EQUIVALENCE * zoom

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            offsetY += moveControlSpeed
        if keys[pygame.K_DOWN]:
            offsetY -= moveControlSpeed
        if keys[pygame.K_LEFT]:
            offsetX += moveControlSpeed
        if keys[pygame.K_RIGHT]:
            offsetX -= moveControlSpeed

        if keys[pygame.K_EQUALS]:
            if zoom - zoomInc > 0:
                zoom -= zoomInc
            else:
                zoom = 10 ** -10
        if keys[pygame.K_MINUS]:
            zoom += zoomInc

        if keys[pygame.K_LEFTBRACKET]:
            time_mult -= TIME_MULT_INC
        if keys[pygame.K_RIGHTBRACKET]:
            time_mult += TIME_MULT_INC

        screen.fill("#5a82c2")

        phys_sim.applyForces(phys_sim.calc_forces())

        pygame.display.update()
