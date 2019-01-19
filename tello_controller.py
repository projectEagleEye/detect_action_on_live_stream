"""
Name: tello_controller.py
Author: Shi Jie (Barney) Wei
Date of Creation: 01/18/18
Last Modified Date: 01/18/19

Description:
    - connects to the tello 3 drone
    - control the drone
    - implements tellopy library
"""

# Import libraries and packages
import tellopy
import time

tello_drone = tellopy.Tello()
tello_drone.connect()
tello_drone.takeoff()
time.sleep(3)
tello_drone.land()

