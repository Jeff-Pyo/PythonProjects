import cv2
import time
import numpy as np
import mediapipe as mp
import hand_detector as hd
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
my_hands = mp_hands.Hands()

def main():
    wCam, hCam = 640, 480
    frameR = 100
    smoothening = 1.3

    pTime = 0
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    detector = hd.handDetector(detectionCon=0.7)
    wScr, hScr = pyautogui.size()
    print(wScr, hScr)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)
        output = img.copy()
        results = my_hands.process(img)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            x3, y3 = lmList[16][1:]

            fingers = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (205, 250, 255), -1)
            img = cv2.addWeighted(img, 0.5, output, 1 - .5, 0, output)

            if fingers[1] == 1 and fingers[2] == 1:
                x3 = np.interp((x1 + x2)/2, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp((y1 + y2)/2, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                pyautogui.moveTo(wScr - clocX, clocY)
                cv2.circle(img, (x1, y1), 6, (255, 28, 0), cv2.FILLED)
                plocX, plocY = clocX, clocY

                length, img, lineInfo = detector.findDistance(8, 12, img)
                if length < 25:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 6, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.imshow("Virtual Mouse Monitor", cv2.flip(img, 1))
        cv2.setWindowProperty("Virtual Mouse Monitor", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
