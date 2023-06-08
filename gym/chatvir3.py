import cv2
import time
import numpy as np
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
my_hands = mp_hands.Hands()
pyautogui.FAILSAFE = False

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
    wScr, hScr = pyautogui.size()
    print(wScr, hScr)

    while True:
        success, img = cap.read()
        results = my_hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x1, y1 = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                x2, y2 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

                fingers = [1 if lm.y < y2 else 0 for lm in hand_landmarks.landmark[1:]]
                cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (205, 250, 255), -1)
                img = cv2.addWeighted(img, 0.5, img, 1 - .5, 0, img)

                if fingers[1] == 1 and fingers[2] == 1:
                    x3 = np.interp((x1 + x2)/2, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp((y1 + y2)/2, (frameR, hCam - frameR), (0, hScr))

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening

                    pyautogui.moveTo(clocX, clocY)
                    cv2.circle(img, (int(x1 * wCam), int(y1 * hCam)), 6, (255, 28, 0), cv2.FILLED)
                    plocX, plocY = clocX, clocY

                    length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    if length < 0.025:
                        cv2.circle(img, (int(x2 * wCam), int(y2 * hCam)), 6, (0, 255, 0), cv2.FILLED)
                        pyautogui.click()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.imshow("Virtual Mouse Monitor", cv2.flip(img, 1))
        cv2.setWindowProperty("Virtual Mouse Monitor", cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
