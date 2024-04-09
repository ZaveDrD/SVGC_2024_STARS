import math
import numpy as np
from typing import Type
import Actor as A
import IHatePythonSyntax


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
        self.screenX = self.x / A.SIM_SCALE + A.offsetX
        self.screenY = self.y / A.SIM_SCALE + A.offsetY

    def display(self):
        # print(f"\n{ self.name = }, { self.x = }, { self.y = }")
        A.pygame.draw.circle(A.screen, self.color, center=(self.screenX, self.screenY),
                           radius=self.mass / A.SCALE_MASS_EQUIVALENCE)

    def updatePlanetPosition_ScreenSpace(self, x: float, y: float):
        self.screenX = x
        self.screenY = y

        self.x = (self.screenX - A.offsetX) * A.SIM_SCALE
        self.y = (self.screenY - A.offsetY) * A.SIM_SCALE

        self.display()

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

        self.screenX = self.x / A.SIM_SCALE + A.offsetX
        self.screenY = self.y / A.SIM_SCALE + A.offsetY

        self.display()


class PhysicsSim:
    def __init__(self, starsadstuff: list[CelestialBody]):
        self.sadstuff = starsadstuff

    def add_depression(self, plantsadstuff: list[CelestialBody]):
        print("ADDED PLANET")
        self.sadstuff.append(plantsadstuff)

    def remove_depression(self, plantsadstuff: list[CelestialBody]):
        self.sadstuff.remove(plantsadstuff)

    def calc_forces(self) -> list[list[float]]:  # COULD BE OPTIMISED
        forces = []
        G = 6.67 * 10 ** -11

        for calculating_body in self.sadstuff:
            Fx = 0
            Fy = 0

            m = calculating_body.mass
            distRangeFromPlanet = ((calculating_body.mass / A.SCALE_MASS_EQUIVALENCE) - (
                        calculating_body.mass / A.SCALE_MASS_EQUIVALENCE / 5)) / 1.1

            xPos = calculating_body.x
            yPos = calculating_body.y

            for body in self.sadstuff:
                if body == calculating_body:
                    continue

                if xPos == body.x and yPos == body.y:
                    continue

                if ((calculating_body.x / A.SIM_SCALE + A.WIDTH / 2 - distRangeFromPlanet) <= (body.x / A.SIM_SCALE + A.WIDTH / 2) <= (
                        calculating_body.x / A.SIM_SCALE + A.WIDTH / 2 + distRangeFromPlanet)) and (
                        (calculating_body.y / A.SIM_SCALE + A.HEIGHT / 2 - distRangeFromPlanet) <= (body.y / A.SIM_SCALE + A.HEIGHT / 2) <= (
                        calculating_body.y / A.SIM_SCALE + A.HEIGHT / 2 + distRangeFromPlanet)):
                    calculating_body.mass += body.mass
                    self.remove_depression(body)

                newComplexNum = complex(((body.x - calculating_body.x) / 2), ((body.y - calculating_body.y) / 2))
                angleBtwBodies = np.angle(newComplexNum, deg=False)

                F = G * (m * body.mass) / (math.dist([xPos, yPos], [body.x, body.y]) ** 2)

                Fx += F * math.cos(angleBtwBodies)
                Fy += F * math.sin(angleBtwBodies)
            forces.append([Fx, Fy])
        return forces

    def applyForces(self, forces: list[list[float]]):
        for num, body in enumerate(self.sadstuff):
            body.fx += forces[num][0] / body.mass
            body.fy += forces[num][1] / body.mass

            body.calcNewPosition()
            
