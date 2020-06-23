


import olympe
# from olympe.messages.ardrone3.PilotingSettingsState import MaxDistance, NoFlyOverMaxDistance
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import math
from time import sleep
import cv2
from video_streaming import yuv_frame_cb
import random
import time
# import detect
import os
from detect_smoke_cascade import detect_smoke_cascade
from detect_smoke_simple_grey import detect_smoke_simple_grey_board

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


def test_0_take_off_turn_and_land(drone):
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(5)
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_1_fly_straight_1_meter():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    #
    # drone(
    #     moveBy(dX=2, dY=0, dZ=0, dPsi=0)
    #     >> FlyingStateChanged(state="hovering", _timeout=5)
    # ).wait()
    sleep(100)
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_2_fly_straight_turn_fly_back():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()

    drone(
        moveBy(dX=10, dY=0, dZ=0, dPsi=0)
        >> FlyingStateChanged(state="hovering", _timeout=20)
    ).wait()

    drone(
        moveBy(dX=0, dY=0, dZ=0, dPsi=math.pi)
        >> FlyingStateChanged(state="hovering", _timeout=20)
    ).wait()

    drone(
        moveBy(dX=10, dY=0, dZ=0, dPsi=0))
    #     >> FlyingStateChanged(state="hovering", _timeout=20)
    # ).wait()

    drone(CancelMoveBy(_timeout=10))

    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_3_fly_straight_2_seconds():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(5)

    drone(
        moveBy(dX=5, dY=0, dZ=0, dPsi=0)
        >> FlyingStateChanged(state="hovering", _timeout=2)
    ).wait()

    sleep(5)
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_4_takeoff_detect_plume_land():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(5)

    start = time.time()
    counter = time.time() - start
    while smoke_detect() is False and counter<=30:
        continue

    sleep(5)
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_5_gimbal_move():
    change_gimbal_angle(-90)
    sleep(10)
    reset_gimbal_orientation()


def test_6_streaming_with_detect():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    # drone.start_video_streaming()
    # video = cv2.VideoCapture("rtsp://192.168.42.1/live", cv2.CAP_FFMPEG)
    start_time = time.time()
    while time.time() - start_time < 60:
        # define video stream:
        check, frame = video.read()
        # status, img = detect_smoke_cascade(frame)
        # print(status)
        # cv2.imshow("sd", img)
        print(detect_smoke_simple_grey_board(frame))
        cv2.waitKey(1)

    # drone.stop_video_streaming()
    drone.disconnection()


def test_7_detect_and_move():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    # drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()

    change_gimbal_angle(-80)
    sleep(1)

    start_time = time.time()
    while time.time() - start_time < 500:
        tc = detect.detect()
        if tc > 0:
            drone(
                moveBy(dX=2, dY=0, dZ=0, dPsi=0)
                >> FlyingStateChanged(state="hovering", _timeout=5)
            ).wait()
            break

    reset_gimbal_orientation()
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_8_detect_and_move_continuesly():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    # drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()

    change_gimbal_angle(-80)
    sleep(2)

    counter=0
    start_time = time.time()
    while time.time() - start_time < 500 and counter < 2:
        tc = detect.detect()
        if tc > 0:
            drone(
                moveBy(dX=1, dY=0, dZ=0, dPsi=0)
                >> FlyingStateChanged(state="hovering", _timeout=5)
            ).wait()
            counter += 1

    reset_gimbal_orientation()
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_9_calculate_drone_speed():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    # drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()

    counter = 3
    while counter <6:
        start_time = time.time()
        distance = 1 * counter

        drone(
            moveBy(dX=distance, dY=0, dZ=0, dPsi=0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait()

        speed = distance / (time.time()-start_time)
        print("speed [m/s]: ", speed)
        counter+=1


    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def test_10_reach_target():
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    change_gimbal_angle(-85)
    print("------take off-------")
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(2)

    while detect() != 'blue':
        drone(
            moveBy(dX=1, dY=0, dZ=0, dPsi=0)
            >> FlyingStateChanged(state="hovering", _timeout=20)
        ).wait()

    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()


def main(drone):
    drone.connection()

    try:
        test_1_fly_straight_1_meter()
    except KeyboardInterrupt:
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

