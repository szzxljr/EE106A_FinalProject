import rospy
import math
import geometry_msgs.msg
import tf
from tf.msg import tfMessage
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
import time
import numpy as np
from frames import *
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
from baxter_interface import gripper as robot_gripper
import copy

dic = {}
position_relative = []

class a():
    num = 0

obj = a()

def keyboard_control(x):
    
    #Wait for the IK service to become available
    rospy.wait_for_service('compute_ik')
    #rospy.init_node('service_query')

    #Create the function used to call the service
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
    left_gripper = robot_gripper.Gripper('left')
    
    global step 
    step = 0
    mov1 = [0.10, 0.20, 0.05,0.783, -0.621, 0.042, -0.004]
    #0.995, 0.034, 0.067, 0.059
    # mov2 = [0.1, 0, 0.15,0.036, 0.997, -0.062, 0.009]
    # mov3 = [0.1, -0.1, 0.15,0.036, 0.997, -0.062, 0.009]
    # mov4 = [0, -0.1, 0.15,0.036, 0.997, -0.062, 0.009]
    # mov5 = [0.747, -0.241, -0.172,0.061, 0.998, -0.012, 0.013]
    # mov6 = [0.827, -0.261, -0.040,0.998, -0.042, -0.048, -0.010]
    pose = [mov1]

    while not rospy.is_shutdown():

        #raw_input('Press [ Enter ]: ')
        s = pose[step]
        #Construct the request
        request = GetPositionIKRequest()
        request.ik_request.group_name = "left_arm"
        request.ik_request.ik_link_name = "left_gripper"
        request.ik_request.attempts = 20
        request.ik_request.pose_stamped.header.frame_id = "ar_marker_3"#update'base'
        
        #Set the desired orientation for the end effector HERE
        request.ik_request.pose_stamped.pose.position.x = s[0]
        request.ik_request.pose_stamped.pose.position.y = s[1]
        request.ik_request.pose_stamped.pose.position.z = s[2]        
        request.ik_request.pose_stamped.pose.orientation.x = s[3]
        request.ik_request.pose_stamped.pose.orientation.y = s[4]
        request.ik_request.pose_stamped.pose.orientation.z = s[5]
        request.ik_request.pose_stamped.pose.orientation.w = s[6]

        try:
            #Send the request to the service
            response = compute_ik(request)
            
            #Print the response HERE
            #print(response)
            group = MoveGroupCommander("left_arm")
            # print position_relative

            # Setting position and orientation target
            group.set_pose_target(request.ik_request.pose_stamped)

            # TRY THIS
            # Setting just the position without specifying the orientation
            ###group.set_position_target([0.5, 0.5, 0.0])

            # Plan IK and execute
            group.go()
            print "in"
            print  x
            print "out"

        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

        if mov1[0] == 0.1 and mov1[1] == 0.0:
            print "success"
            break

        flag = raw_input()
        if flag== 's':
            next_mov = copy.copy(mov1)
            print next_mov
            # print pose
            # print "s"
            next_mov[0] += 0.1
            # print pose
            if next_mov[0]==x[0] and next_mov[1]==x[1]:
                print "warning!"
                next_mov[0] -= 0.1
            else:
                
                pose.append(next_mov)
                step += 1
        elif flag == 'w':
            print pose
            print "w"
            next_mov = copy.copy(mov1)
            next_mov[0] -= 0.1
            print pose
            if next_mov[0]==x[0] and next_mov[1]==x[1] :
                print "warning!"
                next_mov[0] += 0.1
            else:
                pose.append(next_mov)
                step += 1
        elif flag == 'a':
            next_mov = copy.copy(mov1)
            next_mov[1] -= 0.1
            if next_mov[0]==x[0] and next_mov[1]==x[1] :
                print "warning!"
                next_mov[1] += 0.1
            else:
                pose.append(next_mov)
                step += 1
        elif flag == 'd':
            next_mov = copy.copy(mov1)
            next_mov[1] += 0.1
            if next_mov[0]==x[0] and next_mov[1]==x[1] :
                print "warning!"
                next_mov[1] -= 0.1
            else:
                pose.append(next_mov)
                step += 1
        elif flag =='c':
            left_gripper.close()
        elif flag =='o':
            left_gripper.open()
        elif flag =='p':
            left_gripper.calibrate()
        elif flag =='r':
            next_mov = mov1
            next_mov[3] = 0.995
            next_mov[4] = 0.034
            next_mov[5] = 0.067
            next_mov[6] = 0.059
        elif flag =='t':
            next_mov = mov1
            next_mov[3] = 0.783
            next_mov[4] = -0.621
            next_mov[5] = 0.042
            next_mov[6] = -0.004
        elif flag =='u':
            next_mov = mov1
            next_mov[2] += 0.05
        elif flag =='i':
            next_mov = mov1
            next_mov[2] -= 0.05
        elif flag=="e":
            break


def callback(message):
    for tran in message.transforms:
        head = tran.header.frame_id
        child = tran.child_frame_id
        for target_tran_pair in target_transforms_pairs:
            target_head = target_tran_pair[0]
            target_child = target_tran_pair[1]
            if (head == '/' + target_head 
                and child == target_child):
                tfm = tran.transform
                trs = tfm.translation
                rot = tfm.rotation
                translation = [round(trs.x,3), round(trs.y,3), round(trs.z,3)]
                quaternion = [round(rot.x,3), round(rot.y,3), round(rot.z,3), round(rot.w,3)]
                key = target_head + '_to_' + target_child
                dic[key] = [translation, quaternion]

    if not dic == {}: 
        
        key3 = 'right_hand_camera_to_ar_marker_3'
        key5 = 'right_hand_camera_to_ar_marker_5'
        
        position_relative = list(map(lambda x : round(abs(x[0] - x[1]), 1), 
            zip(dic[key5][0], dic[key3][0])))
        #print "OK"
        #print position_relative
        obj.num = position_relative
        #print obj.num


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("tf",tfMessage, callback)
    #rospy.spin()


if __name__ == '__main__':  
    while True:
       listener()
       keyboard_control(obj.num)
       print "Ok"