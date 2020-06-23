# Chemical Plume Tracing By Drone In Turbulant Wind
Drone navigation in turbulent wind, the navigation algorithm is based on moth biomimetics. In turbulent wind, airosols disperse in a non-laminar fashion, resulting in airosol plumes that vary in size and consistency. CPT (chemical plume tracing) is the challenge of navigating to the source of the airosol and is documented heavily in literature. 

We have based our algorithm on a study on Moth navigation via feromone plumes to find female counterparts (Moth-inspired navigation algorithm in a turbulent odor plume from a pulsating source, Liberzon 2018) .

Our mission:
create an algorithm which can detect the source, of any airosol the client would like to trace.

All the user will need to do is attach the relevent sensor to the drone, and create a simple detection function that returns a boolean "True" or "False", measuring when the drone detects a plume.

As a start, we have used the drone's built-in camera and a smoke machine to write and test the algorithm. Therefore, our detection function detects traces of smoke in the drone's vecinity (the camera was angled to the ground so smoke will only be dtetected when reaching the drone).

Notes:
- The detection function needs to be written as "detect()" in the "detection_function.py" file.
- The detection needs to occur asynchronously to the drone navigation, hence multithreading should be used and can be implemented according to this link: https://docs.python.org/3/library/threading.html (we have not implemented this since the drone's streaming is asynchronous built-in).
 
Specifications:
- Drone: Parrot Anafi 
- Commands Library: Olympe by Parrot https://developer.parrot.com/docs/olympe/
