import DroneTest, Working_Tello_Test
from time import sleep
import tellopy
import multiprocessing
from multiprocessing import Process
import time

#########################################
##########importing muse related libraries
#########################################

import argparse
import math
import socket
import os
import pythonosc
import time
import sys
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder

###################################################
###################################################

"""
if __name__ == '__main__':
    for bot in ('bot1','bot2'):
       p = multiprocessing.Process(target=lambda: __import__(bot))
       p.start()
"""

def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


def Test():
    if is_jaw_clench:
        print('The freaking jaw clenched')


def Drone():
    print('Muse')
    drone = tellopy.Tello()
    try:
        drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)

        # unused var
        unused_addr = 0
        args = 0
        drone.connect()
        drone.wait_for_connection(60.0)
        drone.takeoff()
        time.sleep(5)
        drone.forward(40)
        time.sleep(5)
        if is_jaw_clench:
            drone.forward(1)
        elif LookLeft():
            drone.land()
        elif LookRight():
            drone.right(1)
    except Exception as ex:
        print(ex)
    finally:
        drone.quit()


# Array to store OSC data for further processing
TempCH1 = []
TempCH2 = []
TempCH3 = []
TempCH4 = []

# Global Variable
is_jaw_clench = False;

def counter(x):
    counter.calls += 1
    return x + 1

def LookLeft():
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
            return True
    return False

"""
def blink(unused_addr, args, ch5):
    if ch5 > 0.2:

        print("Blinked rigorously")
        return True
    return False
"""

def jawClench(unused_addr, args, ch6):
    global is_jaw_clench
    if ch6 > 0.2:
        print("clench")
        is_jaw_clench = True
        return True
    is_jaw_clench = False
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

counter.calls = 0


#def Muse():



if __name__ == '__main__':
    p1 = Process(target=Drone)

    print('hello')

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=1000,  # make sure you change the port every time you wanna run the code
                        # for example next one would be 5050 :)

                        help="The port to listen on")
    parser.add_argument("--serial",
                        default="",
                        help="Arduino serial port")
    args = parser.parse_args()

    dispatcher.Dispatcher()
    dispatcher.Dispatcher().map("/debug", print)
    dispatcher.Dispatcher().map("/muse/notch_filtered_eeg", eeg_handler, "EEG")
    dispatcher.Dispatcher().map("/muse/elements/jaw_clench", jawClench, "EEG")
    #########################################################################   dispatcher.map("/muse/elements/blink", blink, "EEG")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
    #p1 = Process(target=Drone)
    #p2 = Process(target=Muse)
    #p3 = Process(target=Test)

#    p1.start()
#    p2.start()
#    p3.start()
#    p1.join()
#    p2.join()
#    p3.join()