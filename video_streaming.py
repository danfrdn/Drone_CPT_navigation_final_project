
# -*- coding: UTF-8 -*-
from time import sleep
import olympe
import math
import cv2
from detect_smoke_cascade import detect_smoke_cascade
from detect_smoke_hsv import detect_smoke_hsv
import time
from threading import Thread


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

    # We used the drone's camera to detect smoke, so the detect function is used here:
    detect_output = detect_smoke_hsv(cv2frame)
    f_handle = open("detection_output.txt", "w")
    f_handle.write(str(detect_output))
    f_handle.close()

    # # Use OpenCV to show this frame
    # # Uncomment to show drone streaming on screen:
    # cv2.imshow("Olympe Streaming Example", cv2frame)
    # cv2.waitKey(1)  # please OpenCV for 1 ms...




def change_gimbal_angle(angle=-80):
    """
    not sure if this really works, need to test.
    taken from this link: https://forum.developer.parrot.com/t/how-to-control-gimbal-from-olympe-script/9421/22
    :return:
    """
    drone(olympe.messages.gimbal.set_target(
        gimbal_id=0,
        control_mode="position",
        yaw_frame_of_reference="none",  # None instead of absolute
        yaw=0.0,
        pitch_frame_of_reference="absolute",
        pitch=angle,
        roll_frame_of_reference="none",  # None instead of absolute
        roll=0.0,
    )).wait()


def stream_test(drone):
    change_gimbal_angle(0)
    # drone.set_streaming_output_files()
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    # drone.start_video_streaming("Bee - 4773.mp4")
    drone.start_video_streaming()
    start_t= time.time()
    while time.time()-start_t<500:
        # print(time.time()-start_t)
        f_handle = open("state.txt", "r")
        print(f_handle.readline())
        f_handle.close()

    sleep(1000)
    drone.stop_video_streaming()


def main(drone):
    # Drone IP
    ANAFI_IP = "192.168.42.1"
    # Drone web server URL
    ANAFI_URL = "http://{}/".format(ANAFI_IP)

    drone.connection()
    stream_test(drone)
    drone.disconnection()

if __name__ == "__main__":

    with olympe.Drone(ANAFI_IP, loglevel=0) as drone:
        main(drone)