import pygame
import PhysicsSimulation
import atexit
import sys

atexit.register(lambda:[pygame.quit(), sys.exit()])
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])

distanceDivideConst = 10**10

class CelestialBody:
    def __init__(self, type, mass, force, pos, *args):
        self.type: str = type
        self.mass: float = mass
        self.force: float = force
        self.pos: float = pos
        self.x: float = pos[0]
        self.y: float = pos[1]

    def display(self):
        print(f"{(self.x) = }, {(self.y) = }")
        pygame.draw.circle(screen, "#000000", center=(self.x / distanceDivideConst, self.y / distanceDivideConst), radius=self.mass/10)


if __name__ == "__main__":
    celestial_bodies = [CelestialBody('', 5.97 * 10 ** 24, 0, [0, 0]),
                        CelestialBody('', 2 * 10 ** 30, 0, [149_600_000_000, 0]),
                        CelestialBody('', 10 ** 2, 0, [0, 50000])]

    phys_sim = PhysicsSimulation.PhysicsSim(celestial_bodies)

    while True:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
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
        for body in phys_sim.sadstuff:
            body.display()
        pygame.display.update()
