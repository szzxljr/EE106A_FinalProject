#!/usr/bin/env python
import rospy
from moveit_msgs.srv import GetPositionIK, GetPositionIKRequest, GetPositionIKResponse
from geometry_msgs.msg import PoseStamped
from moveit_commander import MoveGroupCommander
import numpy as np
from numpy import linalg
from baxter_interface import gripper as robot_gripper
import copy
# from AI import search
from AI import search
from moveit_msgs.msg import OrientationConstraint, Constraints
#from AI import b as board
#from AI import movep

unit_len = 0.1

#Wait for the IK service to become available
rospy.wait_for_service('compute_ik')
rospy.init_node('service_query')
left_gripper = robot_gripper.Gripper('left')
left_gripper.calibrate()

def printboardlive():
	print "The current board is:"
	for row in board:
		print row

def moveboard(move):
	movep(move[1], move[2])

def split_moves(moves):
	splitmovs = []
	factor = 10
	for mov in moves:
		p0, pd = mov[1], mov[2]
		x0, y0 = p0
		xd, yd = pd
		xs = np.linspace(x0, xd, factor)
		ys = np.linspace(y0, yd, factor)
		ps = np.dstack(xs, ys)
		print ps

def main():

	global step
	mov = search()

	# print mov
	for i in range(len(mov)):
		#moveboard(mov[i])
		#printboardlive()
		if i == 0:
			ac = transform(mov[i],0)
			do(ac,0)
	
		else:
			if mov[i-1][0]==mov[i][0]:
				if mov[i][0] == "box1" or mov[i][0]=="box2":
					ac = transform(mov[i],1)
				if mov[i][0] == "empty":
					ac = transform(mov[i],0)
				do(ac,0)
			elif mov[i-1][0]!=mov[i][0]:
				if mov[i][0] == "empty":
					ac1 = transform(mov[i-1],1)
					ac2 = transform(mov[i],0)
					do('move_down_then_open_gripper_then_move_up',ac1)
					do(ac2,0)
				elif mov[i][0] == "box1" or mov[i][0]=="box2":
					ac1 = transform(mov[i-1],0)
					ac2 = transform(mov[i],1)
					do('move_down_then_close_gripper_then_move_up',ac1)
					do(ac2,0)

	
def do(action,pos):             
	if action == 'move_down_then_open_gripper_then_move_up':
		move_down_small(pos)
		open_gripper()
		move_up(pos)
	elif action == 'move_down_then_close_gripper_then_move_up':      
		move_down(pos)
		close_gripper()
		move_up_small(pos)
	else:
		move_action(action)

def move_action(x):

	#Create the function used to call the service


	compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
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
		# orien_const = OrientationConstraint()
		# orien_const.link_name = "left_arm"
		# orien_const.header.frame_id = "base"
		# orien_const.orientation.x = 0.0

		# orien_const.orientation.y = 1.0

		# orien_const.orientation.z = 0.0

		# orien_const.absolute_x_axis_tolerance = 0.1
		# orien_const.absolute_y_axis_tolerance = 0.1
		# orien_const.absolute_z_axis_tolerance = 0.1
		# orien_const.weight = 1.0
		# consts = Constraints()
		# consts.orientation_constraints = [orien_const]
		# group.set_path_constraints(consts)
		group.go()
		step = step + 1

def move_down_small(x):
	go_pos = x
	go_pos[2] -= 0.025
	move_action(go_pos)
def move_down(x):
	go_pos = x
	go_pos[2] -= 0.05
	move_action(go_pos)
def move_up_small(x):
	go_pos = x
	go_pos[2] += 0.025
	move_action(go_pos)
def move_up(x):
	go_pos = x
	go_pos[2] += 0.05
	move_action(go_pos)

def open_gripper():
	left_gripper.open()

def close_gripper():
	left_gripper.close()

def transform(x,flag):
	if flag == 1:
		return [x[2][0]*unit_len,x[2][1]*unit_len-0.03,0.025,0.000, 1.000, 0.000, 0.036]
	else:
		return [x[2][0]*unit_len,x[2][1]*unit_len-0.03,0.06,0.000, 1.000, 0.000, 0.036]


if __name__ == '__main__':

	main()
