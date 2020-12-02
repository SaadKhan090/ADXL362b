############################################################
### Library for Communicating with ADXL362 Accelerometer ###
### for Raspberry Pi using spidev                        ###
###                                                      ###
### Authors: Sam Zeckendorf                              ###
###          Nathan Tarrh                                ###
###    Date: 3/29/2014                                   ###
############################################################

# spidev is the Raspberry Pi spi communication library
import spidev
import time

class ADXL362:

    def __init__(self, device=0, ce_pin=0):
        """
        device: the SPI device (often 0)

        ce_pin: pass 0 for CE0, 1 for CE1, etc.

        device and ce_pin map to device file /dev/spidev{device}.{ce_pin}
        """

        # init spi for communication
        self.spi = spidev.SpiDev()
        self.spi.open(device, ce_pin) # (x,0) == CE0, (x,1) == CE1

        # Set clock phase and polarity to default
        self.spi.mode = 0b00 
        self.spi.max_speed_hz = 1000000 
        self.spi.cshigh = False

        time.sleep(.5)
      
        self.spi_write_reg(0x1F, 0x52)
        time.sleep(.01)

        print('Soft reset')
    
    def spi_write_reg(self, address, value):
        ''' Write value to address
            Arguments:
                - address: Hexidecimal value of register address
                -   value: Desired hexidecimal byte to write
        '''
        # Send instruction (write), address, and value
        self.spi.xfer2([0x0A, address, value])
        
    def spi_read_reg(self, address):
        ''' Read contents of register at specified address
            Arguments:
                - address: Hexidecimal value of register address
            Returns:
                - value at address
        '''

        # Send instruction (write)
        response = self.spi.xfer2([0x0B, address, 0x00])
        return response[-1]

    def begin_measure(self):
        ''' Turn on measurement mode, required after reset
        '''
        
        # Read in current value in power control register
        pc_reg = self.spi_read_reg(0x2D)
        
        # Mask measurement mode onto power control buffer
        pc_reg_new = pc_reg | 0x02

        # Write new power control buffer to register
        self.spi_write_reg(0x2D, pc_reg_new)

        time.sleep(.01)

    def read_x(self):
        ''' Read the x value
            Returns:
                - Value of ug in x direction
        '''
        x = self.spi_read_two(0x0E)
        return x

    def read_y(self):
        ''' Read the y value
            Returns:
                - Value of ug in the y direction
        '''
        y = self.spi_read_two(0x10)
        return y

    def read_z(self):
        ''' Read the z value
            Returns:
                - Value of ug in the z direction
        '''
        z = self.spi_read_two(0x12)
        return z

    def read_temp(self):
        ''' Read the temperature value (for calibration/correlation)
            Returns:
                - Internal device temperature
        '''
        temp = self.spi_read_two(0x14)
        return temp

    def read_xyz(self):
        ''' Read x, y, and z data in burst mode. A burst read is required to
            guarantee all measurements correspond to the same sample time.
            Returns:
                - Tuple with x, y, z, and temperature data
        '''
        x = self.read_x()
        y = self.read_y()
        z = self.read_z()
        temp = self.read_temp()

        return (x, y, z, temp)
        
    def read_all(self):

	x,y,z =self.spi_read_two(0x0E)

	return (x,y,z)
 
    def spi_read_two(self, address):
        ''' Read two sequential registers
            Arguments: 
                - address: Hexidecimal address of first register to read from
            Returns: 
                - Value contained within said two registers
        '''
       
        # Send read instruction
        value = self.spi.xfer2([0x0B, address, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
      
        # Isolate low and high bytes from response
        val_lx = value[2]
        val_hx = (value[3] & 0xF) << 8
	val_ly = value[4]
	val_hy = (value[5] & 0xF) << 8
	val_lz = value[6]
	val_hz = (value[7] & 0xF) << 8 
        
        # Append low byte and high byte together
        valuex = (val_lx + val_hx)
	valuey = (val_ly + val_hy)
	valuez = (val_lz + val_hz) 
      
        return self.twos_comp(valuex,12),self.twos_comp(valuey,12),self.twos_comp(valuez,12)
 
    def spi_write_two(self, address, value):
        ''' Write to two sequential registers
            Arguments: 
                - address: Hexidecimal address of first register to write from
                -   value: Value to be written
        '''
        # Split value into high and low bytes for writing
        high_byte = value >> 8
        low_byte = value & 0xFF
       
        # Send write instruction
        self.spi.xfer2([0x0A, address, low_byte, high_byte])
       
        return value
    
    def check_all_regs(self):
        instructions = [0x0B, 0x20]
        registers = [0x00] * 15
        instructions.extend(registers)
        values = self.spi.xfer2(instructions)
        
        return values[2:]

    def twos_comp(self,val, bits):
        """ Returns two's complement of value given a number of bits
        """
        if val&(1<<(bits-1)) != 0:
            val = val - (1<<bits)
        return val

