import numpy as np

split = 10

def split_move(pose):
    """
    Split one destination coordinates to split pieces.
    Return the series of result.
    """
    pose = np.array(pose)
    poses = np.dstack([np.linspace(0, x, split) for x in pose])[0]
    return poses

mov1 = [1, 2, 3, 4, 5, 6, 7]
make_split_move(mov1)

def make_split_move(pose):
    '''
    split and do the move.
    '''
    poses = split_move(pose)
    for p in poses:
        make_single_move(p)

def make_single_move(pose):
    '''
    Do a single move.
    '''
    s = pose[0]
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
        response = compute_ik(request)
        group = MoveGroupCommander("left_arm")
        group.set_pose_target(request.ik_request.pose_stamped)
        group.go()
        print "in"
        print  x
        print "out"
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e




    

