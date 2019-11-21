print("ultrasonic sensor and wifi detection")
#Import the library
from wifi import Cell, Scheme
import os
from time import sleep
import RPi.GPIO as GPIO 
import time
from threading import Thread
import threading

GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

sem = threading.Semaphore()

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
#    while True:
#        cells = scanForCells()
#    
#        sem.acquire()
#        for cell in cells:
#            print(cell.summary)
#            speak(cell.summary)
#            sem.release()
    print("Hello world") 

def dist_func():
#    while True:
#        dist = distance()
#        if dist < 5:
#            sem.acquire()
#            print("dist:", dist)
#            time.sleep(1)
#            sem.release()

    t1 = threading.Timer(2.0, dist_func)
    t1.start()
    print("T2") 

def print_it():
    t2 = threading.Timer(5.0, print_it)
    t2.start()
    print("Hello, World!")

if __name__ == '__main__':
    try:
#        t = threading.Thread(target = dist_func)
#        t.start()
        dist_func()
        print_it()
        #t2.start()
          
    except KeyboardInterrupt:
        print("stopped")
        t.join()
        t2.join()
        print("All threads stopped") 
        GPIO.cleanup()

        
        
    
    
    