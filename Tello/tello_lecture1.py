from djitellopy import Tello
from time import sleep
import time as t


tello = Tello()
tello.connect()
print(tello.get_battery())


my_drone = tello.Tello()
print(my_drone.get_battery())
my_drone.takeoff()
my_drone.land()


tello = Tello()
tello.connect()
tello.takeoff()
tello.move_up(20)
alti = tello.get_barometer()
print(alti)
sleep(2)
tello.move_up(30)
tello.flip_back()
tello.land()
tello.end()



tello = Tello()
tello.connect()
tello.takeoff()

for i in range(3):
    tello.flip_back()
    sleep(3)

tello.land()
tello.end()

