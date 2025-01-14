#!/usr/bin/env python3
"""
  Odometry publisher script
  
  This scripts extracts the world position of a given robot in Gazebo simulation.
  The information is then transformed into a Odometry message and published on /odom
  The script also publishes accompanying tf transformation from odom -> base frame of the robot
"""

import rospy
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetModelState
from geometry_msgs.msg import PoseWithCovariance, TwistWithCovariance, TransformStamped
import tf2_ros


# TODO: More general robot name ?
# TODO: See if other robots have different base frame names
# if so, we have to use the name as param

if __name__ == "__main__":
    rospy.init_node("odom_pub")
    rate = rospy.Rate(50)  # ROS Rate at 50Hz
    pub = rospy.Publisher("/odom", Odometry, queue_size=10)
    rospy.wait_for_service("/gazebo/get_model_state")
    caller = rospy.ServiceProxy("/gazebo/get_model_state", GetModelState)
    br = tf2_ros.TransformBroadcaster()

    while not rospy.is_shutdown():
        # First param is the name of the robot in Gazebo
        # maybe we should change this to something more general like robot
        resp = caller("turtlebot3", "world")
        now = rospy.get_rostime()
        msg = Odometry()
        t = TransformStamped()
        t.header.stamp = now
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.transform.translation = resp.pose.position
        t.transform.rotation = resp.pose.orientation
        br.sendTransform(t)
        msg.header.stamp = now
        msg.header.frame_id = "odom"
        msg.child_frame_id = "base_link"
        msg.pose.pose = resp.pose
        msg.twist.twist = resp.twist

        # Covariance was taken from jackal's velocity controller config file

        msg.pose.covariance[0] = 0.001
        msg.pose.covariance[7] = 0.001
        msg.pose.covariance[14] = 1000000.0
        msg.pose.covariance[21] = 1000000.0
        msg.pose.covariance[28] = 1000000.0
        msg.pose.covariance[35] = 0.03

        msg.twist.covariance[0] = 0.001
        msg.twist.covariance[0] = 0.001
        msg.twist.covariance[0] = 0.001
        msg.twist.covariance[0] = 1000000.0
        msg.twist.covariance[0] = 1000000.0
        msg.twist.covariance[0] = 0.03

        pub.publish(msg)
        rate.sleep()
