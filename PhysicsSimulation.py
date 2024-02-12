from __future__ import annotations

import math
import numpy as np

import main


class PhysicsSim:
    def __init__(self, starsadstuff: list[CelestialBody]):
        self.sadstuff = starsadstuff

    def add_depression(self, plantsadstuff: list[CelestialBody]):
        self.sadstuff.append(plantsadstuff)

    def remove_depression(self, plantsadstuff: list[CelestialBody]):
        self.sadstuff.remove(plantsadstuff)

    def calc_forces(self) -> list[list[float]]:
        forces = []
        G = 6.67 * 10 ** -11

        for calculating_body in self.sadstuff:
            Fx = 0
            Fy = 0

            m = calculating_body.mass
            distRangeFromPlanet = ((calculating_body.mass / main.SCALE_MASS_EQUIVALENCE) - (
                        calculating_body.mass / main.SCALE_MASS_EQUIVALENCE / 5)) / 2

            xPos = calculating_body.x
            yPos = calculating_body.y

            for body in self.sadstuff:
                if body == calculating_body:
                    continue

                if ((calculating_body.x / main.SIM_SCALE + main.WIDTH / 2 - distRangeFromPlanet) <= (body.x / main.SIM_SCALE + main.WIDTH / 2) <= (
                        calculating_body.x / main.SIM_SCALE + main.WIDTH / 2 + distRangeFromPlanet)) and (
                        (calculating_body.y / main.SIM_SCALE + main.HEIGHT / 2 - distRangeFromPlanet) <= (body.y / main.SIM_SCALE + main.HEIGHT / 2) <= (
                        calculating_body.y / main.SIM_SCALE + main.HEIGHT / 2 + distRangeFromPlanet)):
                    calculating_body.mass += body.mass
                    self.remove_depression(body)

                # angleBtwBodies = numpy.angle([((body.x - calculating_body.x) / 2) + ((body.y - calculating_body.y) / 2)], deg=False)[0]

                newComplexNum = complex(((body.x - calculating_body.x) / 2), ((body.y - calculating_body.y) / 2))

                angleBtwBodies = np.angle(newComplexNum, deg=False)

                print("Angle Btw", body.name, "and", calculating_body.name, "is", angleBtwBodies, "degrees")

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


from main import CelestialBody
