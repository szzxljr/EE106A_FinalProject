import rospy
import math
import geometry_msgs.msg
import tf
from tf.msg import tfMessage
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
import time
import numpy as np

from frames import *

dic = {}
#global position_relative
position_relative = []


class a():
    num = 0

obj = a() 

def callback(message):
    
     
    # obj.num += 1
    # print obj.num
    """    
    for target_tran_pair in target_transforms_pairs:
        target_head = target_tran_pair[0]
        target_child = target_tran_pair[1]
        for tran in message.transforms:
            head = tran.header.frame_id
            child = tran.child_frame_id
            #print 'head:' + head + '   child:' + child
            #header_receive_time = tran.header.stamp
            if (head == '/' + target_head 
            	and child == target_child):
                tfm = tran.transform
                trs = tfm.translation
                rot = tfm.rotation
                translation = [trs.x, trs.y, trs.z]
                quaternion = [rot.x, rot.y, rot.z, rot.w]
                key = target_head + '_to_' + target_child
                dic[key] = [translation, quaternion]
    if not (dic == {}):            
        print dic
    #time.sleep(0.5)
    """   
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
                # print dic[key]
    if not dic == {}: 
        
        #position_relative = []
        key3 = 'right_hand_camera_to_ar_marker_3'
        key5 = 'right_hand_camera_to_ar_marker_5'
        """
        print dic[key5]
        for i in range(2):
            position_relative[i] = dic[key5][0][i] - dic[key3][0][i]
        """
        
        position_relative = list(map(lambda x : round(x[0] - x[1], 1), 
            zip(dic[key5][0], dic[key3][0])))
        print "OK"
        print position_relative

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("tf",tfMessage, callback)
    rospy.spin()
if __name__ == '__main__':  
    listener()
