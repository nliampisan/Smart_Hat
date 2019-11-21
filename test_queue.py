
import threading
import queue
import random
import time

def queuePrint(q):
    t3 = threading.currentThread()
    while getattr(t3, "do_run", True):
        print(q.get())


def wifi_func(q):
    
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        #print("wifi") 
        q.put((1,"wifi"))
    print("stopping wifi")

    
def dist_func(q):
    t2 = threading.currentThread()
    while getattr(t2, "do_run", True):
        #print("dist") 
        q.put((0,"dist"))
    print("stopping distance sensor")
      

if __name__ == '__main__':
    threadLock = threading.Lock()
    q = queue.PriorityQueue()

    try:
        q.put(1)
        print(q.get())
        t = threading.Thread(target = dist_func, args=(q,))
        t.start()
        t2 = threading.Thread(target = wifi_func,args=(q,)) 
        t2.start()
        t3 = threading.Thread(target = queuePrint, args=(q,))
        t3.start()
          
    except KeyboardInterrupt:
        print("stopping")
        t.do_run = False
        t2.do_run = False
        t3.do_run = False
        t.join()
        t2.join()
        t3.join()
        print("All threads stopped") 
        GPIO.cleanup()
    
    