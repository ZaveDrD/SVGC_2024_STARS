import cv2
import HandTracking.HandTrackingModule as htm

cap = cv2.VideoCapture(0)
handDetector = htm.HandDetector()

handPositions = []

while True:
    success, img = cap.read()  # PROBLEMATIC LINE (DECREASES PERFORMANCE BY A MILLION)

    img = handDetector.FindHands(img)

    currentFrameHandLandmarks = handDetector.ConstructLandmarkList(img)
    handPositions = currentFrameHandLandmarks

    cv2.waitKey(1)
