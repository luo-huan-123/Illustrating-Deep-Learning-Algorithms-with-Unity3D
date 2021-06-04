#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import *
import math

def Joy2ToJoy():
    rospy.init_node('Joy2ToJoy')
    sub_joy2 = rospy.Subscriber('/joy2',Joy,modifyjoy,queue_size=1)
    rospy.spin()
def modifyjoy(joymsg):
    
    pub_joy = rospy.Publisher ('/joy',Joy,queue_size = 1)
    msg=Joy()
    # linear_vel = joymsg.axes[1] *1
    # angular_vel = joymsg.axes[0]
    linear_vel = joymsg.axes[0]*math.cos(-math.pi/4)*1.414 - joymsg.axes[1]*math.sin(-math.pi/4)*1.414
    angular_vel= joymsg.axes[0]*math.sin(-math.pi/4)*1.414 + joymsg.axes[1]*math.cos(math.pi/4)*1.414
    
    msg.axes.append(linear_vel)
    msg.axes.append(angular_vel)

    pub_joy.publish(msg)

if __name__=='__main__':
    Joy2ToJoy()
