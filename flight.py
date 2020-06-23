
# -*- coding: UTF-8 -*-
# documentation link: https://developer.parrot.com/docs/olympe/arsdkng_ardrone3_piloting.html

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import math
from time import sleep
import cv2
from video_streaming import yuv_frame_cb
import random
import time
import os
from detect_smoke_cascade import detect_smoke_cascade
from threading import Thread
from flight_alg_functions import *
from detection_function import detect
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


def flight_algorithm():
    """
    Flight algorithm. Run flight.py from the terminal to initiate drone.
    """

    # test maximum run time until considered failure [sec]:
    test_max_time = 6000
    casting_memory = []

    # set drone param:
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    change_gimbal_angle(-60)
    sleep(1)

    # take off:
    print("------take off-------")
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(1)

    # wait for first plume detection, while not detected stay in place, if detected move forward:
    wait_to_start()
    tc = count_time_and_fly_straight(casting_memory)

    # initialize test start time, and casting angle memory so we can fly "straight" once detect() is True.
    # in the future the drone will need to be able to analyze where the wind is coming from and fly in that direction.
    casting_memory=[]
    test_start_time = time.time()

    ########### main algorithm: ###########
    # while the drone hasn't reached the source (='success')
    while read_detect_func_output() != 'success' and (time.time() - test_start_time) < test_max_time:

        print("----started flight algorithm loop------")

        if read_detect_func_output() is True:

            tc = count_time_and_fly_straight(casting_memory)
            casting_memory = []

        if read_detect_func_output() is False:
            print("----------didnt find next plume going into casting mode----------")
            if wait_for_plume_or_until_t(tc, casting_memory) is False:
                print("----------start casting----------")
                casting_memory = casting_with_moveby(tc,casting_memory)


    ######## end of run #########

    print("...landing...")
    reset_gimbal_orientation()
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def main(drone):

    drone.connection()
    # try-except so if something goes run, press ctrl-c from the terminal and the drone will land immediately
    try:
        flight_algorithm()
    except KeyboardInterrupt:
        reset_gimbal_orientation()
        drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()

    drone.stop_video_streaming()
    drone.disconnection()


if __name__ == "__main__":

    # Enter drone parameters:
    # Drone IP
    ANAFI_IP = "192.168.42.1"

    # Drone web server URL
    ANAFI_URL = "http://{}/".format(ANAFI_IP)

    with olympe.Drone(ANAFI_IP, loglevel=0) as drone:
        main(drone)



