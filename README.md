# Drone Chemical Plume Tracing In Turbulent Wind #
Drone navigation in turbulent wind, the navigation algorithm is based on moth biomimetics. In turbulent wind, aerosols disperse in a non-laminar fashion, resulting in aerosol plumes that vary in size and consistency. CPT (chemical plume tracing) is the challenge of navigating to the source of the aerosol and is documented heavily in literature. 

We have based our algorithm on a study on Moth navigation via pheromone plumes to find female counterparts (Moth-inspired navigation algorithm in a turbulent odor plume from a pulsating source, Liberzon 2018) .

 ### Our mission: ###
Create an algorithm which can detect the source of any aerosol/chemical the client would like to trace.

All a user will need to do is attach the relevant sensor to the drone, and create a simple detection function that returns a boolean "True" or "False", measuring when the drone detects a plume.

As a start, we have used the drone's built-in camera and a smoke machine to write and test the algorithm. Therefore, our detection function detects traces of smoke in the drone's vicinity (the camera was angled to the ground so smoke will only be detected when reaching the drone).

### Documentation: ###
- Olympe is a library released by the Parrot company to control their drones and it works on liux machines.
- Download Ubuntu 18.04: https://releases.ubuntu.com/18.04/
- Dual boot (if necessary): https://www.howtogeek.com/187789/dual-booting-explained-how-you-can-have-multiple-operating-systems-on-your-computer/
- Download Olympe: https://github.com/Parrot-Developers/olympe
- Once Olympe is downloaded, run the Olympe environment from the terminal ("source .../parrot-groundsdk/products/olympe/linux/env/shell"), if successful you will notice the env name change to "(olympe-python3)".
- We recommend running the "tests_file.py" file from the terminal, start from “test_0”  function and changing the tests in the main(), just to get the hang of the drone, to make sure all functions work properly and to understand how to control it first.
- In order for the drone to detect the chosen aerosol/chemical you need to mount the necessary sensor to the drone and transfer the code to an external controller (Raspberry pie). Then, write a detection function which reads the sensor and returns True if the chemical is present, False if not and "success" if the source is reached.
- The detection function needs to be written as "detect()" in the "detection_function.py" file - switch the current function.
- The detection needs to occur asynchronously to the drone navigation, hence multithreading should be used and can be implemented according to this link: https://docs.python.org/3/library/threading.html .we did not need to implement this since the drone's streaming is asynchronous out-of-the-box, but we have highlighted where this should be done in the "flight.py" file.
- Important (!!!): we encountered issues with reading the output of the "detect()" function when running parallel to the navigation function. To solve this issue, we came up with a workaround, the output is writen to a text file - "detect_output.txt". When the detection state is required in the algorithm, we read the current state from this file. See "write_detect_func_output()" & "read_detect_func_output()" functions in "flight_alg_functions.py" file. 
- We have highlighted (commented) the location of the detect function in the "flight.py" file, un-comment to use your detect() function. This is neccessery since we used the built-in camera to detect the smoke (airosol) and therefore needed to insert our detection into the "yuv_frame_cb()" function in the "video_streaming.py" file.
- Run the "flight.py" file from the terminal to initiate the drone flight and navigation.



#### Notes: ####
- To cancel the test and land the drone immediatly you can press ctrl+c from the terminal.
- If ctrl+c doesn't work -> run the "land_sos.py" file from the terminal.

 
 #### Specifications: ####
- Drone: Parrot Anafi 
- Commands Library: Olympe by Parrot https://developer.parrot.com/docs/olympe/
- OS: Ubuntu 18.04
- Environment: Olympe 

##### dependencies: #####
- olympe
- opencv
- matplotlib
- numpy


Example Video:
https://www.youtube.com/watch?v=AQOPfjAKT-M
