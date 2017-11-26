#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
from baxter_interface import gripper as robot_gripper
import copy

unit_len = 0.09

#Wait for the IK service to become available
rospy.wait_for_service('compute_ik')
rospy.init_node('service_query')
left_gripper = robot_gripper.Gripper('left')
left_gripper.calibrate()


def main():
	global step 

	mov = [['empty',(3,3),(2,0)],['empty',(2,0),(2,1)],['box1',(2,1),(2,2)],['box1',(2,2),(3,2)],['empty',(3,2),(3,3)],
			['box2',(3,3),(2,3)],['box2',(2,3),(1,3)],['empty',(1,3),(1,2)]]
	for i in range(len(mov)):
	
		if i == 0:
			ac = transform(mov[i])
			do(ac,0)
	
		# else:
		# 	if mov[i-1][0]==mov[i][0]:
		# 		if mov[i][0] == 'empty':
		# 			ac = transform(mov[i])
		# 			do(ac,0)
		# 		else:
		# 			ac = transform(mov[i])
		# 			do(ac,0)
		# 			if i != len(mov)-1 :
		# 				if mov[i][0]!=mov[i+1][0]:
		# 					ac = transform(mov[i])
		# 					do('move_down_then_close_gripper_then_move_up',ac)
		
	
		# 	elif mov[i][0]!=mov[i-1][0]:
		# 		if mov[i][0] == 'empty':
		# 			ac = transform(mov[i])
		# 			do(ac,0)	
		# 		else:
		# 			ac = transform(mov[i])
		# 			do('move_down_then_close_gripper_then_move_up',ac)
		# 			do(ac,0)
		# 			if i != len(mov)-1 :
		# 				if mov[i][0]!=mov[i+1][0]:
		# 					do('move_down_then_open_gripper_then_move_up',ac)
		else:
			if mov[i-1][0]==mov[i][0]:
				ac = transform(mov[i])
				do(ac,0)
			elif mov[i-1][0]!=mov[i][0]:
				if mov[i][0] == "empty":
					ac1 = transform(mov[i-1])
					ac2 = transform(mov[i])
					do('move_down_then_open_gripper_then_move_up',ac1)
					do(ac2,0)
				elif mov[i][0] == "box1" or mov[i][0]=="box2":
					ac1 = transform(mov[i-1])
					ac2 = transform(mov[i])
					do('move_down_then_close_gripper_then_move_up',ac1)
					do(ac2,0)

                   			
              		
def do(action,pos):             
 	if action == 'move_down_then_open_gripper_then_move_up':
		move_down(pos)
		open_gripper()
		move_up(pos)
 	elif action == 'move_down_then_close_gripper_then_move_up':      
		move_down(pos)
		print "ok1"
		close_gripper()
		print "ok4"
		move_up(pos)
		print "ok5"
	else:
		move_action(action)

def move_action(x):

	#Create the function used to call the service
	compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
	#abs_position = [x[2][0]*unit_len+0.03,x[2][1]*unit_len,0.05,0.001, 0.999, 0.005, 0.036]
	step = 0
	pose = [x]
	if step == 0:

		s = pose[step]

		request = GetPositionIKRequest()
		request.ik_request.group_name = "left_arm"
		request.ik_request.ik_link_name = "left_gripper"
		request.ik_request.attempts = 20
		request.ik_request.pose_stamped.header.frame_id = "ar_marker_0"

		request.ik_request.pose_stamped.pose.position.x = s[0]
		request.ik_request.pose_stamped.pose.position.y = s[1]
		request.ik_request.pose_stamped.pose.position.z = s[2]        
		request.ik_request.pose_stamped.pose.orientation.x = s[3]
		request.ik_request.pose_stamped.pose.orientation.y = s[4]
		request.ik_request.pose_stamped.pose.orientation.z = s[5]
		request.ik_request.pose_stamped.pose.orientation.w = s[6]

		response = compute_ik(request)
		group = MoveGroupCommander("left_arm")
		group.set_pose_target(request.ik_request.pose_stamped)
		group.go()
		step = step + 1


def move_down(x):
	#abs_position = [x[2][0]*unit_len,x[2][1]*unit_len,0.05,0.001, 0.999, 0.005, 0.036]
	go_pos = x
	go_pos[2] -= 0.06
	move_action(go_pos)

def move_up(x):
	#abs_position = [x[2][0]*unit_len,x[2][1]*unit_len,0.05,0.001, 0.999, 0.005, 0.036]
	go_pos = x
	go_pos[2] += 0.06
	move_action(go_pos)

def open_gripper():
	left_gripper.open()

def close_gripper():
	print "ok2"
	left_gripper.close()
	print "ok3"

def transform(x):
	return [x[2][0]*unit_len,x[2][1]*unit_len,0.07,0.001, 0.999, 0.005, 0.036]


if __name__ == '__main__':
      main()
# 	############################
# '''
#       mov = [['empty',(3,3),(0,3)],
#        ['box1',(0,3),(2,3)],
#        ['box1',(2,3),(2,1)],
#        ['empty',(2,1),(1,1)],
#        ['box2',(1,1),(1,0)],
#        ['empty',(1,0),(2,0)],
#        ['empty',(2,0),(2,1)],
#        ['box1',(2,1),(0,1)],
#        ['box1',(0,1),(0,0)]]
#     '''