target_transforms_pairs = []
usb_cam = "usb_cam"
# ar = "ar_marker_"
arframes = ["ar_marker_3",
			"ar_marker_0",
			"ar_marker_1",
			"ar_marker_2",
			"ar_marker_4",
			"ar_marker_5",
			"ar_marker_6",
			"ar_marker_7",
			"ar_marker_8",]

# for i in range(1, 10):
# 	arframes += [ar + str(i)]

for arframe in arframes:
    target_transforms_pairs += [[usb_cam, arframe]]

"""
base_frame_to_left_hand_camera = [["base", "left_hand_camera"]]
target_transforms_pairs += base_frame_to_left_hand_camera


left_hand_to_camera = [["left_hand", "left_hand_camera"]]
target_transforms_pairs += left_hand_to_camera


target_transforms_pairs += [["left_hand", "left_gripper_mass"]]
"""
print target_transforms_pairs

