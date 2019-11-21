#Import the library
from wifi import Cell, Scheme

# Define a function which adds a summary attribute (this isn't necessary but was handy for my purposes)
def scanForCells():
    # Scan using wlan0
    cells = Cell.all('wlan0')

    # Loop over the available cells
    for cell in cells:
        cell.summary = 'SSID {} / Quality {}'.format(cell.ssid, cell.quality)

        if cell.encrypted:
            enc_yes_no = '*'
        else:
            enc_yes_no = '()'

        cell.summary = cell.summary + ' / Encryption {}'.format(enc_yes_no)

    return cells


cells = scanForCells()
for cell in cells:
    print(cell.summary)

