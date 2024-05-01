import BASE_GAME_FILES.scripts.PhysicsSimulation as PhysSim
import BASE_GAME_FILES.scripts.Actor as A


class Player(PhysSim.CelestialBody):
    def __init__(self, phys_sim: PhysSim.PhysicsSim, endPos, color, mass, pos: list[float], *args):
        super().__init__(color, mass, pos, *args)
        self.endPosX: float = endPos[0]
        self.endPosY: float = endPos[1]
        self.phys_sim = phys_sim

    def updatePhys(self, phys_sim):
        self.phys_sim = phys_sim

    def drawPath(self, prediction_length=2):
        x0, y0, vx0, vy0 = self.x, self.y, self.vx, self.vy
        for i in range(prediction_length):
            x, y = x0, y0
            x0, y0, vx0, vy0 = self.phys_sim.predict_path(self, [vx0, vy0], [x, y])

            # print("x:", x, x0, "\ny:", y, y0, "\nPrediction no.", i, "\n")

            px, py = PhysSim.CelestialBody.conv_x_to_px(x, y)
            px0, py0 = PhysSim.CelestialBody.conv_x_to_px(x0, y0)

            A.pygame.draw.line(A.game_specs.display, [0, 255, 0], [px, py], [px0, py0])

    def checkForLevelEnd(self):
        print("IDK")

    def checkForPlayerDeath(self):
        if self.merged:
            print("DEAD")

