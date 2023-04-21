#!/usr/bin/python3

import os, sys
from fcntl import ioctl

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

def fixTo6(str1):
    if(len(str1) == 5):
        str1 = str1[:2] + "0" + str1[2:]
    if(len(str1) == 4):
        str1 = str1[:2] + "00" + str1[2:]
    if(len(str1) == 3):
        str1 = str1[:2] + "000" + str1[2:]    
    return str1

def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    # data to write
    data = 0x08080808;
    ioctl(fd, WR_R_DISPLAY)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print("wrote %d bytes"%retval)

    # data to write
    data = 0x08080808;
    ioctl(fd, WR_L_DISPLAY)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print("wrote %d bytes"%retval)

    ioctl(fd, RD_PBUTTONS)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    print("red 0x%X"%int.from_bytes(red, 'little'))

    ioctl(fd, RD_SWITCHES)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    print("red 0x%X"%int.from_bytes(red, 'little'))

    data = 0x1FF
    ioctl(fd, WR_GREEN_LEDS)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print('wrote %d bytes'%retval)

    data = 0x100
    ioctl(fd, WR_RED_LEDS)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print('wrote %d bytes'%retval)

    os.close(fd)

if __name__ == '__main__':
    main()

