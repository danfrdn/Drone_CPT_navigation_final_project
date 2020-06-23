# -*- coding: UTF-8 -*-
# documentation link: https://developer.parrot.com/docs/olympe/arsdkng_ardrone3_piloting.html
######## functions used in flight algorithm ###########

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
from detection_function import detect

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


def write_detect_func_output():
    f_handle = open("detection_output.txt", "w")
    output = detect()
    f_handle.write(str(output))
    f_handle.close()

def read_detect_func_output():
    f_handle = open("detection_output.txt", "r")
    state = f_handle.readline()
    f_handle.close()
    if state == "False":
        return False
    elif state == "success":
        return "success"
    else:
        return True


def wait_to_start():
    """
    wait in hovering mode until first smoke sign is detected
    :param cv2frame: frame of image
    :return: tc - amount of time drone in smoke
    """

    while read_detect_func_output() is False:
        sleep(0.1)
        print("wait_to_start")
    return


def wait_for_plume_or_until_t(tc, casting_memory):
    """
    hover until another grey plume comes for a maximum of t seconds, if it comes than count tc and fly straight.
    If it dos not arrive, return False.
    :param tc: time drone detected inside plume [sec]
    :return: boolean - FALSE if reached maximum time tc or TRUE if next plume is detected before max time
    """
    wait_start_time = time.time()
    while time.time() - wait_start_time < tc:
        sleep(0.5)
        print("waiting for plume")
        if read_detect_func_output() is True:
            new_tc = count_time_and_fly_straight(casting_memory)
            print("detected plume, new tc: ", new_tc)
            return new_tc
    print("did not detect new plume, reached tc=",tc)
    return False


def turn_angle_needed_to_face_upwind_in_rad(turn_memory):
    turn_sum = 0
    for i in turn_memory:
        turn_sum+=i

    print("----turn memory sum: {}".format(turn_sum))
    while turn_sum > 2*math.pi:
        turn_sum -= 2*math.pi
    if turn_sum ==0:
        return 0
    elif turn_sum <= math.pi:
        return (-1) * turn_sum
    else:
        return (2 * math.pi) - turn_sum


def casting_with_moveby(tc, casting_memory):
    """
    If no new plume is detected, we use CASTING. Pick a random angle between 30 to 120 degrees, turn CCW to face this degree and fly for tc seconds.
    Continue this pattern until a new plume is detected or until a miximum ammout of turns which we will define as a "failed attempt".
    There is a need to "remember" every counterturn the Drone makes in order to fly back "upwind" (degree 0) once a plume is detected.
    :param tc - time in plume [sec]
    :return: True if plume detected
    """

    degree = random.randint(30, 120)
    rad = degree * math.pi / 180
    print("degree: ",degree)
    print("rad: ", rad)
    casting_memory.append(rad)

    # turn:
    # olympe.messages.ardrone3.Piloting.moveBy(dPsi=rad).wait()
    print("casting turn: ",degree)
    drone(moveBy(dX=0, dY=0, dZ=0, dPsi=rad) >> FlyingStateChanged(state="hovering", _timeout=20)).wait()
    # print("we turned: ", rad)
    print("casting fly: ",dx(tc))
    drone(moveBy(dX=dx(tc), dY=0, dZ=0, dPsi=0) >> FlyingStateChanged(state="hovering", _timeout=20)).wait()
    # print(" moved after casting for time tc = ", tc)

    return casting_memory


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


def reset_gimbal_orientation():
    drone(olympe.messages.gimbal.reset_orientation(gimbal_id=0)).wait()


def count_time_while_in_plume():
    """
    count time that smoke is being detected
    :return: tc
    """
    start_time = time.time()
    while read_detect_func_output() is True:
        continue
    tc = time.time() - start_time
    return tc


def count_time_and_fly_straight(casting_memory):
    """
    count time that smoke is being detected and fly straight for that amount of time
    """
    tc=0
    while tc < 0.5:
        tc = count_time_while_in_plume()
    print("detected plume for tc = {}, fly: {}".format(tc,dx(tc)))
    upwind_rad = turn_angle_needed_to_face_upwind_in_rad(casting_memory)
    drone(moveBy(dX=0, dY=0, dZ=0, dPsi=upwind_rad) >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    print("------ moving: {}  -----".format(dx(tc)))
    drone(moveBy(dX=dx(tc), dY=0, dZ=0, dPsi=0) >> FlyingStateChanged(state="hovering", _timeout=tc+20)).wait()
    return tc


def dx(tc, acceleration=0.2):
    """
    acceleration = 0.2 m/s
    """
    return acceleration * (tc**2)/2

