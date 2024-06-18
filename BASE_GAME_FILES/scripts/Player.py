import BASE_GAME_FILES.scripts.PhysicsSimulation as PhysSim
import BASE_GAME_FILES.scripts.Actor as A


class Player(PhysSim.Spacecraft):
    def __init__(self, phys_sim: PhysSim.PhysicsSim, endGoal: PhysSim.CelestialBody, img, mass, pos: list[float], velocity: list[float] = [0, 0], acceleration: list[float] = [0, 0],
                 start_force: list[int] = [0, 0], static=False, interaction=True, *args):
        super().__init__(img, mass, pos, velocity, acceleration, start_force, static, interaction)
        self.interaction = False
        self.static = False
        self.phys_sim = phys_sim
        self.endGoal = endGoal

        self.alive = True

    def updatePhys(self, phys_sim):
        self.phys_sim = phys_sim

    def drawPath(self, prediction_length=2):
        x0, y0, vx0, vy0 = self.x, self.y, self.vx, self.vy
        for i in range(prediction_length):
            x, y = x0, y0
            x0, y0, vx0, vy0 = self.phys_sim.predict_path(self, [vx0, vy0], [x, y])

            # print("x:", x, x0, "\ny:", y, y0, "\nPrediction no.", i, "\n")

            px, py = PhysSim.CelestialBody.conv_x_to_px(0, x, y)
            px0, py0 = PhysSim.CelestialBody.conv_x_to_px(0, x0, y0)

            A.pygame.draw.line(A.game_specs.renderer.layers[0].display, [0, 255, 0], [px, py], [px0, py0])

    def checkForLevelEnd(self):
        if self.merged and self.merged_to == self.endGoal:
            print("WIN")

    def checkForPlayerDeath(self):
        if self.merged and self.merged_to != self.endGoal:
            self.alive = False
            print("DEAD")

