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
from evdev import InputDevice, categorize, ecodes
gamepad = InputDevice('/dev/input/event4')


GPIO.setmode(GPIO.BCM)

GPIO_TRIGGER = 18
GPIO_ECHO = 24

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

import smtplib

def panic_button_func():
    print("sending emergency alert") 
    conn = smtplib.SMTP('imap.gmail.com',587)
    conn.ehlo()
    conn.starttls()
    conn.login('studymonmon@gmail.com', 'mon@4325')
    conn.sendmail('studymonmon@gmail.com','homecom1@gmail.com','Subject: Emergency Alert \n\n Reply Reply Reply')
    conn.quit()


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

def wifi_func():
    print("wifi") 
    cells = scanForCells()
    for cell in cells:
        q.put((1, cell.summary))
        
def dist_func():
    while True:
        dist = distance()
        if dist < 5:
            q.put((0,"danger"))
        time.sleep(1)
        global stop_threads 
        if stop_threads: 
            break
    print("stopping distance sensor")
    
def speak_func():
    while True:
        try:
            out = q.get_nowait()
            txt = out[1]
            speak(txt)
        except: 
            global stop_threads 
            if stop_threads: 
                break
    print("stopping speak function")

    
def LED_blink():
    os.system("sudo ./Lab6")


if __name__ == '__main__':
    #threadLock = threading.Lock()
    #lock not needed due to the fact that
    #put and get of queue has blocking behavior
    stop_threads = False
    q = Queue.PriorityQueue()
    
    t = threading.Thread(target = dist_func)
    t2 = threading.Thread(target = wifi_func)
    t3 = threading.Thread(target = speak_func)
    t4 = threading.Thread(target = LED_blink)
    t5 = threading.Thread(target = panic_button_func)

    t.start()
    t3.start()
    
    
    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY:
            keyevent = categorize(event)
            if keyevent.keystate == keyevent.key_down: 
                if keyevent.keycode == 'BTN_THUMB':
                    print("Green")
                    stop_threads = True
                    print('threads killed')
                    t.join()
                    if t2.isAlive(): 
                        t2.join()
                    t3.join()
                    if t4.isAlive(): 
                        t4.join()
                    if t5.isAlive():
                        t5.join()
                    GPIO.cleanup()
                    exit(0) 
                    
                elif keyevent.keycode[0] == 'BTN_JOYSTICK':
                    print("Blue")
                    t2.start()
                    t2.join()
                    

                elif keyevent.keycode == 'BTN_THUMB2':
                    print("Red")
                    t5.start()
                    t5.join()
                    print("send complete") 
                    
                    
                elif keyevent.keycode == 'BTN_TOP':
                    print("Yellow")
                    t4.start()
                    t4.join()
    
    
    
    

        
        
    
    
    