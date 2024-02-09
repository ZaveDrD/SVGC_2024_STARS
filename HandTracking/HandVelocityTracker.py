from math import sqrt
import cv2
import mediapipe as mp
import HandTrackingModule as htm
import time


def main():
    prevTime = 0
    currentTime = 0

    prevFrameHandLandmarks = []
    currentFrameHandLandmarks = []

    cap = cv2.VideoCapture(0)

    handDetector = htm.HandDetector()

    while True:
        success, img = cap.read()

        img = handDetector.FindHands(img)
        # lmList = handDetector.FindLandmarksForHand(img)
        #
        # if len(lmList) != 0:
        #     print(lmList[0])

        currentTime = time.time()
        timeDif = (currentTime - prevTime)
        fps = 1 / timeDif
        prevTime = currentTime

        currentFrameHandLandmarks = handDetector.ConstructLandmarkList(img)

        # print(currentFrameHandLandmarks)

        if prevFrameHandLandmarks:
            for handNum in range(0, len(currentFrameHandLandmarks)):
                for lm in range(0, len(currentFrameHandLandmarks[handNum])):
                    currentX, currentY, currentZ = currentFrameHandLandmarks[handNum][lm][1], currentFrameHandLandmarks[handNum][lm][2], currentFrameHandLandmarks[handNum][lm][3]
                    if len(prevFrameHandLandmarks) > handNum:
                        prevX, prevY, prevZ = prevFrameHandLandmarks[handNum][lm][1], prevFrameHandLandmarks[handNum][lm][2], prevFrameHandLandmarks[handNum][lm][3]
                        deltaX = currentX - prevX
                        deltaY = currentY - prevY
                        deltaZ = currentZ - prevZ

                        if abs(deltaX) < 3:
                            deltaX = 0

                        if abs(deltaY) < 3:
                            deltaY = 0

                        if abs(deltaZ) < 3:
                            deltaZ = 0

                        # CALCULATE PIXEL VELOCITY
                        ux, uy, uz = 0, 0, 0
                        sx, sy, sz = deltaX, deltaY, deltaZ
                        t = timeDif

                        vx = ((2 * sx) / t) - ux
                        vy = ((2 * sy) / t) - uy
                        vz = ((2 * sz) / t) - uz

                        totalVel = sqrt((vx ** 2) + (vy ** 2))
                    else:
                        deltaX = 0
                        deltaY = 0
                        totalVel = 0

                    print("\nHAND: " + str(handNum) + "\nID: " + str(currentFrameHandLandmarks[handNum][lm][0]) + "\nX VELOCITY: " + str(vx) + "\nY VELOCITY: " + str(vy) + "\nZ VELOCITY: " + str(vz) + "\nOVERALL VELOCITY (X & Y): " + str(totalVel))

        prevFrameHandLandmarks = currentFrameHandLandmarks

        cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()

