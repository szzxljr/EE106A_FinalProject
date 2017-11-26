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
#from make_move import *
from constant import *

boxes_axis = {}
tf_dic = {}
position_relative = []
board = []

class a():
    num = 0

obj = a()

def make_split_move(pose):

    	poses = split_move(pose)
    	for p in poses:
        	make_single_move(p)
def split_move(pose):
 	"""
   	Split one destination coordinates to split pieces.
   	Return the series of result.
   	"""
   	pose = np.array(pose)
   	poses = np.dstack([np.linspace(0, x, split) for x in pose])[0]
   	return poses

def keyboard_control(x):
    

    #Wait for the IK service to become available
    rospy.wait_for_service('compute_ik')
    #rospy.init_node('service_query')

    #Create the function used to call the service
    compute_ik = rospy.ServiceProxy('compute_ik', GetPositionIK)
    left_gripper = robot_gripper.Gripper('left')
    
    global step 
    step = 0
    pose = [0.10, 0.20, 0.00,0.783, -0.621, 0.042, -0.004]




    split = 10

    # def split_move(pose):
    # 	"""
    # 	Split one destination coordinates to split pieces.
    # 	Return the series of result.
    # 	"""

    # 	pose = np.array(pose)
    # 	poses = np.dstack([np.linspace(0, x, split) for x in pose])[0]
    # 	return poses

	# def make_split_move(pose):

 #    		poses = split_move(pose)
 #    		for p in poses:
 #        		make_single_move(p)

def make_single_move(pose):
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
      		#print "out"
  	except rospy.ServiceException, e:
     		print "Service call failed: %s"%e





    	while not rospy.is_shutdown():

        	make_split_move(pose)
    
    	    # if mov1[0] == 0.1 and mov1[1] == 0.0:
        	#     print "success"
        	#     break

        	flag = raw_input()
        	if flag== 's':
            		next_mov = mov1
            		next_mov[0] += 0.1
            	if next_mov[0]==x[0] and next_mov[1]==x[1]:
            		    print "warning!"
            		    next_mov[0] -= 0.1
            	else:
            		    pose.append(next_mov)
                step += 1
        	elif flag == 'w':
            		next_mov = mov1
            		next_mov[0] -= 0.1
            		if next_mov[0]==x[0] and next_mov[1]==x[1] :
            	    		print "warning!"
            	    	next_mov[0] += 0.1
            		else:
            	    	pose.append(next_mov)
            	    step += 1
        	elif flag == 'a':
            	next_mov = mov1
            	next_mov[1] -= 0.1
            	if next_mov[0]==x[0] and next_mov[1]==x[1] :
            	    print "warning!"
            	    next_mov[1] += 0.1
            	else:
            	    pose.append(next_mov)
            	    step += 1
        	elif flag == 'd':
            	next_mov = mov1
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





"""Listener"""
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
                tf_dic[key] = [translation, quaternion]

    if not tf_dic == {}: 
        position_relative = list(map(lambda x : round(abs(x[0] - x[1]), 1), 
            zip(tf_dic[wall0][0], tf_dic[origin][0])))

        create_coordinates(tf_dic)
        board = create_board(tf_dic, board)
        #print "OK"
        #print position_relative
        obj.num = position_relative
        #print obj.num


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("tf",tfMessage, callback)
    #rospy.spin()







"""Board"""

def create_coordinates(tf_dic):
    '''
    Create a list which store the Pieces storing 
    coordinates of each box, wall, destination, type and number.
    '''
    pieces = []
    for i in range(len(walls)):
        coordinate = tfdicToCoordinate(tf_dic, walls[i])
        piece = Piece(coordinate, 'WAL', i)
        pieces.append(piece)
    for i in range(len(boxes)):
        coordinate = tfdicToCoordinate(tf_dic, walls[i])
        piece = Piece(coordinate, 'BOX', i)
        pieces.append(piece)
    for i in range(len(deses)):
        coordinate = tfdicToCoordinate(tf_dic, walls[i])
        piece = Piece(coordinate, 'DES', i)
        pieces.append(piece)
    return pieces

def tfdicToCoordinate(tf_dic, key):
    """Return the coordinate of a pieces relative to origin."""
    return list(map(lambda x : round(abs(x[0] - x[1]), 3), 
            zip(tf_dic[key][0], tf_dic[origin][0])))

def pieceTolist(pieces):
    """Pieces type to common coordinates type"""
    list_pieces = []
    for p in pieces:
        list_pieces.append(p.coordinate)
    return list_pieces

def create_board(tf_dic):
    """return a new game board."""
    return update_board(tf_dic, clear_board())


def update_board(tf_dic, oldboard):
    """return a game board in 2D list. acr is the Accuracy"""
    pieces = create_coordinates(tf_dic)
    board = oldboard
    for piece in pieces:
        unit_cod = CoordinateToUnit(piece.coordinate)
        x, y = unit_cod[0], unit_cod[1]
        if piece.type == 'WAL':
            board[x][y] = '#'
        elif pieces.type == 'BOX':
            board[x][y] = '$'
        elif pieces.type == 'DES':
            board[x][y] = '.'
    return board

def CoordinateToUnit(cod):
    """Return unit coordinate"""
    _ACR = 3
    unit = round(abs(tf_dic[origin][0][0] - tf_dic[wall1][0][0]), _ACR)
    x = round(cod[0] / unit)
    y = round(cod[1] / unit)
    return [x, y, 0]


def clear_board():
    """
    Return a new empty board. With all pieces being WALL.
    Wall = '#', box = '$'
    """
    b = []
    for i in range(_LENGTH):
        row = []
        for j in range(_WIDTH):
            row.append('#')
        b.append(row)
    return b

class Piece:
    """
    The piece in each position of the board.
    type is 'WAL', 'BOX', 'DES'
    number is the number
    """
    def __init__(self, coordinate, _type, number=-1):
        self.coordinate = coordinate
        self.type = _type
        self.number = number




if __name__ == '__main__':  
    while True:
       listener()
       keyboard_control(obj.num)
       print "Ok"


