import mediapipe as mp
import cv2
import math
import pyautogui
import time

from adjusting_vol import set_volume #coded by Donghyeon Lim
from adjusting_bri import set_brightness #coded by Donghyeon Lim
from texting import putText #coded by Junho Pyo
import gesture  #coded by Junho Pyo
import distance as ds #coded by Junho Pyo

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
#referenced by MediaPipe (Google)

pyautogui.FAILSAFE = False 
screen_width, screen_height = pyautogui.size() 
space_pressed = False
#coded by Junho Pyo

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

while True:
    success,img = cap.read()
    h,w,c = img.shape
    if not success:
        continue
#coded by Donghyeon Lim

    img = cv2.cvtColor(cv2.flip(img,1), cv2.COLOR_BGR2RGB)
    results = my_hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:

            lms = handlms
            sound_adjust = gesture.adjust_sound(dist, lms)
            thumb_folded = gesture.thumb_folded(dist, lms)
            index_folded = gesture.index_folded(dist, lms)
            middle_folded = gesture.middle_folded(dist, lms)
            ring_folded = gesture.ring_folded(dist, lms)
            pinky_folded = gesture.pinky_folded(dist, lms)
            #coded by Junho Pyo

            virtual_mouse = ring_folded & pinky_folded & thumb_folded
            adjust_brightness = ring_folded and thumb_folded and middle_folded
            open_palm = (not thumb_folded) & (not index_folded) & (not middle_folded) & (not ring_folded) & (not pinky_folded)
            #coded by Junho Pyo

            if (sound_adjust == False) and not thumb_folded:

                texts = "Adjusting Sound"
                colors = [200, 200, 255]
                putText(img, texts, colors)
                sdist = ds.sound_dist(dist, lms)
                sdist = sdist * 50
                sdist = -60 - sdist
                sdist = min(0,sdist)
                set_volume(sdist)
            #referenced by https://developeralice.tistory.com/11
            #fixed by Junho Pyo

            elif virtual_mouse:

                texts = "Virtual Mouse"
                colors = [255, 0, 255]
                putText(img, texts, colors)

                wFS, hFS = pyautogui.size()
                middle_x = int((handlms.landmark[8].x + handlms.landmark[12].x) * screen_width - screen_height/2)
                middle_y = int((handlms.landmark[8].y + handlms.landmark[12].y) * screen_height)
                pyautogui.moveTo(middle_x, middle_y, duration=0.1)
                length = ds.clk_len(dist, lms)

                if length < 6:
                    print(length)
                    pyautogui.click()
            #coded by Junho Pyo

            elif adjust_brightness:

                texts = "Adjusting Brightness"
                colors = [125, 125, 0]
                putText(img, texts, colors)
                bdist = ds.brightness_dist(dist, lms)
                bdist = bdist*255
                set_brightness(int(bdist))
            #coded by Donghyeon Lim
            #helped by Junho Pyo

            elif open_palm:

                if not space_pressed:
                    pyautogui.press('space')         
                    space_pressed = True
                    texts = "Press space"
                    colors = [125, 125, 125]
                    putText(img, texts, colors)
                    start_time = time.time()

                elapsed_time = time.time() - start_time
                
                if elapsed_time >= 3:
                    space_pressed = False
            #coded by Donghyeon Lim
            #helped by Junho Pyo

            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
        
    cv2.imshow("Operating Monitor", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  