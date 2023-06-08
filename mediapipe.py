#!/usr/bin/env python
import rospy
import sys
import roslib
import math
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Int8
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist, Vector3

def takeoff():    
   takeoff_pub.publish(Empty())


def land():    
   land_pub.publish(Empty())

def forward() :
	pub_velocity.publish(Twist(Vector3(0.5,0,0),Vector3(0,0,0)))

def hover() :
	pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))

def up() :
	pub_velocity.publish(Twist(Vector3(0,0,1),Vector3(0,0,0)))

def down() :
	pub_velocity.publish(Twist(Vector3(0,0,-0.5),Vector3(0,0,0)))

def right() :
	pub_velocity.publish(Twist(Vector3(0,0.5,0.0),Vector3(0,0,0)))

def left() :
	pub_velocity.publish(Twist(Vector3(0,-0.5,0.0),Vector3(0,0,0)))
def down() :
	pub_velocity.publish(Twist(Vector3(0,0,-0.5),Vector3(0,0,0)))
def rotateright() :
	pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0.5)))
def rotateleft() :
	pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,-0.5)))

def menu():
   print ("t: takeoff")
   print ("l: land")
   print ("h: hover")
   print ("n: up")
   print ("b: down")
   print ("f: forward")
   print ("r: right")
   print ("k: left")
   print ("a: rotateright")
   print ("d: rotateleft")

if __name__ == '__main__':
   rospy.init_node('bebop_control_node', anonymous=True)
   takeoff_pub = rospy.Publisher("bebop/takeoff", Empty, queue_size=10 )
   land_pub = rospy.Publisher("bebop/land", Empty, queue_size=10 )
   pub_velocity = rospy.Publisher('/bebop/cmd_vel', Twist, queue_size=10)
   #rate = rospy.Rate(10) # 10hz
   try:
       while not rospy.is_shutdown():
           menu()
           #key= input("press a key for action")
           key=sys.stdin.read(1)
        if (key == str('t')):
               	takeoff()
        elif (key == str('l')):
               	land()
	   	elif (key == str('h')):
               	hover()
	   	elif (key == str('f')):
               	forward()
	   	elif (key == str('h')):
               	hover()
	   	elif (key == str('n')):
               	up()
	   	elif (key == str('r')):
               	right()
	   	elif (key == str('k')):
               	left()
	   	elif (key == str('b')):
               	down()
	   	elif (key == str('a')):
               	rotateright()
	   	elif (key == str('d')):
               	rotateleft()
	       	rospy.sleep(0.5)
   		except rospy.ROSInterruptException:
       pass