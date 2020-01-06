
# -*- coding: UTF-8 -*-
from time import sleep
import olympe
import math
import cv2

# Drone IP
ANAFI_IP = "192.168.42.1"

# Drone web server URL
ANAFI_URL = "http://{}/".format(ANAFI_IP)


def stream(drone):
    # drone.set_streaming_output_files()
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    sleep(10)
    drone.stop_video_streaming()

def yuv_frame_cb(yuv_frame):
    """
    This function will be called by Olympe for each decoded YUV frame.

        :type yuv_frame: olympe.VideoFrame
    """
    # the VideoFrame.info() dictionary contains some useful informations
    # such as the video resolution
    info = yuv_frame.info()
    height, width = info["yuv"]["height"], info["yuv"]["width"]

    # convert pdraw YUV flag to OpenCV YUV flag
    cv2_cvt_color_flag = {
        olympe.PDRAW_YUV_FORMAT_I420: cv2.COLOR_YUV2BGR_I420,
        olympe.PDRAW_YUV_FORMAT_NV12: cv2.COLOR_YUV2BGR_NV12,
    }[info["yuv"]["format"]]

    # yuv_frame.as_ndarray() is a 2D numpy array with the proper "shape"
    # i.e (3 * height / 2, width) because it's a YUV I420 or NV12 frame

    # Use OpenCV to convert the yuv frame to RGB
    cv2frame = cv2.cvtColor(yuv_frame.as_ndarray(), cv2_cvt_color_flag)

    # Use OpenCV to show this frame
    cv2.imshow("Olympe Streaming Example", cv2frame)
    cv2.waitKey(1)  # please OpenCV for 1 ms...


def main(drone):
    drone.connection()
    stream(drone)
    drone.disconnection()

if __name__ == "__main__":
    with olympe.Drone(ANAFI_IP, loglevel=0) as drone:
        main(drone)