import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import math
from time import sleep
import cv2
from video_streaming import yuv_frame_cb

# Drone IP
ANAFI_IP = "192.168.42.1"

# Drone web server URL
ANAFI_URL = "http://{}/".format(ANAFI_IP)

def take_off_turn_and_land(drone):
    drone.set_streaming_callbacks(raw_cb=yuv_frame_cb)
    drone.start_video_streaming()
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(5)
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.stop_video_streaming()
    drone.disconnection()

def main(drone):
    drone.connection()
    take_off_turn_and_land(drone)
    drone.disconnection()

if __name__ == "__main__":
    with olympe.Drone(ANAFI_IP, loglevel=0) as drone:
        main(drone)