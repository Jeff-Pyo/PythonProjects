import cv2
from djitellopy import Tello
from time import sleep

me = Tello()
me.connect()
takeoff_flag = 0
print(me.get_battery())
me.streamon()
Kpx = 0.1
Kpy = 0.1
Kpz = -0.0001
global offset_x
'''
def adjust_tello_position_x(offset_x):
    if not -90 <= offset_x <= 90 and offset_x != 0:
    # offset_x가 음수이면 시계 방향으로 일정 거리 만큼 이동
        if offset_x > 0:
            me.rotate_counter_clockwise(10)
     # offset_x가 양수이면 시계 반대 방향으로 일정 거리 만큼 이동
        elif offset_x < 0:
            me.rotate_clockwise(10)
        offset_x*Kp

def adjust_tello_position_y(offset_y):
    if not -70 <= offset_y <= 70 and offset_y != -30:
        if offset_y > 0:qqqq
            print('move up')
            me.move_up(20)
        elif offset_y < 0:
            print('move down')
            me.move_down(20)

def adjust_tello_position_z(offset_z):
    if not 15000 <= offset_z <= 30000 and offset_z != 0:
            if offset_z < 15000:
                me.move_forward(20)
            elif offset_z > 30000:
                me.move_back(20)

'''

def adjust_tello(offset_x, offset_y, offset_z):
    if 10000 < offset_z :
        me.send_rc_control(0, int(offset_z*Kpz), int(offset_y*Kpy), -int(offset_x*Kpx))
                        # left_right velocity, forward_backward_velocity, up_down_velocity, yaw_velocity

    else:
        cv2.imwrite('picture.png', img)


while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360*2, 240*2))
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.3, 5)

    if len(faces) == 1:
        print('face found')
        print('faces', faces)
    else:
        print('face not found')

    tcx = 360
    tcy = 240       # 중심

    cv2.circle(img, (tcx, tcy), 10, (255, 0, 0), cv2.FILLED)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        print('area=', area)

        cv2.line(img, (cx, cy), (tcx, tcy), (255, 0, 0), 2)

    cv2.imshow('frame', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if len(faces) == 1 and takeoff_flag:        ## 이륙중이고, 얼굴을 찾았을 때

        offset_x = tcx-cx
        offset_y = tcy-cy
        size_z = w * h
        offset_z = 20000-size_z
        '''
        adjust_tello_position_x(offset_x)
        adjust_tello_position_y(offset_y)
        adjust_tello_position_z(offset_z)
        '''
        adjust_tello(offset_x, offset_y, offset_z)
        print(offset_x)

    if cv2.waitKey(1)&0xFF == ord('q'):
        takeoff_flag = 0
        break
    elif cv2.waitKey(1)&0xFF == ord('e'):
        me.takeoff()
        takeoff_flag = 1

    sleep(0.01)



cv2.destroyAllWindows()
