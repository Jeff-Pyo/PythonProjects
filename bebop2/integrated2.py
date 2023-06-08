#!/usr/bin/env python
#integrated2.py
import rospy
import sys
import roslib
import math
from std_msgs.msg import Empty
from std_msgs.msg import String
from std_msgs.msg import Int8
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist, Vector3
from ardrone_autonomy.msg import Navdata

xmin = None
xmax = None
height = None
position = None
man = None
mans = None
man1 = None
man2 = None
man3 = None
man4 = None
man5 = None

#publish commands (send to quadrotor)
pub_velocity = rospy.Publisher('/cmd_vel', Twist)
pub_takeoff = rospy.Publisher('/bebop/takeoff', Empty)
pub_land = rospy.Publisher('/bebop/land', Empty)
pub_reset = rospy.Publisher('/bebop/reset', Empty)

def forward() :
	pub_velocity.publish(Twist(Vector3(0.5,0,0),Vector3(0,0,0)))

def rotateleft() :
	pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,-0.25)))

def rotateright() :
	pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0.25)))

def honeybeefar() :
	pub_velocity.publish(Twist(Vector3(0.5,0,0.5),Vector3(0,0,0)))

def honeybeemiddle() :
	pub_velocity.publish(Twist(Vector3(0.25,0,0.25),Vector3(0,0,0)))

def takeoff() :
	pub_takeoff.publish(Empty())

def landing() :
	pub_land.publish(Empty())

def hover() :
	pub_velocity.publish(Twist(Vector3(0,0,0),Vector3(0,0,0)))

def up() :
	pub_velocity.publish(Twist(Vector3(0,0,0.5),Vector3(0,0,0)))

def callback0(data) :
	global height
	height = data.data

	if height < 1800:
		print("go up..")
		up()
	else:
		print("hover")
		hover()

def callback1(data) :
	global xmin
	xmin = data.data

def callback2(data) :
	global xmax
	xmax = data.data

def callback3(data) :
	global ymin
	ymin = data.data

def callback4(data) :
	global ymax
	ymax = data.data

def callback5(data) :
	global man
	man = data.data

def detection() :
	global mans
	rospy.Subscriber('/darknet_ros/found_object',Int8,callback5)
	
	if man > 0:
		man1 = man
		man2 = man1
		man3 = man2
		man4 = man3
		man5 = man4
		mans = (man1+man2+man3+man4+man5)/5

def altitude() :
	rospy.Subscriber('/bebop/states/ardrone3/PilotingState/AltitudeChanged',Navdata,callback0)


def yoloa() :
	global position
	rospy.Subscriber('/darknet_ros/x_min', Int64, callback1)
    	rospy.Subscriber('/darknet_ros/x_max', Int64, callback2)

	if (xmin >= 0 and xmin <= 128) and (xmax >= 513 and xmax <= 640):
		position = 1
		print "Near"
	elif (xmin >= 0  and xmin <= 128) and (xmax >= 385 and xmax <= 512):
		position = 1
		print "Near"
	elif (xmin >= 129 and xmin <=256) and (xmax >= 513 and xmax <= 640):
		position = 1
		print "Near"
	elif (xmin >= 0 and xmin <= 128) and (xmax >= 0 and xmax <= 128):
		position = 0
		print "Far Very Right"
		rotateright()
		rospy.sleep(3)
	elif (xmin >= 0 and xmin <= 128) and (xmax >= 129 and xmax <= 256):
		position = 0
		print "Far Right"
		rotateright()
		rospy.sleep(2)
	elif (xmin >= 0 and xmin <= 128) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Middle Right"
		rotateright()
		rospy.sleep(1)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 129 and xmax <= 256):
		position = 0
		print "Far Right"
		rotateright()
		rospy.sleep(2)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Middle Right"
		rotateright()
		rospy.sleep(1)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 385 and xmax <= 512):
		position = 0
		print "Middle Center"
		honeybeemiddle()
		rospy.sleep(2)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Middle Right"
		rotateright()
		rospy.sleep(2)
	elif (xmin >= 257 and xmin <= 384) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Very Far Center"
		honeybeefar()
		rospy.sleep(2)
	elif (xmin >= 257 and xmin <= 384) and (xmax >= 385 and xmax <= 512):
		position = 0
		print "Middle Left"
		rotateleft()
		rospy.sleep(1)
	elif (xmin >= 257 and xmin <= 384) and (xmax >= 513 and xmax <= 640):
		position = 0
		print "Middle Left"
		rotateleft()
		rospy.sleep(1)
	elif (xmin >= 385 and xmin <= 512) and (xmax >= 385 and xmax <= 512):
		position = 0
		print "Far Left"
		rotateleft()
		rospy.sleep(2)
	elif (xmin >= 385 and xmin <= 512) and (xmax >= 513 and xmax <= 640):
		position = 0
		print "Far Left"
		rotateft()
		rospy.sleep(2)
	elif (xmin >= 513 and xmin <= 640) and (xmax >= 513 and xmax <= 640):
		position = 0
		print "Far Very Left"
		rotateright()
		rospy.sleep(3)
	else :
		print ("%d %d",xmin, xmax)


def yolob() :
	global position
	rospy.Subscriber('/darknet_ros/x_min', Int64, callback1)
    	rospy.Subscriber('/darknet_ros/x_max', Int64, callback2)

	if (xmin >= 0 and xmin <= 128) and (xmax >= 513 and xmax <= 640):
		position = 1
		print "Target is Near"
	elif (xmin >= 0  and xmin <= 128) and (xmax >= 385 and xmax <= 512):
		position = 1
		print "Target is Near"
	elif (xmin >= 129 and xmin <=256) and (xmax >= 513 and xmax <= 640):
		position = 1
		print "Target is Near"
	elif (xmin >= 0 and xmin <= 128) and (xmax >= 0 and xmax <= 128):
		position = 0
		print "Approach Target on the Right"
		print "Far Very Right"
		rotateright()
		rospy.sleep(3)
	elif (xmin >= 0 and xmin <= 128) and (xmax >= 129 and xmax <= 256):
		position = 0
		print "Approach Target on the Right"
		print "Far Right"
		rotateright()
		rospy.sleep(2)
	elif (xmin >= 0 and xmin <= 128) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Approach Target on the Right"
		print "Middle Right"
		rotateright()
		rospy.sleep(1)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 129 and xmax <= 256):
		position = 0
		print "Approach Target on the Right"
		print "Far Right"
		rotateright()
		rospy.sleep(2)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Approach Target on the Right"
		print "Middle Right"
		rotateright()
		rospy.sleep(1)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 385 and xmax <= 512):
		position = 0
		print "Approach Target Ahead"
		print "Middle Center"
		honeybeemiddle()
		rospy.sleep(2)
	elif (xmin >= 129 and xmin <= 256) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Approach Target on the Right"
		print "Middle Right"
		rotateright()
		rospy.sleep(2)
	elif (xmin >= 257 and xmin <= 384) and (xmax >= 257 and xmax <= 384):
		position = 0
		print "Approach Target Ahead"
		print "Very Far Center"
		honeybeefar()
		rospy.sleep(2)
	elif (xmin >= 257 and xmin <= 384) and (xmax >= 385 and xmax <= 512):
		position = 0
		print "Approach Target on the Left"
		print "Middle Left"
		rotateleft()
		rospy.sleep(1)
	elif (xmin >= 257 and xmin <= 384) and (xmax >= 513 and xmax <= 640):
		position = 0
		print "Approach Target on the Left"
		print "Middle Left"
		rotateleft()
		rospy.sleep(1)
	elif (xmin >= 385 and xmin <= 512) and (xmax >= 385 and xmax <= 512):
		position = 0
		print "Approach Target on the Left"
		print "Far Left"
		rotateleft()
		rospy.sleep(2)
	elif (xmin >= 385 and xmin <= 512) and (xmax >= 513 and xmax <= 640):
		position = 0
		print "Approach Target on the Left"
		print "Far Left"
		rotateft()
		rospy.sleep(2)
	elif (xmin >= 513 and xmin <= 640) and (xmax >= 513 and xmax <= 640):
		position = 0
		print "Approach Target on the Left"
		print "Far Very Left"
		rotateright()
		rospy.sleep(3)
	else :
		print ("%d %d",xmin, xmax)


if __name__ == '__main__':
	rospy.init_node('example_node', anonymous=True)

	print("ready!")
	rospy.sleep(1.0)
	
	print("takeoff")
	pub_takeoff.publish(Empty())
	rospy.sleep(5)

   	print("stop")
	hover() 
	rospy.sleep(2)           
	       
	#set drone altitude
	print("define altitude")
	while True:
		altitude()
		rospy.sleep(2)
		if height >= 1800:
			break
	print "hover"
	hover()
	rospy.sleep(2)

	while True:
		detection()
		rospy.sleep(1)
		forward()
		rospy.sleep(2)
		if man != None and man != 0:
			break
	hover()
	rospy.sleep(1)	
	detection()
	rospy.sleep(2)
	print("Human detected:", mans)
	if mans == 1:
		while True:
			yoloa()
			rospy.sleep(2)
			if position == 1:
				break
			
	elif mans > 1:
		while True:
			yolob()
			rospy.sleep(2)
			if position == 1:
				break
	print("hover")
	rospy.sleep(1) 
	hover()
	rospy.sleep(2)
	print("Mission Accomplished, Proceed Landing")
	rospy.sleep(1)
	landing()