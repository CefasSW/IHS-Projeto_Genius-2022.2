import serial

ser = serial.Serial("/dev/ttyUSB0")
while(True):
	res = ser.readline()
	#value = float.from_bytes(res, 'little')
	value = float(res.decode())
	print(value)
	print()
