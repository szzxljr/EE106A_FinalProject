#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
from baxter_interface import gripper as robot_gripper
import copy
import sys
sys.path.append("/home/cc/ee106a/fa17/class/ee106a-act/ros_workspaces/project_camera/src/chatter/src")
import frames
import listener 

unit_length = 0.1
def main():
    #Wait for the IK service to become available
    rospy.wait_for_service('compute_ik')
    rospy.init_node('service_query')
    
    #Create the function used to call the service
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
    left_gripper = robot_gripper.Gripper('left')
    
    global step 
    step = 0
    mov1 = [2*unit_length, 3*unit_length, 0.07,0.000, 1.000, 0.000, 0.036]
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
        request.ik_request.pose_stamped.header.frame_id = "ar_marker_0"#update'base'
        
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
            print(response)
            group = MoveGroupCommander("left_arm")
            # print position_relative

            # Setting position and orientation target
            group.set_pose_target(request.ik_request.pose_stamped)

            # TRY THIS
            # Setting just the position without specifying the orientation
            ###group.set_position_target([0.5, 0.5, 0.0])

            # Plan IK and execute
            group.go()
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

        if mov1[0] == 0 and mov1[1] == -0.2:
    	    print "success"
       	    break

        flag = raw_input()
        if flag== 's':
        	next_mov = mov1
        	next_mov[1] -= 0.1
        	print next_mov[1]
        	if next_mov[0]==0 and next_mov[1]==-0.1 :
        		print "warning!"
        		next_mov[1] += 0.1
        	else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'w':
        	next_mov = mov1
        	next_mov[1] += 0.1
        	if next_mov[0]==0 and next_mov[1]==-0.1 :
        		print "warning!"
        		next_mov[1] -= 0.1
        	else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'a':
        	next_mov = mov1
        	next_mov[0] -= 0.1
        	if next_mov[0]==0 and next_mov[1]==-0.1 :
        		print "warning!"
        		next_mov[0] += 0.1
        	else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'd':
        	next_mov = mov1
        	next_mov[0] += 0.1
        	if next_mov[0]==0 and next_mov[1]==-0.1 :
        		print "warning!"
        		next_mov[0] -= 0.1
        	else:
        		pose.append(next_mov)
        		step += 1
        		
          

#Python's syntax for a main() method
if __name__ == '__main__':
      main()

