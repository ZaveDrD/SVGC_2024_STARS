import random
import sys

import scripts.Actor as A  # This should initialise all game functions to be called THROUGH actor (A)


def start_game():
    while True:
        A.game_time += (A.TIME_CHANGE_PER_SECOND / A.TPS) * A.time_change_mult
        A.sim_time = A.game_time * A.SIM_TIME_EQUIVALENCE

        if not A.TRIPPY_MODE: A.screen.fill("#5a82c2")

        # Closes the application on quit
        for event in A.pygame.event.get():
            if event.type == A.pygame.QUIT:
                A.pygame.quit()
                sys.exit()

        keys = A.pygame.key.get_pressed()
        A.updateMovementParams(keys, A)

        for hand in A.convertCamHandsToScreenSpaceHands(A.hands):  # MAKE INTO STARS LATER
            for lm in hand:
                A.pygame.draw.circle(A.screen, [0, 0, 0], center=(lm[1], lm[2]), radius=10)

        # for gesture in gestures:  # DISPLAYS WHAT GESTURES ARE BEING DONE (alL gestures)
        #     gesturingHands = detect_vertebraeC6(hands, gestures[gesture])
        #     if len(gesturingHands) > 0:
        #         print(gesture, "Being Did'd by hands:", gesturingHands)

        pinchingHands = A.detect_vertebraeC6(A.convertCamHandsToScreenSpaceHands(A.hands), A.gestures['Pinch'])
        if len(pinchingHands) > 0:
            for planetaryBody in A.phys_sim.celestial_bodies:  # PINCH DETECTION TO GRAB PLANETS
                if planetaryBody.merged: continue
                for hand in pinchingHands:
                    if hand is None: break
                    if hand >= len(hands): break

                    pinchingHand = calcScreenSpaceLandmarks(hands[hand])
                    landmarkCoord = [pinchingHand[A.gestures['Pinch'][0][0][1]][1],
                                     pinchingHand[A.gestures['Pinch'][0][0][1]][2]]

                    bodyPos = [planetaryBody.px, planetaryBody.py]

                    if abs(math.dist(landmarkCoord, bodyPos)) <= planetaryBody.radius * A.player_zoom:
                        planetaryBody.set_pos([landmarkCoord[0], landmarkCoord[1]])

        planetSummoningHands = detect_vertebraeC6(convertCamHandsToScreenSpaceHands(hands), A.gestures['Summon Small Planet'])
        if len(planetSummoningHands) > 0:
            for planetaryBody in phys_sim.celestial_bodies:  # SUMMON PLANETS
                if planetaryBody.merged: continue
                for hand in planetSummoningHands:
                    if hand is None: break
                    if hand >= len(hands): break

                    summoningHand = calcScreenSpaceLandmarks(hands[hand])

                    landmarkCoord = [(summoningHand[9][1] + summoningHand[12][1]) / 2,
                                     (summoningHand[9][2] + summoningHand[12][2]) / 2]

                    planetPosPadding = 50
                    canPlaceBody = True

                    for body in phys_sim.celestial_bodies:
                        if planetaryBody.merged: continue

                        if body.px - planetPosPadding <= landmarkCoord[0] <= body.px + planetPosPadding and \
                                body.py - planetPosPadding <= landmarkCoord[1] <= body.py + planetPosPadding:
                            canPlaceBody = False
                            continue

                    if canPlaceBody:
                        body = CelestialBody('Small Planet',
                                             [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                                             2 * 10 ** 30 * 50, [landmarkCoord[0], landmarkCoord[1]])
                        phys_sim.add_object(body)
                    else:
                        print("TOO CLOSE TO SPAWN PLANET")

        phys_sim.applyForces(phys_sim.celestial_bodies)

        A.pygame.display.update()
        A.clock.tick(A.TPS)
