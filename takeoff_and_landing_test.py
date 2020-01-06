
# -*- coding: UTF-8 -*-

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
import math
from time import sleep

# Drone IP
ANAFI_IP = "192.168.42.1"

# Drone web server URL
ANAFI_URL = "http://{}/".format(ANAFI_IP)

def take_off_turn_and_land(drone):
    drone(TakeOff() >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    sleep(5)
    # moveBy((1, 0, 0, 0) >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    # moveBy((0, 0, 0, math.pi) >> FlyingStateChanged(state="hovering", _timeout=5)).wait()
    drone(Landing() >> FlyingStateChanged(state="landed", _timeout=5)).wait()
    drone.disconnection()

def main(drone):
    drone.connection()
    take_off_turn_and_land(drone)
    drone.disconnection()

if __name__ == "__main__":
    with olympe.Drone(ANAFI_IP, loglevel=0) as drone:
        main(drone)