print("ultrasonic sensor and wifi detection")
#Import the library
from wifi import Cell, Scheme
import os
from time import sleep
import RPi.GPIO as GPIO 
import time
from threading import Thread
import threading
import multiprocessing
import Queue
import random

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


# Define a function which adds a summary attribute (this isn't necessary but was handy for my purposes)
def scanForCells():
    # Scan using wlan0
    cells = Cell.all('wlan0')

    # Loop over the available cells
    for cell in cells:
        cell.summary = cell.ssid

    return cells

def speak(txt):
    print("speak get", txt)
    os.system("sudo espeak \""+txt+"\" --stdout |aplay")


def distance():
    GPIO.output(GPIO_TRIGGER,True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER,False)
    
    StartTime = time.time()
    StopTime = time.time()
    
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        
    TimeElapsed = StopTime - StartTime
    
    distance = (TimeElapsed * 34300)/2
    
    return distance

def wifi_func(event):
    while not event.is_set():
        cells = scanForCells()
        for cell in cells:
            q.put((1, cell.summary))
    
        time.sleep(30)
    print("stopping wifi") 
    
def dist_func(event):
    while not event.is_set():
        dist = distance()
        if dist < 5:
            q.put((0,"danger"))
        time.sleep(1)
    print("stopping distance sensor")
    
def speak_func(event):
    while not event.is_set():
        out = q.get()
        txt = out[1]
        speak(txt)
    

if __name__ == '__main__':
    #threadLock = threading.Lock()
    #lock not needed due to the fact that
    #put and get of queue has blocking behavior
    threadLock = threading.Lock()
    q = Queue.PriorityQueue()
    
    
    try:
        event = threading.Event()
        t = threading.Thread(target = dist_func, args=(event,))
        t.start()
        t2 = threading.Thread(target = wifi_func, args=(event,))
        t2.start()
        t3 = threading.Thread(target = speak_func, args=(event,))
        t3.start()
        event.wait(1) #wait forever without blocking KeyboardInterrupt exceptions
          
    except KeyboardInterrupt:
        print("stopping")
        event.set() #inform child thread that it should exit
        print("All threads stopped") 
        GPIO.cleanup()
        sys.exit(1)
        
    

        
        
    
    
    