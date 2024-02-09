import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, mode=False, maxHands=2, modelComplexity=1, detectionCon=0.7, trackCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDrawHands = mp.solutions.drawing_utils

    def FindHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDrawHands.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def ConstructLandmarkList(self, img):
        lmList = []
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                lmsForHand = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z

                    lmsForHand.append([id, cx, cy, cz])
                lmList.append(lmsForHand)
        return lmList

    def FindLandmarksForHand(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            handLandmarks = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(handLandmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                lmList.append([id, cx, cy])

                if draw:
                    cv2.putText(img, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 0), 1)

        return lmList

def main():
    prevTime = 0
    currentTime = 0
    cap = cv2.VideoCapture(0)

    handDetector = HandDetector()

    while True:
        success, img = cap.read()

        img = handDetector.FindHands(img)
        lmList = handDetector.FindLandmarksForHand(img)

        if len(lmList) != 0:
            print(lmList[0])

        currentTime = time.time()
        fps = 1 / (currentTime - prevTime)
        prevTime = currentTime

        cv2.putText(img, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
