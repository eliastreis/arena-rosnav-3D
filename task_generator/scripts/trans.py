#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


# def odom_callback(data):
#     # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
#     pub = rospy.Publisher("/odom", Odometry, queue_size=10)
#     pub.publish(data)


def vel_callback(data):
    pub = rospy.Publisher("/jackal_velocity_controller/cmd_vel", Twist, queue_size=10)
    pub.publish(data)


def listener():
    rospy.init_node("listener", anonymous=True)

    # rospy.Subscriber("/jackal_velocity_controller/odom", Odometry, odom_callback)
    rospy.Subscriber("/cmd_vel", Twist, vel_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == "__main__":
    listener()
