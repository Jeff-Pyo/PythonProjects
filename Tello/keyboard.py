'''

from djitellopy import Tello
import cv2
import numpy
from time import sleep

global img
me = Tello()

me.connect()

print(me.get_battery())
me.streamon()

def getKeyinput():
    lr, fb, ud, vv = 0, 0, 0, 0
    speed = 50
    key = cv2.waitKey(1) & 0xff

    if key == ord('u'):
        fb = speed
    elif key == ord('i'):
        fb = -speed
    if key == ord('k'):
        lr = speed
    elif key == ord('h'):
        lr = -speed
    if key == ord('w'):
        ud = speed
    elif key == ord('s'):
        ud = -speed
    if key == ord('a'):
        vv = speed
    elif key == ord('d'):
        vv = -speed
    if key == ord('g'):
        me.land()
        sleep(3)
    if key == ord('e'):
        me.takeoff()
    if key == ord('z'):
        cv2.imwrite("picture.png", img)
        sleep(0.3)
    if key == ord('q'):
        me.end()

    return [lr, fb, ud, vv]
    ### 키보드 입력해서 리턴하는 함수

while True:
    sleep(0.001)
    vals = getKeyinput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", numpy.random*10, img)
    cv2.waitKey(1)

'''
