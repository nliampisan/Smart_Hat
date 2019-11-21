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
        cell.summary = 'SSID {}'.format(cell.ssid)

    return cells

def speak(txt):
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

def wifi_func():
    t = threading.currentThread()
    while getattr(t, "do_run", True):    
        cells = scanForCells()
        threadLock.acquire()
        for cell in cells:
            print(cell.summary)
            speak(cell.summary)
        threadLock.release()
    
        time.sleep(30)
    print("stopping wifi") 
    
def dist_func():
    t2 = threading.currentThread()
    while getattr(t2, "do_run", True):    
        dist = distance()
        if dist < 5:
            threadLock.acquire()
            print("dist:", dist)
            time.sleep(1)
            threadLock.release()
    print("stopping distance sensor")

if __name__ == '__main__':
    threadLock = threading.Lock()
    try:
        t = threading.Thread(target = dist_func)
        t.start()
        t2 = threading.Thread(target = wifi_func) 
        t2.start()
          
    except KeyboardInterrupt:
        print("stopping")
        t.do_run = False
        t2.do_run = False
        t.join()
        t2.join()
        
        print("All threads stopped") 
        GPIO.cleanup()

        
        
    
    
    