import mediapipe as mp
import math
import cv2

cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def takeoff():    
#    takeoff_pub.publish(Empty())
    print("take off")
def land():    
#    land_pub.publish(Empty())
    print("landing")
def forward() :
	# pub_velocity.publish(Twist(Vector3(0.5,0,0),Vector3(0,0,0)))
    print("forward")
def hover() :
	# pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))
    print("hovering")
def up() :
	# pub_velocity.publish(Twist(Vector3(0,0,1),Vector3(0,0,0)))
    print("go up")
def down() :
	# pub_velocity.publish(Twist(Vector3(0,0,-0.5),Vector3(0,0,0)))
    print("go down")
def right() :
	# pub_velocity.publish(Twist(Vector3(0,-0.5,0.0),Vector3(0,0,0)))
    print("go right")
def left() :
	# pub_velocity.publish(Twist(Vector3(0,0.5,0.0),Vector3(0,0,0)))
    print("go left")
def rotateright() :
	# pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0.5)))
    print("turn right")
def rotateleft() :
	# pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,-0.5)))
    print("turn left")




