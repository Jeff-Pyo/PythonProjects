import mediapipe as mp
import cv2
import math
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

def dist(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1 - x2,2)) + math.sqrt(math.pow(y1 - y2,2))

while True:
    success,img = cap.read()
    h,w,c = img.shape
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            open = dist(handlms.landmark[0].x, handlms.landmark[0].y,handlms.landmark[14].x,handlms.landmark[14].y) < dist(handlms.landmark[0].x, handlms.landmark[0].y,handlms.landmark[16].x,handlms.landmark[16].y)
            
            if open == False:
                curdist = -dist(handlms.landmark[4].x, handlms.landmark[4].y,handlms.landmark[8].x, handlms.landmark[8].y) / (dist(handlms.landmark[2].x, handlms.landmark[2].y,handlms.landmark[5].x, handlms.landmark[5].y) * 2)
                curdist = curdist * 50
                curdist = -60 - curdist
                curdist = min(0,curdist)
                volume.SetMasterVolumeLevel(curdist,None)
            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
        

    # cv2.imshow("HandTracking", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
