# -*- coding: utf-8 -*-
"""
Created on Fri Nov 9 18:18:16 2018

@author: johnl
"""

import argparse
import tellopy
import math
import socket
import pythonosc
import time
import errno, os, sys
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder
import multiprocessing


def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


# Array to store OSC data for further processing
TempCH1 = []
TempCH2 = []
TempCH3 = []
TempCH4 = []


def counter(x):
    counter.calls += 1
    return x + 1

first_lookLeft = False
def LookLeft():
    global first_lookLeft
    upward_spike_ch3 = any(a > 880 for a in TempCH3[(len(TempCH3) - 5):(len(TempCH3) - 1)])

    downward_spike_ch2 = any(b < 830 for b in TempCH2[(len(TempCH2) - 5):(len(TempCH2) - 1)])

    within_range_ch1 = any((740 > c or c > 920) for c in TempCH1[(len(TempCH1) - 30):(len(TempCH1) - 3)])

    if downward_spike_ch2 and upward_spike_ch3 and not within_range_ch1:

        upward_spike_ch2 = any(d > 870 for d in TempCH2[(len(TempCH2) - 30):(len(TempCH2) - 3)])

        downward_spike_ch3 = any(e < 820 for e in TempCH3[(len(TempCH3) - 30):(len(TempCH3) - 3)])

        downward_spike_ch4 = any(f < 830 for f in TempCH4[(len(TempCH4) - 30):(len(TempCH3) - 3)])

        if downward_spike_ch3 and upward_spike_ch2 and downward_spike_ch4:
          
            print("look Left")
            print("_____")
            first_lookLeft = True
            drone.backward(60)
            time.sleep(0.7)
            drone.backward(0)

            #############################################################################
            #############################################################################
            return True

    return False


def LookRight():
    downward_spike_ch3 = any(a < 810 for a in TempCH3[(len(TempCH3) - 5):(len(TempCH3) - 1)])

    downward_spike_ch4 = any(b < 810 for b in TempCH4[(len(TempCH4) - 5):(len(TempCH4) - 1)])

    within_range_ch1 = any((780 > c or c > 880) for c in TempCH1[(len(TempCH1) - 30):(len(TempCH1) - 3)])

    if downward_spike_ch3 and downward_spike_ch4 and within_range_ch1:

        upward_spike_ch3 = any(d > 870 for d in TempCH3[(len(TempCH3) - 30):(len(TempCH3) - 3)])

        downward_spike_ch2 = any((740 < e < 830) for e in TempCH2[(len(TempCH2) - 30):(len(TempCH2) - 3)])

        if upward_spike_ch3 and downward_spike_ch2:

            print("look Right")
            drone.land()
            return True
    return False


"""
def blink(unused_addr, args, ch5):
    if ch5 > 0.2:
       
        print("Blinked rigorously")
        return True
    return False
"""

"""
def Resetbool():
    global first_clench
    global first_lookLeft
    first_lookLeft = False
    first_clench = False
    Timer(3.0,Resetbool())
"""
"""
def backward():
    global first_lookLeft
    global first_clench
    if first_lookLeft == True:
        if first_clench == True:
            drone.backward(60)
            time.sleep(0.7)
            drone.backward(0)
            print ('back')
"""
first_clench = False
def Clenched():
    global drone
    global first_clench
    first_clench = True
    drone.forward(60)
    time.sleep(0.7)
    drone.forward(0)





def jawClench(unused_addr, args, ch6):
    if ch6 > 0.2:
        print("clench")
        Clenched()
        return True

    return False


# the eeg_handler function imports the OSC values with a frequence of
# 256 readings per 1 second (256/1sec = every 3.90625 milliseconds)

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    counter.calls += 1  # calling the counter function

    if counter.calls > 10:
        # print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)
        # print("counter works!!", counter.calls)
        TempCH1.append(ch1)
        TempCH2.append(ch2)
        TempCH3.append(ch3)
        TempCH4.append(ch4)

        LookLeft()
        LookRight()
 
        counter.calls = 0  # resetting the counter so that it counts back to 10 every time


# Below is the function to receive the OSC live feed from the muse
if __name__ == "__main__":

    drone = tellopy.Tello()

    drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)


    # unused var
    unused_addr = 0
    args = 0
    drone.connect()
    drone.wait_for_connection(5.0)
    drone.takeoff()

    #p1 = Process(target=Resetbool)

    #p1.start()
    #    p2.start()
    #    p1.join()
    #    p2.join()

    counter.calls = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=2000,  # make sure you change the port every time you wanna run the code
                        # for example next one would be 5050 :)

                        help="The port to listen on")
    parser.add_argument("--serial",
                        default="",
                        help="Arduino serial port")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    dispatcher.map("/muse/notch_filtered_eeg", eeg_handler, "EEG")
    dispatcher.map("/muse/elements/jaw_clench", jawClench, "EEG")
 #########################################################################   dispatcher.map("/muse/elements/blink", blink, "EEG")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


