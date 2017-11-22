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
from make_move import *

boxes_axis = {}
tf_dic = {}
position_relative = []
board = []

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
    mov1 = [0.10, 0.20, 0.00,0.783, -0.621, 0.042, -0.004]
    pose = [mov1]

    while not rospy.is_shutdown(): 

        make_split_move(pose)
    
        if mov1[0] == 0.1 and mov1[1] == 0.0:
            print "success"
            break

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
        
        origin = 'right_hand_camera_to_ar_marker_3'
        wall1 = 'right_hand_camera_to_ar_marker_0'
        wall2 = 'right_hand_camera_to_ar_marker_1'
        wall3 = 'right_hand_camera_to_ar_marker_2'
        wall4 = 'right_hand_camera_to_ar_marker_4'
        wall5 = 'right_hand_camera_to_ar_marker_5'
        wall6 = 'right_hand_camera_to_ar_marker_6'
        box1 = 'right_hand_camera_to_ar_marker_7'
        box2 = 'right_hand_camera_to_ar_marker_8'
        
        position_relative = list(map(lambda x : round(abs(x[0] - x[1]), 1), 
            zip(tf_dic[wall1][0], tf_dic[origin][0])))

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
origin = 'right_hand_camera_to_ar_marker_3'
wall1 = 'right_hand_camera_to_ar_marker_0'
wall2 = 'right_hand_camera_to_ar_marker_1'
wall3 = 'right_hand_camera_to_ar_marker_2'
wall4 = 'right_hand_camera_to_ar_marker_4'
wall5 = 'right_hand_camera_to_ar_marker_5'

wall6 = 'right_hand_camera_to_ar_marker_6'
box1 = 'right_hand_camera_to_ar_marker_7'
box2 = 'right_hand_camera_to_ar_marker_8'
des1 = 'right_hand_camera_to_ar_marker_9'
des2 = 'right_hand_camera_to_ar_marker_10'

def create_coordinates(tf_dic):
    '''
    create a dictionary which store the coordinates of 
    each box, wall, destination.
    '''
    unit_length = round(abs(tf_dic[origin][0][0] - tf_dic[wall1][0][0]), 3)
    pieces = []
    for _ in range(len(tf_dic)):
        coordinate = list(map(lambda x : round(abs(x[0] - x[1]), 3), 
            zip(tf_dic[wall1][0], tf_dic[origin][0])))
        pieces






def create_board(tf_dic, oldboard):
    unit_length = 

class Piece:
    """
    The piece in each position of the board.
    """
    def __init__(self, coordinate, type, number=0):
        self.coordinate = coordinate
        self.type = type
        self.number = number


if __name__ == '__main__':  
    while True:
       listener()
       keyboard_control(obj.num)
       print "Ok"


