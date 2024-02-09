from __future__ import annotations

import math
import numpy

class PhysicsSim:
    def __init__(self, starsadstuff):
        self.sadstuff = starsadstuff

    def add_depression(self, plantsadstuff : list[CelestialBody]):
        self.sadstuff.append(plantsadstuff)

    def calc_forces(self) -> list[list[float]]:
        forces = []
        G = 6.67 * 10 ** -11

        for calculating_body in self.sadstuff:
            Fx = 0
            Fy = 0

            m = calculating_body.mass

            xPos = calculating_body.x
            yPos = calculating_body.y

            for body in self.sadstuff:
                if body == calculating_body:
                    continue

                try:
                    angleBtwBodies = math.atan((body.y - calculating_body.y) / (body.x - calculating_body.x))
                except:
                    angleBtwBodies = math.pi/2 * (-1 if (body.y - calculating_body.y) < 0 else 1)

                GMm = G * (m * body.mass)

                try:
                    F = GMm / ((math.dist([xPos, yPos], [body.x, body.y])/2) ** 2)
                except ZeroDivisionError:
                    F = 0  # ABSORB MASSES IN DA FUTURE

                Fx += F * math.cos(angleBtwBodies)
                Fy += F * math.sin(angleBtwBodies)
            forces.append([Fx, Fy])
        return forces

    def applyForces(self, forces: list[list[float]]):
        for num, body in enumerate(self.sadstuff):
            body.x += forces[num][0] / body.mass
            body.y += forces[num][1] / body.mass

            body.display()


from main import CelestialBody