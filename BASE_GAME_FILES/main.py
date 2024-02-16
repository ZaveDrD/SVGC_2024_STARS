import pygame
import PhysicsSimulation
import atexit
import sys
import Actor as A

atexit.register(lambda: [pygame.quit(), sys.exit()])

pygame.display.init()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150
screen = pygame.display.set_mode([WIDTH, HEIGHT])

A.WIDTH, A.HEIGHT = WIDTH, HEIGHT


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
        pygame.draw.circle(screen, self.color, center=(self.x / A.SIM_SCALE + WIDTH / 2 + A.offsetX, self.y / A.SIM_SCALE + HEIGHT / 2 + A.offsetY), radius=self.mass / A.SCALE_MASS_EQUIVALENCE)

    def calcNewPosition(self):
        deltaT = A.TIME_INC

        self.ax = self.fx / self.mass
        self.ay = self.fy / self.mass

        # acc = deltaV / deltaT ... deltaV = acc * deltaT

        self.vx += self.ax * deltaT
        self.vy += self.ay * deltaT

        # deltaV = deltaX / deltaT ... deltaX = deltaV * deltaT

        self.x += self.vx * deltaT
        self.y += self.vy * deltaT

        # print(f"\n{ self.name = }, \nPOSITIONS: { self.x = }, { self.y = }, \nVELOCITIES: { self.vx = }, { self.vy }, \nACCELERATION: { self.ax }, { self.ay }, \nFORCES: { self.fx = }, { self.fy }")
        self.display()


if __name__ == "__main__":
    celestial_bodies = [
        CelestialBody('SUN 2', [255, 255, 255], "", 2 * 10 ** 30 * 100, [0, 0], [0, 0], [0, 0], [0, 4000000000000]),
        CelestialBody('SUN 1', [0, 0, 0], "", 2 * 10 ** 30, [0, 0], [0, 0], [-5 * 10 ** -10, 0], [0, -2000000000000])
    ]

    phys_sim = PhysicsSimulation.PhysicsSim(celestial_bodies)

    while True:
        print(A.handPositions)

        A.TIME_INC = A.DEFAULT_TIME_INC * A.time_mult
        A.current_time += A.TIME_INC

        A.SIM_SCALE = A.DEFAULT_SIM_SCALE * A.zoom
        A.SCALE_MASS_EQUIVALENCE = A.DEFAULT_SCALE_MASS_EQUIVALENCE * A.zoom

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            A.offsetY += A.moveControlSpeed
        if keys[pygame.K_DOWN]:
            A.offsetY -= A.moveControlSpeed
        if keys[pygame.K_LEFT]:
            A.offsetX += A.moveControlSpeed
        if keys[pygame.K_RIGHT]:
            A.offsetX -= A.moveControlSpeed

        if keys[pygame.K_EQUALS]:
            if A.zoom - A.zoomInc > 0:
                A.zoom -= A.zoomInc
            else:
                A.zoom = 10 ** -10
        if keys[pygame.K_MINUS]:
            A.zoom += A.zoomInc

        if keys[pygame.K_LEFTBRACKET]:
            A.time_mult -= A.TIME_MULT_INC
        if keys[pygame.K_RIGHTBRACKET]:
            A.time_mult += A.TIME_MULT_INC

        screen.fill("#5a82c2")

        for handNum in range(0, len(A.handPositions)):
            for lm in range(0, len(A.handPositions[handNum])):
                # for lm_other in range(0, len(currentFrameHandLandmarks[handNum])):
                #     if lm == 0 and lm_other == (1 or 5 or 9 or 13 or 17):
                #         pygame.draw.line(screen, [255, 255, 255], [currentFrameHandLandmarks[handNum][lm][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm][2] * 3 - HEIGHT / 4], [currentFrameHandLandmarks[handNum][lm_other][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm_other][2] * 3 - HEIGHT / 4], 5)

                pygame.draw.circle(screen, [0, 0, 0], center=(
                    A.handPositions[handNum][lm][1] * -2 + .9 * WIDTH,
                    A.handPositions[handNum][lm][2] * 2 - HEIGHT / 2), radius=10)

        phys_sim.applyForces(phys_sim.calc_forces())

        pygame.display.update()
