# -*- coding: utf-8 -*-
"""
Created on Fri Nov 9 18:18:16 2018

@author: johnl
"""

import argparse
import math
import socket
import os
import pythonosc
import time
import threading
import sys
import selectors
import types

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder



# Array to store OSC data for further processing
TempCH1 = []
TempCH2 = []
TempCH3 = []
TempCH4 = []

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65440      # Port to listen on (non-privileged ports are > 1023)# ...
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize server
sock.setblocking(False) # initiate server
sock.connect_ex((host, port)) # connect to server

def counter(x):
    counter.calls += 1
    return x + 1


def LookLeft():
    UpwardSpikeCH3 = any(a > 880 for a in TempCH3[(len(TempCH3) - 5):(len(TempCH3) - 1)])

    DownwardSpikeCH2 = any(b < 830 for b in TempCH2[(len(TempCH2) - 5):(len(TempCH2) - 1)])

    WithinRangeCH1 = any((740 > c or c > 920) for c in TempCH1[(len(TempCH1) - 30):(len(TempCH1) - 3)])

    if DownwardSpikeCH2 == True and UpwardSpikeCH3 == True and WithinRangeCH1 == False:

        UpwardSpikeCH2 = any(d > 870 for d in TempCH2[(len(TempCH2) - 30):(len(TempCH2) - 3)])

        DownwardSpikeCH3 = any(e < 820 for e in TempCH3[(len(TempCH3) - 30):(len(TempCH3) - 3)])

        DownwardSpikeCH4 = any(f < 830 for f in TempCH4[(len(TempCH4) - 30):(len(TempCH3) - 3)])

        if DownwardSpikeCH3 and UpwardSpikeCH2 and DownwardSpikeCH4:
          
            # print("look_left")
            text = str("left").encode('ascii')
            sock.send(text)
            return True

    return False


def LookRight():
    DownwardSpikeCH3 = any(a < 810 for a in TempCH3[(len(TempCH3) - 5):(len(TempCH3) - 1)])

    DownwardSpikeCH4 = any(b < 810 for b in TempCH4[(len(TempCH4) - 5):(len(TempCH4) - 1)])

    WithinRangeCH1 = any((780 > c or c > 880) for c in TempCH1[(len(TempCH1) - 30):(len(TempCH1) - 3)])

    if DownwardSpikeCH3 and DownwardSpikeCH4 and WithinRangeCH1:

        UpwardSpikeCH3 = any(d > 870 for d in TempCH3[(len(TempCH3) - 30):(len(TempCH3) - 3)])

        DownwardSpikeCH2 = any((e < 830 and e > 740) for e in TempCH2[(len(TempCH2) - 30):(len(TempCH2) - 3)])

        if UpwardSpikeCH3 and DownwardSpikeCH2:

            # print("look Right")
            text = str("right").encode('ascii')
            sock.send(text)
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
    if ch6 > 0.2:

        # print("clench")
        text = str("clench").encode('ascii')
        sock.send(text)
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
    counter.calls = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=7000,  # make sure you change the port every time you wanna run the code
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
