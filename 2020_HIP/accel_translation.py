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

while True:
    
    a,b,c =  accel.read_all()
    a_in = a
    b_in = b
    c_in = c

    time.sleep(.1)
    a,b,c = accel.read_all()
    a_fin = a
    b_fin = b
    c_fin = c

    a_delta = a_fin-a_in
    b_delta = b_fin-b_in
    c_delta = c_fin-c_in


    if (abs(b_delta)>15):
	if (b_delta >0):
	    keyboard.send('left arrow')
        else:
            keyboard.send('right arrow')

    if (abs(c_delta)>25):
        if (c_delta > 0):
            keyboard.send('up arrow')
        else:
            keyboard.send('down arrow')

    print accel.spi_read_reg(0)
    time.sleep(.3)
