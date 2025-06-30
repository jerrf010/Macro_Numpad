Instructions for installing to pico:

1. Drag and drop the pico firmware onto the raspberry pi pico's storage. The storage will become visable when you have a supported microusb cable that can transmit data and power. Hold down the bootload button and plug in the pico.
This will install a verison of circuitpython onto the pico.

2. The pico's storage device should become visable again once it is done copying. Move the files from /lib and copy them into the lib folder on the pico. Copy the contents from numpad firmware.py onto the code.py.

3. After making changes, change the 3nd line of code to be NOT COMMENTED

**After Uncommenting:**

YOU WILL NOT BE ABLE TO CHANGE THE CODE UNLESS YOU ERASE THE ENTIRE PICO AND INSTALLING CIRCUIT PYTHON AGAIN (pico firmware.uf2). 
THIS IS NESSESARRY IN ORDER TO SAVE THE EFFECT STATE WHEN THE POWER IS OFF
