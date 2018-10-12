# -*- coding: utf-8 -*-
"""
Spyder Editor

Abdulnaser

This code takes values every 3.9 seconds and stores them in four arrays corresponding to the four channels
The functions below process the data using the any() function which is a boolean function turns True once it
recongnizes particual events (i.e the uV over 900 ...)
"""



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


# Array to store OSC data for further processing
TempCH1 = [] 
TempCH2 = []
TempCH3 = []
TempCH4 = []
counter232 = 0
# Below is a counter function to count the function (eeg_handler) call times

"""class Counter():
    def __init__(self):
        self.counter = 0
    def add(self):
        self.counter = self.counter + 1
        print(self.counter)"""
def counter(x):
    counter.calls += 1
    return x + 1    
thing = Counter()
def Blink():
    """  
   -The variables UpwardSpikeCHn, WithinRangeCHn are boolean variables turning true
    when the the function any() turns to True
    
   -The function any() evaluates the OSC data stored in arrays corresponding to the channel number (1,2,3,4)
   
   -The variables a,b,c,d,e are temporary variables (within the scope of each individual functions)
   
   -The UpwardSpikeCH1 line for example uses the any() function to register the event when CH1 value
   exceeds 890 uV, it searches for that value within the current address of the array's element at which
   the function was called and scrolls back for the FIVE past elements to check if ANY exceeds 890 uV
   """
    
    UpwardSpikeCH1 = any(a > 890 for a in TempCH1[(len(TempCH1)-5):(len(TempCH1)-1)])
    """ this function is reading """
    UpwardSpikeCH4 = any(b > 890 for b in TempCH4[(len(TempCH4)-5):(len(TempCH4)-1)])
    
    if ( UpwardSpikeCH1 ==True and UpwardSpikeCH4 == True ) :
        
     #if Both The spikes above were activated, then move to next processing
     #the second phase of processing does the same method above but through the past 30 values
     #There is a new element in the array every 3.9 ms.
        DownwardSpikeCH1 = any(c < 730 for c in TempCH1[(len(TempCH1)-30):(len(TempCH1)-3)])
    
        DownwardSpikeCH4 = any(d < 730 for d in TempCH4[(len(TempCH4)-30):(len(TempCH4)-3)])
        
      #  WithinRangeCH3 = any((770 > e or e > 880) for e in TempCH3[(len(TempCH3)-30):(len(TempCH3)-3)])
      #  and WithinRangeCH3 == False        
        if ( DownwardSpikeCH1 == True and DownwardSpikeCH4 == True) :
                    print("_____")
                    print("Blink") 
                    print("_____")
                    thing.add()
                    return
def LookUp():
    
    FirstDownwardSpikeCH1 = any(a < 750 for a in TempCH1[(len(TempCH1)-5):(len(TempCH1)-1)])
    
    UpwardSpikeCH2 = any(b > 900 for b in TempCH2[(len(TempCH2)-10):(len(TempCH2)-1)])
    WithinRangeCH2 = any(c < 730 for c in TempCH2[(len(TempCH2)-20):(len(TempCH2)-1)])
    
    FirstDownwardSpikeCH4 = any(d < 750 for d in TempCH4[(len(TempCH4)-5):(len(TempCH4)-1)])
    
    if ( FirstDownwardSpikeCH1 ==True and UpwardSpikeCH2 == True and FirstDownwardSpikeCH4 == True and WithinRangeCH2 == False ) :
        
        DownwardSpikeCH1 = any(e < 780 for e in TempCH1[(len(TempCH1)-30):(len(TempCH1)-3)])
    
        DownwardSpikeCH4 = any(f < 780 for f in TempCH4[(len(TempCH4)-30):(len(TempCH4)-3)])
        
        WithinRangeCH3 = any((770 > g or g > 880) for g in TempCH3[(len(TempCH3)-30):(len(TempCH3)-3)])
        
        #WithinRangeCH3: We want to see some fluctuation so we need at least one value out of the range
                
        if ( DownwardSpikeCH1 == True and DownwardSpikeCH4 == True and WithinRangeCH3 == True) :
                    print("_____")
                    print("Look Up") 
                    print("_____")
                    return
    
def LookRight():
    
    DownwardSpikeCH3 = any(a < 810 for a in TempCH3[(len(TempCH3)-5):(len(TempCH3)-1)])
    
    DownwardSpikeCH4 = any(b < 810 for b in TempCH4[(len(TempCH4)-5):(len(TempCH4)-1)])
    
    WithinRangeCH1 = any((780 > c or c > 880) for c in TempCH1[(len(TempCH1)-30):(len(TempCH1)-3)])
    
    if ( DownwardSpikeCH3 ==True and DownwardSpikeCH4 == True and WithinRangeCH1 == False ) :
        
        UpwardSpikeCH3 = any(d > 870 for d in TempCH3[(len(TempCH3)-30):(len(TempCH3)-3)])
    
        DownwardSpikeCH2 = any((e < 830 and e > 740 )for e in TempCH2[(len(TempCH2)-30):(len(TempCH2)-3)])   
                
        if ( UpwardSpikeCH3 == True and DownwardSpikeCH2 == True ) :
                    print("_____")
                    print("look Right") 
                    print("_____")
                    return
                
def LookLeft():
    
    UpwardSpikeCH3 = any(a > 880 for a in TempCH3[(len(TempCH3)-5):(len(TempCH3)-1)])
    
    DownwardSpikeCH2 = any(b < 830 for b in TempCH2[(len(TempCH2)-5):(len(TempCH2)-1)])
    
    WithinRangeCH1 = any((740 > c or c > 920) for c in TempCH1[(len(TempCH1)-30):(len(TempCH1)-3)])
    
    if ( DownwardSpikeCH2 == True and UpwardSpikeCH3 == True and WithinRangeCH1 == False ) :
        
        UpwardSpikeCH2 = any(d > 870 for d in TempCH2[(len(TempCH2)-30):(len(TempCH2)-3)])
    
        DownwardSpikeCH3 = any(e < 820 for e in TempCH3[(len(TempCH3)-30):(len(TempCH3)-3)])
        
        DownwardSpikeCH4 = any(f < 830 for f in TempCH4[(len(TempCH4)-30):(len(TempCH3)-3)])
                
        if ( DownwardSpikeCH3 == True and UpwardSpikeCH2 == True and DownwardSpikeCH4 == True ) :
                    print("_____")
                    print("look Left") 
                    print("_____")
                    return
                        
    
#the eeg_handler function imports the OSC values with a frequence of
    #256 readings per 1 second (256/1sec = every 3.90625 milliseconds) 

def eeg_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    counter.calls +=1 #calling the counter function
  
    if counter.calls > 10:
        #print("EEG (uV) per channel: ", ch1, ch2, ch3, ch4)
        #print("counter works!!", counter.calls)
        TempCH1.append(ch1)
        TempCH2.append(ch2)
        TempCH3.append(ch3)
        TempCH4.append(ch4)
        
        
        Blink()
        LookRight()
        LookLeft()
        LookUp()
      
                    
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
                        default=5001, #make sure you change the port every time you wanna run the code
                        # for example next one would be 5052 :)
                        
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

#Below is a code takes values from a port every 3.9ms
#for which every value is used with its predecessor to calculate the slope
#then using if statements it determines whether it"S and inclining, declining,
#or horizontal slope    
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
    