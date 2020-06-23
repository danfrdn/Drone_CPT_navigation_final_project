import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def detect(frame):
    """
    Detect smoke via hsv video processing using OpenCV.
    :param frame:
    :return:
    """
    # OpenCV works in BGR format - convert to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV OpenCV values - H: 0-179, S: 0-255, V: 0-255
    # Grey (smoke):
    low_grey_color = np.array([80, 10, 170])
    high_grey_color = np.array([120, 70, 245])

    # White (End):
    low_white_color = np.array([75, 0, 175])
    high_white_color = np.array([175, 5, 200])

    # create a mask on the video - showing only section within the threshold
    grey_mask = cv2.inRange(hsv_frame, low_grey_color, high_grey_color)
    grey = cv2.bitwise_and(frame, frame, mask=grey_mask)

    white_mask = cv2.inRange(hsv_frame, low_white_color, high_white_color)
    white = cv2.bitwise_and(frame, frame, mask=grey_mask)

    ########################### Threshold - change if necessery ###############################
    threshold = 0.01
    ###########################################################################################

    # create blue box when successfully reached end:
    if np.count_nonzero(grey) / white.size > threshold:
        cv2.rectangle(frame, (0, 0), (1280, 720), (255, 0, 0), 50)

    # create green box when successfully detected smoke:
    if np.count_nonzero(grey) / grey.size > threshold:
        cv2.rectangle(frame, (0, 0), (1280, 720), (0, 255, 0), 50)


    # show original frame and mask frame (frame where only smoke is visible - for testing):
    cv2.imshow("Frame", frame)
    cv2.imshow("grey", grey)
    cv2.waitKey(1)

    # calculate the percent of 'success' (white cloth) or smoke (grey) out of the whole image:
    if np.count_nonzero(white) / white.size > threshold:
        # if white cloth detected return "success"
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~ Success')
        return 'success'
    if np.count_nonzero(grey) / grey.size >threshold:
        # if smoke (grey) is detected return True
        print("########################## True  ", np.count_nonzero(grey) / grey.size)
        return True
    else:
        return False





