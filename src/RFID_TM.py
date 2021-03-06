# RFID_TM.py
# Author: Noah J Epstein
# Created: 4/1/2016
# Modified: 9/30/2016
# Manages RFID I/O with USB-serial RFID reader via Raspberry Pi

import os
import serial
import glob

BAUD = 9600
TIMEOUT = 5
TAG_BYTESIZE = 12

PLATFORM = 'PI' # can change to 'OSX'

# constantly read from serial
def scanRFIDTag():


	if PLATFORM == 'PI':
		serialName = "/dev/ttyUSB*"
	else:
		serialName = "dev/cu.usbserial*"

	reader_name = glob.glob(serialName)[0]
	# os.system('fuser -k ' + reader_name )
	reader = serial.Serial(reader_name, BAUD)
	ID = reader.read(TAG_BYTESIZE)
	print ID
	reader.close()
	return ID
