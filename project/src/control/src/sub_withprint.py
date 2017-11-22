


#Import the dependencies as described in example_pub.py
import rospy
import math
#import ar_track_alvar
#from std_msgs.msg import String
import geometry_msgs.msg
import tf
from tf.msg import tfMessage
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker
import time
import numpy as np

def callback(message):
    trans = message.transforms


    baseframe = "left_hand_camera"
    arframe3 = "ar_marker_3"
    frames = [baseframe, arframe3]

    left_hand_to_camera = ["left_hand", "left_hand_camera"]

    target_transforms_pairs = [left_hand_to_camera]


    dic = {}
    for target_tran_pair in target_transforms_pairs:
        target_head = target_tran_pair[0]
        target_child = target_tran_pair[1]
        for tran in trans:
            head = tran.header.frame_id
            child = tran.child_frame_id
            #header_receive_time = tran.header.stamp
            if (head == "reference/" + target_head 
            	and child == "reference/" + target_child):
                tfm = tran.transform
                trs = tfm.translation
                rot = tfm.rotation
                translation = [trs.x, trs.y, trs.z]
                quaternion = [rot.x, rot.y, rot.z, rot.w]
                key = target_head + '_to_' + target_child
                """
                print "transforms from {0} to {1} is".format(target_tran_pair[0], target_tran_pair[1])
                print translation
                print quaternion
                print '\n'
                print key
                """
                dic[key] = [translation, quaternion]

                
    key = 'left_hand_to_left_hand_camera'
    if key in dic.keys():
        #translation
        print dic[key][0]
        #rotation
        print dic[key][1]
    

    time.sleep(0.5)

    
    



    
    #print message.transforms[0].child
    

    """
    print tran.header
                print '\n'
                print tran.child
    for trans in message.transforms:
        print trans.child
    time.sleep(0.5)

    print trans[0].child
    print trans[0].transform.translation
    trans = message.transforms[0]
    for tran in trans:
        #print tran
        print tran.header
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", message.data) 
    print message
    """
    

def listener():

    #Run this program as a new node in the ROS computation graph
    #called /listener_<id>, where <id> is a randomly generated numeric
    #string. This randomly generated name means we can start multiple
    #copies of this node without having multiple nodes with the same
    #name, which ROS doesn't allow.
    rospy.init_node('listener', anonymous=True)

    #Create a new instance of the rospy.Subscriber object which we can 
    #use to receive messages of type std_msgs/String from the topic /chatter_talk.
    #Whenever a new message is received, the method callback() will be called
    #with the received message as its first argument.
    #print "heel"
    rospy.Subscriber("tf",tfMessage, callback)
    #print "hi"


    #Wait for messages to arrive on the subscribed topics, and exit the node
    #when it is killed with Ctrl+C
    rospy.spin()


#Python's syntax for a main() method
if __name__ == '__main__':
    listener()
