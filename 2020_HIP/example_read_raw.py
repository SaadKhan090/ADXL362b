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

accel = ADXL362.ADXL362()
accel.begin_measure()

while True:
    print accel.read_all()
    
    time.sleep(.1)
    print accel.spi_read_reg(0)
    time.sleep(.1)
