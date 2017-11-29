#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
from baxter_interface import gripper as robot_gripper
import copy
from map_to_matrix import *
# from ik_example import *

game_map = [['#', '#', '@', '#'], 
        ['#', '#', '-', '.2'], 
        ['$1', '-', '-', '-'], 
        ['#', '$2', '.1', '#']]
unit_length = 0.1
def main():
    print "ok1"
    #Wait for the IK service to become available
    rospy.wait_for_service('compute_ik')
    rospy.init_node('service_query')
    
    #Create the function used to call the service
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
    left_gripper = robot_gripper.Gripper('left')
    
    global step 
    step = 0
    mov1 = [2*unit_length, 3*unit_length-0.05, 0.07,0.000, 1.000, 0.000, 0.036]
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
            # print(response)
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

        # if mov1[0] == 0 and mov1[1] == -0.2:
    	   #  print "success"
       	#     break

        flag = raw_input()
        if flag== 's':
            next_mov = mov1
            next_mov[1] -= 1*unit_length
            print next_mov[1]
            if game_map[int(10*(next_mov[0]))][int(10*(next_mov[1]+0.05))] == "#":
                print "warning!"
                next_mov[1] += 1*unit_length
            else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'w':
        	next_mov = mov1
        	next_mov[1] += 1*unit_length
        	if game_map[int(10*(next_mov[0]))][int(10*(next_mov[1]+0.05))] == "#":
        		print "warning!"
        		next_mov[1] -= 1*unit_length
        	else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'a':
        	next_mov = mov1
        	next_mov[0] -= 1*unit_length
        	if game_map[int(10*(next_mov[0]))][int(10*(next_mov[1]+0.05))] == "#":
        		print "warning!"
        		next_mov[0] += 1*unit_length
        	else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'd':
        	next_mov = mov1
        	next_mov[0] += 1*unit_length
        	if game_map[int(10*(next_mov[0]))][int(10*(next_mov[1]+0.05))] == "#":
        		print "warning!"
        		next_mov[0] -= 1*unit_length
        	else:
        		pose.append(next_mov)
        		step += 1
        elif flag == 'i':
            next_mov = mov1
            next_mov[2] -= 0.07
            pose.append(next_mov)
            step += 1
        elif flag == 'u':
            next_mov = mov1
            next_mov[2] += 0.07
            pose.append(next_mov)
            step += 1
        elif flag == 'c':
            left_gripper.close()
        elif flag == 'o':
            left_gripper.open()
        		
          

#Python's syntax for a main() method
if __name__ == '__main__':
      main()
