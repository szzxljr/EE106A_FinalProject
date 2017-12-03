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
from AI import *
# from ik_example import *


def do(action,pos):             
	if action == 'move_s':
		move_s(pos)
	elif action == 'move_w':
		move_w(pos)
	elif action == 'move_a':
		move_a(pos)
	elif action == 'move_d':
		move_d(pos)
	elif action == 'open_gripper':
		move_down(pos)
		left_gripper.open()
	elif action == 'close_gripper':      
		left_gripper.close()
		move_up(pos)
	elif action == 'move_up':
		move_up_high(pos)
	elif action == 'move_down':
		move_down_high(pos)
	elif action == 'turn_a_or_d':
		turn_a_or_d(pos)
	elif action == 'turn_s_or_w':
		turn_s_or_w(pos)
	elif action == 'move_up_high':
		move_up_high(pos)
	elif action == 'move_down_high':
		move_down_high(pos)
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
		group.go()
		step = step + 1

def move_down(x):
	go_pos = x
	go_pos[2] -= 0.02
	move_action(go_pos)

def move_up(x):
	go_pos = x
	go_pos[2] += 0.02
	move_action(go_pos)

def turn_s_or_w(x):
	go_pos = x
	go_pos[3] = 0.672
	go_pos[4] = 0.739
	go_pos[5] = 0.0

	move_action(go_pos)


def turn_a_or_d(x):
	go_pos = x
	go_pos[3] = 0.0
	go_pos[4] = 1.0
	go_pos[5] = 0.0
	move_action(go_pos)
def move_s(x):
	go_pos = x
	go_pos[1] -= unit_length
	move_action(go_pos)

def move_w(x):
	go_pos = x
	go_pos[1] += unit_length
	move_action(go_pos)

def move_a(x):
	go_pos = x
	go_pos[0] -= unit_length
	move_action(go_pos)

def move_d(x):
	go_pos = x
	go_pos[0] += unit_length
	move_action(go_pos)

def open_gripper():
	left_gripper.open()

def close_gripper():
	left_gripper.close()

def move_up_high(x):
	go_pos = x
	go_pos[2] += 0.05
	move_action(go_pos)

def move_down_high(x):
	go_pos = x
	go_pos[2] -= 0.05
	move_action(go_pos)

def main():
	print "Please input:"
	flag = raw_input()
	printboard2(game_map)
	if flag in "wsad":
		dic = {"s" : (0, -unit_length), "w": (0, unit_length),
		   "a" : (-unit_length, 0), "d" : (unit_length, 0)}
		expected = tuple([int(round(pos[i] + dic[flag][i], 1) * 10) for i in range(2)])
		if expected in walls:
			print "Warning: illegal move {}".format(flag)
			return
		if flag == "s":
			print "Move down"
			do('move_s',pos)
		elif flag == "w":
			print "Move up"
			do('move_w',pos)
		elif flag == "a":
			print "Move left"
			do('move_a',pos)
		elif flag == "d":
			print "Move right"
			do('move_d',pos)
	else:
	#movep2(game_map, findposition2(game_map, MAN), expected)
	#print "Recent map:"
	#printboard2(game_map)
	#return
		if flag == "o":
			print "Open gripper"
			do('open_gripper',pos)
		elif flag == "c":
			print "Close gripper"
			do('close_gripper',pos)
		elif flag == "u":
			print "Move up"
			do('move_up_high',pos)
		elif flag == "i":
			print "Move down"
			do('move_down_high',pos)
		elif flag == "t":
			print "turn direction"
			do('turn_a_or_d',pos)
		elif flag == 'r':
			print "turn direction"
			do('turn_s_or_w',pos)
	#print "Recent map:"
	#printboard2(game_map)



#Python's syntax for a main() method
if __name__ == '__main__':

	game_map = mapTomatrix()
	#print game_map

	unit_length = 0.1
	rospy.wait_for_service('compute_ik')
	rospy.init_node('service_query')
	left_gripper = robot_gripper.Gripper('left')
	left_gripper.calibrate()

	for i in range(4):
		for j in range(4):
			if game_map[i][j] == "@":
				start_x = i
				start_y = j

	mov1 = [start_x*unit_length, start_y*unit_length-0.03, 0.025,0.000, 1.000, 0.000, 0.036]

	do(mov1,0)
	walls = findallposition2(game_map, WAL)
	pos = mov1
	while True:
		main()