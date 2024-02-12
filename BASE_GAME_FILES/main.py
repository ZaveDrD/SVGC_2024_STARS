import pygame
import atexit
import sys
import cv2
import HandTracking.HandTrackingModule as htm
import consts


# Setup
atexit.register(lambda: [pygame.quit(), sys.exit()])
pygame.display.init()


# Variables
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0][0] - 50, pygame.display.get_desktop_sizes()[0][1] - 150

screen = pygame.display.set_mode([WIDTH, HEIGHT])

scale_mass_equivalence = consts.DEFAULT_SCALE_MASS_EQUIVALENCE
sim_scale = consts.DEFAULT_SIM_SCALE

offsetX, offsetY = 0, 0
moveControlSpeed = 1

zoom = 1
zoomInc = 1 * 10 ** -3

time_inc = consts.DEFAULT_TIME_INC
current_time = 0
time_mult = 1


class CelestialBody:
    """
    # CelestialBody
    A class for all celestial bodies including stars, planets etc. This class can be used for
    tracking their movement and forces acting upon them.
    """
    def __init__(self, name: str, color: list[int] | str, bodyType: str, mass: float, force: list[float], 
                 acceleration: list[float], velocity: list[float], pos: list[float], *args) -> None:
        """
        ## Params
        ### name
            (str) The type of celestial body; star, planet, moon, asteroid etc.]
        ### color
            (str | list[int]) The color of the body, either in hex or rgb. Used when displaying the body.
        ### bodyType
            (str) I have no idea what this does; need to ask Zave
        ### mass
            (float) The mass of the body in kilograms
        ### force
            (float[]) The force currently acting on the object in newtons. First element is x, second
                      is y. Positive is up and right, negative is left and down.
        ### acceleration
            (float[]) The acceleration of the object; First element is y, second is x. Positive is up and
                       left, negative is down and right
        ### velocity
            (float[]) The velocity of the object; First element is y, second is x. Positive is up and
                       left, negative is down and right
        ### pos
            (float[]) The position of the object; First element is y, second is x.
        """
        if isinstance(color, str):
            color = [int(color.replace('#', '')[i:i+2], 16) for i in range(0, 6, 2)]
        self.name: str = name
        self.color: list[int] = color
        self.type: str = bodyType
        self.mass: float = mass
        self.force: list[float] = force
        self.acceleration: list[float] = acceleration
        self.velocity: list[float] = velocity
        self.pos: list[float] = pos
        self.x: float = pos[0]
        self.y: float = pos[1]
        self.fx: float = force[0]
        self.fy: float = force[1]
        self.ax: float = acceleration[0]
        self.ay: float = acceleration[1]
        self.vx: float = velocity[0]
        self.vy: float = velocity[1]

    def display(self) -> None:
        """
        Draws the body to the screen as a circle
        """
        # print(f"\n{ self.name = }, { self.x = }, { self.y = }")
        pygame.draw.circle(screen, self.color, center=(self.x / sim_scale + WIDTH / 2 + offsetX, self.y / sim_scale + HEIGHT / 2 + offsetY), radius=self.mass / scale_mass_equivalence)

    def calcNewPosition(self, display: bool = True) -> None:
        """
        Calculates position of the object 1 frame (unit of time) later. Changes are based on velocity,
        acceleration and force.
        ## Params
        ### display
                (bool) True by default. If true, the object will be drawn after calculations, otherwise it will
                       not
        """
        deltaT = time_inc

        self.ax = self.fx / self.mass
        self.ay = self.fy / self.mass

        # acc = deltaV / deltaT ... deltaV = acc * deltaT

        self.vx += self.ax * deltaT
        self.vy += self.ay * deltaT

        # deltaV = deltaX / deltaT ... deltaX = deltaV * deltaT

        self.x += self.vx * deltaT
        self.y += self.vy * deltaT

        # print(f"\n{ self.name = }, \nPOSITIONS: { self.x = }, { self.y = }, \nVELOCITIES: { self.vx = }, { self.vy }, \nACCELERATION: { self.ax }, { self.ay }, \nFORCES: { self.fx = }, { self.fy }")
        if display:
            self.display()


if __name__ == "__main__":
    import PhysicsSimulation
    cap = cv2.VideoCapture(0)
    handDetector = htm.HandDetector()

    celestial_bodies = [
            CelestialBody('SUN 2', [255, 255, 255], "", 2 * 10 ** 30 * 100, [0, 0], [0, 0], [0, 0], [0, 4000000000000]),
            CelestialBody('SUN 1', [0, 0, 0], "", 2 * 10 ** 30, [0, 0], [0, 0], [-5 * 10 ** -10, 0], [0, -2000000000000]),
                        ]

                        # CelestialBody('SUN', "", 2 * 10 ** 30, 0, [149_600_000_000, 0]),
                        # CelestialBody('EARTH', "", 5.97 * 10 ** 24, 0, [0, 0])

    phys_sim = PhysicsSimulation.PhysicsSim(celestial_bodies)
    prevFrameHandLandmarks = []

    while True:
        success, img = cap.read()

        img = handDetector.FindHands(img)
        currentFrameHandLandmarks = handDetector.ConstructLandmarkList(img)

        time_inc = consts.DEFAULT_TIME_INC * time_mult
        current_time += time_inc

        sim_scale = consts.DEFAULT_SIM_SCALE * zoom
        scale_mass_equivalence = consts.DEFAULT_SCALE_MASS_EQUIVALENCE * zoom

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
            time_mult -= consts.TIME_MULT_INC
        if keys[pygame.K_RIGHTBRACKET]:
            time_mult += consts.TIME_MULT_INC

        screen.fill("#5a82c2")

        phys_sim.applyForces(phys_sim.calc_forces())

        for handNum in range(0, len(currentFrameHandLandmarks)):
            for lm in range(0, len(currentFrameHandLandmarks[handNum])):
                try:
                    if -20 < (prevFrameHandLandmarks[handNum][lm][1] - currentFrameHandLandmarks[handNum][lm][1]) < 20:
                        currentFrameHandLandmarks[handNum][lm][1] = prevFrameHandLandmarks[handNum][lm][1]
                except:
                    print("Error: Non Existant Point On Hand")

                for lm_other in range(0, len(currentFrameHandLandmarks[handNum])):
                    if lm == 0 and lm_other == (1 or 5 or 9 or 13 or 17):
                        pygame.draw.line(screen, [255, 255, 255], [currentFrameHandLandmarks[handNum][lm][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm][2] * 3 - HEIGHT / 4], [currentFrameHandLandmarks[handNum][lm_other][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm_other][2] * 3 - HEIGHT / 4], 5)

                pygame.draw.circle(screen, [0, 0, 0], center=(currentFrameHandLandmarks[handNum][lm][1] * -3 + 1.2 * WIDTH, currentFrameHandLandmarks[handNum][lm][2] * 3 - HEIGHT / 4), radius=10)

        prevFrameHandLandmarks = currentFrameHandLandmarks


        pygame.display.update()
