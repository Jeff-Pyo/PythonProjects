import rospy
from darknet_ros_msgs.msg import BoundingBoxes
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist

def set_state(input):   #possible states: "pd", "np " person detected, no person
    global state
    state = input
def get_state():
    return(state)

def callback(data):

Cy_center = 340 #x center position of the image
Cz_center = 240 #y center position of the image
Area_id = 640 * 480 * 0.30 # 30% of pixel area (for x)
K_x = 1 #vel_x paramete
sum_error_x = 0
sum_error_y = 0
sum_error_z = 0

#parameters to tune
Kp_fb = 0.2 #proportional gain FORWARD/BACKWARD
Kd_fb = 1.5 #derivative gain FORWARD/BACKWARD
Ki_fb = 1 #integral gain FORWARD/BACKWARD
Kp_lr = 0.2 #proportional gain LEFT/RIGHT
Kd_lr = 1.5 #derivative gain LEFT/RIGHT
Ki_lr = 1 #integral gain LEFT/RIGHT
Kp_ud= 0.2 #proportional gain UP/DOWN
Kd_ud = 1.5 #derivative gain UP/DOWN
Ki_ud = 1 #integral gain UP/DOWN

state = get_state()

pub = rospy.Publisher('bebop/cmd_vel', Twist, queue_size = 1)
pub_land = rospy.Publisher('bebop/land', Empty, queue_size = 1)
pub_takeoff = rospy.Publisher('bebop/takeoff', Empty, queue_size = 1)
empty_msg = Empty()
twist = Twist()

if state == "np":
    twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0; 
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -0.3;
    pub.publish(twist)
    print("Looking for person")

for box in data.bounding_boxes:

    if box.Class == "person":

        set_state("pd")
        Cy = box.xmin+(box.xmax-box.xmin)/2;
        Cz = box.ymin+(box.ymax-box.ymin)/2;

        Area_ref = ((box.xmax - box.xmin) * (box.ymax - box.ymin))
        error_y = Cy_center - Cy # LEFT/RIGHT
        #error_z = Cz_center - Cz # UP/DOWN
        error_z = Cz_center - box.ymin #so drone will fly higher
        error_x = Area_id - Area_ref #FORWARD/BACKWARD
        vel_y = error_y/320
        if vel_y >= 1:
            vel_y = 1
        elif vel_y <= -1:
            vel_y = -1
        vel_z = error_z/320
        if vel_z >= 1:
            vel_z = 1
        elif vel_z <= -1:
            vel_z = -1
        vel_x = (error_x*K_x)/Area_id
        if vel_x >= 1:
            vel_x = 1
        elif vel_x <= -1:
            vel_x = -1

        #PID X AXES
        sum_error_x = sum_error_x + vel_x
        last_error_x = vel_x
        output_x = Kp_fb * vel_x + Kd_fb * (vel_x - last_error_x) + Ki_fb * sum_error_x

        #PID Y AXES
        sum_error_y = sum_error_y + vel_y
        last_error_y = vel_y
        output_y = Kp_lr * vel_y + Kd_lr * (vel_y - last_error_y) + Ki_lr * sum_error_y

        #PID Z AXES
        sum_error_z = sum_error_z + vel_z
        last_error_z = vel_z
        output_z = Kp_lr * vel_z + Kd_lr * (vel_z - last_error_z) + Ki_lr * sum_error_z 

    #SEND COMMANDS
    twist.linear.x = 0.5*output_x; twist.linear.y = 0.5*output_y; twist.linear.z = 0.5*output_z; 
    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0;
    pub.publish(twist)

    rospy.loginfo(
        "vel_x: {}, vel_y: {}, vel_z: {}, Classe: {}".format(round(output_x,2), round(output_y,2), round(output_z,2), box.Class)
    )

def main():
    set_state("np")
    while not rospy.is_shutdown():

    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(1)
    rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes , callback )
    set_state("np") #reset state to no person in case detector fails to detect
    rospy.spin() #blocks until ros node is shutdown

if __name__ == '__main__':
    try :
        main()
    except rospy.ROSInterruptException:
        pass