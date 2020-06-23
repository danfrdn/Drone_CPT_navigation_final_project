
# -*- coding: UTF-8 -*-

"""
Run land.py when you want to land the drone quickly from the terminal.
"""

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import math
from time import sleep
import cv2
from video_streaming import yuv_frame_cb
import random
import time


def reset_gimbal_orientation():
    drone(olympe.messages.gimbal.reset_orientation(gimbal_id=0)).wait()


def main(drone):
    drone.connection()
    reset_gimbal_orientation()
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


if __name__ == "__main__":
    # Drone IP
    ANAFI_IP = "192.168.42.1"

    # Drone web server URL
    ANAFI_URL = "http://{}/".format(ANAFI_IP)

    with olympe.Drone(ANAFI_IP, loglevel=0) as drone:
        main(drone)