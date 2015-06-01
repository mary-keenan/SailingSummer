#!/usr/bin/python
import smbus
import time
import math

bus = smbus.SMBus(1)
address = 0x1e

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
write_byte(2, 0b00000000) # Continuous sampling

scale = 0.92

x_offset = -89
y_offset = -179

def find_bearing():
    #while True:
    x_out = (read_word_2c(3) - x_offset) * scale
    y_out = (read_word_2c(7) - y_offset) * scale
    z_out = read_word_2c(5) * scale

    bearing  = math.atan2(y_out, x_out)
        
    if (bearing < 0):
        bearing += 2 * math.pi
    #print math.degrees(bearing)
    #time.sleep(1) 
    res = int(round(math.degrees(bearing)))
    return ("Bearing: " + str(res), res)
    #with open('bearing.txt', 'w') as f:
        #f.write("Bearing: " + "%.2f" % math.degrees(bearing))
        #os.system('pico2wave -w /home/pi/Sailing_Team/Compass/bearing.wav "$(cat /home/pi/Sailing_Team/Compass/bearing.txt)"')
    #time.sleep(1)

#while True:
    #test = find_bearing()
    #print test[1]
    #time.sleep(0.5)
#print test[1]
#def text_to_speech():
    #while True:
	#os.system('pico2wave -w /home/pi/Sailing_Team/Compass/bearing.wav "$(cat /home/pi/Sailing_Team/Compass/bearing.txt)"')

#for i in range(0,500):
    #x_out = read_word_2c(3)
    #y_out = read_word_2c(7)
    #z_out = read_word_2c(5)
    
    #bearing = math.atan2(y_out, x_out)
    #if (bearing < 0):
	#bearing += 2 * math.pi
    #f.write("{} {} {} {}\n".format(x_out, y_out, (x_out * scale), (y_out * scale)))
    #time.sleep(0.1)
