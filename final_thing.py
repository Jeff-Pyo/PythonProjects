import mediapipe as mp
import numpy as np
import cv2
import math
import pyautogui
import wmi
import time
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface,POINTER(IAudioEndpointVolume))
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pyautogui.FAILSAFE = False
space_pressed = False
screen_width, screen_height = pyautogui.size()

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

def set_brightness(level):
    wmi_interface = wmi.WMI(namespace='wmi')     # WMI 인터페이스 초기화
    brightness_instance = wmi_interface.WmiMonitorBrightnessMethods()[0]   # 모니터 설정 변경을 위한 인스턴스 가져오기
    brightness_instance.WmiSetBrightness(level, 0)     # 밝기 레벨 설정

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(level, None)
    volume_range = volume.GetVolumeRange()
    min_volume = volume_range[0]
    max_volume = volume_range[1]
    # print("유효한 볼륨 레벨 범위:", min_volume+65.25, "-", max_volume+65.25)
    master_volume = volume.GetMasterVolumeLevel()
    # print("현재 마스터 볼륨 레벨:", master_volume+65.25)


while True:
    success,img = cap.read()
    h,w,c = img.shape

    if not success:
        continue

    img = cv2.cvtColor(cv2.flip(img,1), cv2.COLOR_BGR2RGB)
    results = my_hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) 

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:

            adjust_sound = dist(
                handlms.landmark[0].x,
                handlms.landmark[0].y,
                handlms.landmark[14].x,
                handlms.landmark[14].y
            ) < dist(
                handlms.landmark[0].x,
                handlms.landmark[0].y,
                handlms.landmark[16].x,
                handlms.landmark[16].y)
            
            thumb_folded = dist(
                handlms.landmark[4].x,
                handlms.landmark[4].y,
                handlms.landmark[10].x,
                handlms.landmark[10].y
            ) < dist(
                handlms.landmark[3].x,
                handlms.landmark[3].y,
                handlms.landmark[10].x,
                handlms.landmark[10].y
            )
            
            index_folded = dist(
                handlms.landmark[8].x,
                handlms.landmark[8].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            ) < dist(
                handlms.landmark[5].x,
                handlms.landmark[5].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            )
            
            middle_folded = dist(
                handlms.landmark[12].x,
                handlms.landmark[12].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            ) < dist(
                handlms.landmark[9].x,
                handlms.landmark[9].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            )
            
            ring_folded = dist(
                handlms.landmark[16].x,
                handlms.landmark[16].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            ) < dist(
                handlms.landmark[13].x,
                handlms.landmark[13].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            )
            
            pinky_folded = dist(
                handlms.landmark[20].x,
                handlms.landmark[20].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            ) < dist(
                handlms.landmark[17].x,
                handlms.landmark[17].y,
                handlms.landmark[0].x,
                handlms.landmark[0].y
            )

            # hand_fliped = dist(
            #     handlms.landmark[12].x,
            #     handlms.landmark[12].y,
            #     handlms.landmark[0].x,
            #     handlms.landmark[0].y
            # ) < dist(
            #     handlms.landmark[9].x,
            #     handlms.landmark[9].y,
            #     handlms.landmark[0].x,
            #     handlms.landmark[0].y
            # )

            virtual_mouse = ring_folded & pinky_folded & thumb_folded
            adjust_brightness = ring_folded and thumb_folded and middle_folded
            open_palm = (not thumb_folded) & (not index_folded) & (not middle_folded) & (not ring_folded) & (not pinky_folded)

            if (adjust_sound == False) and not thumb_folded:
                cv2.putText(
                    img, text="Adjusting Sound",
                    org=(10,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=0, thickness=2)
                ldist = -dist(handlms.landmark[4].x, handlms.landmark[4].y,
                                handlms.landmark[8]. x, handlms.landmark[8].y
                    ) / (dist(handlms.landmark[2].x, handlms.landmark[2].y,
                              handlms.landmark[5].x, handlms.landmark[5].y) * 2)
                ldist = ldist * 50
                ldist = -60 - ldist
                ldist = min(0,ldist)
                set_volume(ldist)

            elif virtual_mouse:
                cv2.putText(
                    img, text="Virtual Mouse",
                    org=(10,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=255, thickness=2)    
                wFS, hFS = pyautogui.size()
                middle_x = int((handlms.landmark[8].x + handlms.landmark[12].x) * screen_width - screen_height/2)
                middle_y = int((handlms.landmark[8].y + handlms.landmark[12].y) * screen_height)
                # 마우스 이동
                pyautogui.moveTo(middle_x, middle_y, duration=0.1)
                length = dist(
                    handlms.landmark[8].x,
                    handlms.landmark[8].y,
                    handlms.landmark[12].x,
                    handlms.landmark[12].y
                )*100
                if length < 6:
                    print(length)
                    pyautogui.click()

            elif adjust_brightness:
                cv2.putText(
                    img, text="Adjusting Brightness",
                    org=(10,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=255, thickness=2)
                rdist = int(dist(handlms.landmark[8].x, handlms.landmark[8].y,
                                 handlms.landmark[20].x, handlms.landmark[20].y
                       ) / (dist(handlms.landmark[2].x, handlms.landmark[2].y,
                                 handlms.landmark[5].x, handlms.landmark[5].y) * 2))
                rdist = rdist*255
                set_brightness(int(rdist))

            elif open_palm:
                if not space_pressed:
                    pyautogui.press('space')         
                    space_pressed = True
                    cv2.putText(
                        img, text="Press space",
                        org=(10,30), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=255, thickness=2)
                    print("press space")
                    start_time = time.time()
                elapsed_time = time.time() - start_time
                if elapsed_time >= 3:
                    space_pressed = False

            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
        
    cv2.imshow("Operating Monitor", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  