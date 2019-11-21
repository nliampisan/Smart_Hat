#Import the library
from wifi import Cell, Scheme
import os
from time import sleep 

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
    

while(True): 
    cells = scanForCells()
    for cell in cells:
        print(cell.summary)
        speak(cell.summary)
    #sleep(5)
    break


