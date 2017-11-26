import numpy as np
import rospy
import math
import geometry_msgs.msg
import tf
from tf.msg import tfMessage
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
import time
import numpy as np

import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
from baxter_interface import gripper as robot_gripper
import copy

#JR import 
from frames import *
from play_origin import compute_ik
from constant import *


split = 10

def split_move(pose):
    """
    Split one destination coordinates to split pieces.
    Return the series of result.
    """

    pose = np.array(pose)
    poses = np.dstack([np.linspace(0, x, split) for x in pose])[0]
    return poses
def make_split_move(pose):
    '''
    split and do the move.
    '''
    poses = split_move(pose)
    for p in poses:
        make_single_move(p)

def make_single_move(pose):
    '''
    Do a single move.
    '''

    print "ok"
    s = pose
    print s
    #Construct the request
    request = GetPositionIKRequest()
    request.ik_request.group_name = "left_arm"
    request.ik_request.ik_link_name = "left_gripper"
    request.ik_request.attempts = 20
    request.ik_request.pose_stamped.header.frame_id = "ar_marker_3"  
    #Set the desired orientation for the end effector HERE
    request.ik_request.pose_stamped.pose.position.x = s[0]
    request.ik_request.pose_stamped.pose.position.y = s[1]
    request.ik_request.pose_stamped.pose.position.z = s[2]        
    request.ik_request.pose_stamped.pose.orientation.x = s[3]
    request.ik_request.pose_stamped.pose.orientation.y = s[4]
    request.ik_request.pose_stamped.pose.orientation.z = s[5]
    request.ik_request.pose_stamped.pose.orientation.w = s[6]

    try:
        print "ok2"
        response = compute_ik(request)
        group = MoveGroupCommander("left_arm")
        print "ok3"
        group.set_pose_target(request.ik_request.pose_stamped)
        print "ok4"
        group.go()
        print "in"
        print  x
        print "out"
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e



pose = [0.10, 0.20, 0.00,0.783, -0.621, 0.042, -0.004]

print "ok1"
make_split_move(pose)



    

