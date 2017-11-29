
"""
3 is origin
11 is gripper position
"""
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
			"ar_marker_10",
			"ar_marker_11",]
target_transforms_pairs = []
usb_cam = "usb_cam"
for arframe in arframes:
    target_transforms_pairs += [[usb_cam, arframe]]

"""
ar = "ar_marker_"
for i in range(1, 10):
	arframes += [ar + str(i)]
"""