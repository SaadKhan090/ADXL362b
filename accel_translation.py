############################################################
### Example for Communicating with ADXL362 Accelerometer ###
### for Raspberry Pi using ADXL362.py                    ###
###                                                      ###
### Authors: Sam Zeckendorf                              ###
###          Nathan Tarrh                                ###
###    Date: 3/29/2014                                   ###
############################################################

import ADXL362  
import time
time.sleep(7)
import keyboard

accel = ADXL362.ADXL362()
accel.begin_measure()

a,b,c = accel.read_all()
a_in = a
b_in = b
c_in = c

while True:

    time.sleep(.05)
    a,b,c = accel.read_all()
    a_fin = a
    b_fin = b
    c_fin = c

    a_delta = a_fin-a_in
    b_delta = b_fin-b_in
    c_delta = c_fin-c_in


    if (abs(a_fin)>800):
	 keyboard.release('down arrow')
         keyboard.press('up arrow')
	 print("up")
    if (abs(b_fin)>800):
	 keyboard.release('up arrow')
         keyboard.press('down arrow')
	 print("down")
    else:
	 keyboard.release('up arrow')
	 keyboard.release('down arrow')
