# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#the aim of this code takes values from a port every 100ms, takes up to 6
#for which every value is used with its predecessor to calculate the slope
#then using if statements it determines whether it"S and inclining, declining,
#or horizontal slope
import argparse
import math
import socket
import os 
import pythonosc
import time

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client
from pythonosc import osc_message_builder


TempData = [] # An Array to store OSC data for further operations
TempDataCH3 = []
# Below is a counter function to count the function (eeg_handler) call times

def counter(x):
    counter.calls += 1
    return x + 1    

#the eeg_handler function imports the OSC values with a frequence of
    #256 readings per 1 second (256/1sec = every 3.90625 milliseconds) 

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    counter.calls +=1 #calling the counter function
  
    if counter.calls > 10:
        #print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)
        #print("counter works!!", counter.calls)
      
        TempDataCH3.append(ch3) #Basically every 10 times the function gets called 
        #the Array stores one reading from ch1 only (every 39 ms)
     
    #    if (TempData[len(TempData)-1] > 960): # if the current reading is < 960 uV then pass
            #through every reading of the 20 before it and test if it's < 780
            #if yes that means it's a DOWNWARD then an UPWARD spike and this is 
            #the wave form of a blink **same principle for lookdown and up below
            
     #       for i in range((len(TempData)-20),(len(TempData)-2)):
                
      #          if(TempData[i] < 780):
                    
       #             print("Blink")
                    
        if (TempDataCH3[len(TempDataCH3)-1] < 800):
            
            for i in range((len(TempDataCH3)-20),(len(TempDataCH3)-2)):
                
                if(TempDataCH3[i] > 875):
                    
                    print("look Right") 
                    
        if (TempDataCH3[len(TempDataCH3)-1] >870):
            
            for i in range((len(TempDataCH3)-20),(len(TempDataCH3)-2)):
                
                if(TempDataCH3[i] < 800):
                    
                    print("look Left") 
                    
       #if (TempDataCH3[len(TempDataCH3)-1] < 800):
            
        #    for i in range((len(TempDataCH3)-20),(len(TempDataCH3)-2)):
                
            # if(TempDataCH3[i] > 875):
                    
             #       print("look LEFT") """
                    
      #  if (TempData[len(TempData)-1] < 750):
            
       #     for i in range((len(TempData)-20),(len(TempData)-2)):
                
        #        if(TempData[i] > 960):
                    
         #           print("lookdown")
                    
       # if (TempData[len(TempData)-1] < 780):
            
        #    for i in range((len(TempData)-20),(len(TempData)-2)):
                
         #       if(TempData[i] < 780):
                    
          #          print("lookup")
                    
        counter.calls = 0 #resetting the counter so that it counts back to 10 every time
  
#Below is the function to receive the OSC live feed from the muse
if __name__ == "__main__":
    counter.calls = 0
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=5007,
                        help="The port to listen on")
    parser.add_argument("--serial",
                        default="",
                        help="Arduino serial port")
    args = parser.parse_args()
    
    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/debug", print)
    dispatcher.map("/muse/notch_filtered_eeg", eeg_handler, "EEG")
    
    server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
    
#trying to classify noise out through the derivate method, needs more work

"""while 820 > port_value <820:
    
    for i in range(0,6,1):
    
        temp.i = port_Value
    
        #calculating the slope
    
        try:
            slope.i = (temp.(i) - temp.(i-1))/100
        
        # finding the direction of the slope
        
            if(slope.i > 0):
                inclining_slope.i = 1
                else if(slope.i < 0):
                    declining_slope.i = 1
                    else if(slope.i = 0):
                        print("need to increase frequency because slope = 0")
            
        #finding maximas and minimas    
            
            if(inclining_slope.i=1 and declining_slope.(i-1) =1):
                maxima.i=1
                if(declining_slope.i=1 and inclining_slope.(i-1) =1):
                    minima.i=1
        #classifying actions (in this case a lookdown)
        
        if maxima then minima
            look down
            
            
    
    delay 100ms"""
    