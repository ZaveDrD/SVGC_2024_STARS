import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDrawHands = mp.solutions.drawing_utils

prevTime = 0
currentTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print("\nID:", id, "\n Landmarks (in px): \nx:", cx, "\ny:", cy, "\nz (in ratio):", lm.z)

                cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 0), 1)

                if id == 0:
                    cv2.circle(img, (cx, cy), 25, (255, 255, 0), cv2.FILLED) # THS IS HOW TO DETECT CERTAIN ID'S AND USE THEM TO DO STUFF

            mpDrawHands.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    currentTime = time.time()
    fps = 1 / (currentTime - prevTime)
    prevTime = currentTime

    cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
