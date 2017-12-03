import rospy
import math
import geometry_msgs.msg
import tf
from tf.msg import tfMessage
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
import time
import numpy as np
import os

from frames import *

dic = {}
#global position_relative
position_relative = []


class a():
    num = [['','','','',],['','','','',],['','','','',],['','','','',]]

obj = a() 

def callback(message):
    # print obj.num
    for tran in message.transforms:
        head = tran.header.frame_id
        child = tran.child_frame_id
        for target_tran_pair in target_transforms_pairs:
            target_head = target_tran_pair[0]
            target_child = target_tran_pair[1]
            if (head == target_head 
                and child == target_child):
                tfm = tran.transform
                trs = tfm.translation
                rot = tfm.rotation
                translation = [round(trs.x,3), round(trs.y,3), round(trs.z,3)]
                quaternion = [round(rot.x,3), round(rot.y,3), round(rot.z,3), round(rot.w,3)]
                key = target_head + '_to_' + target_child

                dic[key] = [translation, quaternion]
                # print dic[key]
                # print "test1"
	
    if not dic == {}: 
        position_relative=[[],[],[],[],[],[],[],[],[],[],[],[]]
        
        #position_relative = []
        key0 = "usb_cam_to_ar_marker_0"
        key1 = "usb_cam_to_ar_marker_1"
        key2 = "usb_cam_to_ar_marker_2"
        key3 = "usb_cam_to_ar_marker_3"
        key4 = "usb_cam_to_ar_marker_4"
        key5 = "usb_cam_to_ar_marker_5"
        key6 = "usb_cam_to_ar_marker_6"
        key7 = "usb_cam_to_ar_marker_7"
        key8 = "usb_cam_to_ar_marker_8"
        key9 = "usb_cam_to_ar_marker_9"
        key10 = "usb_cam_to_ar_marker_10"
        key11 = "usb_cam_to_ar_marker_11"
        def position(x):
        	return round(abs(x[0]-x[1]),3)
        position_relative[0] = map(position, zip(dic[key0][0], dic[key0][0]))
        position_relative[1] = map(position, zip(dic[key1][0], dic[key0][0]))
        position_relative[2] = map(position, zip(dic[key2][0], dic[key0][0]))
        position_relative[3] = map(position, zip(dic[key3][0], dic[key0][0]))
        position_relative[4] = map(position, zip(dic[key4][0], dic[key0][0]))
        position_relative[5] = map(position, zip(dic[key5][0], dic[key0][0]))
        position_relative[6] = map(position, zip(dic[key6][0], dic[key0][0]))
        position_relative[7] = map(position, zip(dic[key7][0], dic[key0][0]))
        position_relative[8] = map(position, zip(dic[key8][0], dic[key0][0]))
        position_relative[9] = map(position, zip(dic[key9][0], dic[key0][0]))
        position_relative[10] = map(position, zip(dic[key10][0], dic[key0][0]))
        position_relative[11] = map(position, zip(dic[key11][0], dic[key0][0]))
        

        game_map = [['-','-','-','-'],['-','-','-','-'],['-','-','-','-'],['-','-','-','-']]
        unit_length = position_relative[1][0]-position_relative[0][0]
        def position_relative_unit(x):
        	if x < 0.5*unit_length:
        		return 0*unit_length
        	elif x>0.5*unit_length and x<1.5*unit_length:
        		return 1*unit_length
        	elif x>1.5*unit_length and x<2.5*unit_length:
        		return 2*unit_length
        	elif x>2.5*unit_length and x<3.5*unit_length:
        		return 3*unit_length
        	else:
        		return "cube out of the map"
        # print unit_length

        for i in range(12):
            for j in range(3):
                position_relative[i][j] = position_relative_unit(position_relative[i][j])
                for k in range(0,4):
                    if position_relative[i][j] == k*unit_length:
        				position_relative[i][j] = k
        #print game_map
        #print position_relative
        box0 = position_relative[0]
        box1 = position_relative[1]
        box2 = position_relative[2]
        box3 = position_relative[3]
        box4 = position_relative[4]
        box5 = position_relative[5]
        box6 = position_relative[6]
        cube1 = position_relative[7]
        cube2 = position_relative[8]
        des1 = position_relative[9]
        des2 = position_relative[10]
        man = position_relative[11]
        game_map[cube1[1]][cube1[0]] = "$1"
        game_map[cube2[1]][cube2[0]] = "$2"  
        game_map[box0[1]][box0[0]] = "#"
        game_map[box1[1]][box1[0]] = "#"
        game_map[box2[1]][box2[0]] = "#"
        game_map[box3[1]][box3[0]] = "#"
        game_map[box4[1]][box4[0]] = "#"
        game_map[box5[1]][box5[0]] = "#"
        game_map[box6[1]][box6[0]] = "#"
        game_map[des1[1]][des1[0]] = ".1"
        game_map[des2[1]][des2[0]] = ".2"
        game_map[man[1]][man[0]] = "@"
        data = os.path.getsize('map.txt')
        print data
        # print game_map
        # if data != 0:
        #     f = open('map.txt','r+')
        #     f.truncate()
        #     f.close()
        
        for p in range(4):
        	for q in range(4):
        		if data == 0:
        			map_file = open("map.txt","a")
        			map_file.write(str(game_map[p][q]))
        			map_file.write('\n')
        			map_file.close()
        

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("tf",tfMessage, callback)
    rospy.spin()
if __name__ == '__main__':  
    listener()
