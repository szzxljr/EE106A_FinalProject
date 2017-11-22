#Listener frames
target_transforms_pairs = []
right_hand_camera = "right_hand_camera"
arframes = ["ar_marker_3",
			"ar_marker_0",
			"ar_marker_1",
			"ar_marker_2",
			"ar_marker_4",
			"ar_marker_5",
			"ar_marker_6",
			"ar_marker_7",
			"ar_marker_8",
			"ar_marker_9",
			"ar_marker_10"]

for arframe in arframes:
    target_transforms_pairs += [[right_hand_camera, arframe]]

#Dictionary keys
origin = 'right_hand_camera_to_ar_marker_3'
wall0 = 'right_hand_camera_to_ar_marker_0'
wall1 = 'right_hand_camera_to_ar_marker_1'
wall2 = 'right_hand_camera_to_ar_marker_2'
wall3 = 'right_hand_camera_to_ar_marker_4'
wall4 = 'right_hand_camera_to_ar_marker_5'
wall5 = 'right_hand_camera_to_ar_marker_6'
box0 = 'right_hand_camera_to_ar_marker_7'
box1 = 'right_hand_camera_to_ar_marker_8'
des0 = 'right_hand_camera_to_ar_marker_9'
des1 = 'right_hand_camera_to_ar_marker_10'

walls = [wall0, wall1, wall2, wall3, wall4, wall5]
boxes = [box0, box1]
deses = [des0, des1]
pieces_frame = [walls, boxes, deses]

"""
ar = "ar_marker_"
for i in range(1, 10):
	arframes += [ar + str(i)]
"""