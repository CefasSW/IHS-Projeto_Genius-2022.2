from pygame.locals import *

PATH = '/dev/mydev'

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

N_ROUNDS = 2

INITIAL_SCREEN, CHOOSE_LEVEL, GAME_ON, GAME_OVER, WINNER = [i for i in range(0,5)]

BRIGHT_GREEN = (0, 255, 0)
BRIGHT_RED = (255, 0, 0)
BRIGHT_BLUE = (0, 0, 255)
BRIGHT_YELLOW = (255, 255, 0)
GREEN = (0, 100, 0)
RED = (139, 0, 0)
BLUE = (18, 10, 143)
YELLOW = (180, 140, 0)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

begin = (RED, GREEN, YELLOW, BLUE)
red_on = (BRIGHT_RED, GREEN, YELLOW, BLUE)
green_on = (RED, BRIGHT_GREEN, YELLOW, BLUE)
yellow_on = (RED, GREEN, BRIGHT_YELLOW, BLUE)
blue_on = (RED, GREEN, YELLOW, BRIGHT_BLUE)
all_on = (BRIGHT_RED, BRIGHT_GREEN, BRIGHT_YELLOW, BRIGHT_BLUE)

key_colors = {
    K_w : red_on,
    K_e : green_on,
    K_d : yellow_on,
    K_s : blue_on 
}

levels = {
    K_1 : 0.4,
    K_2 : 0.3,
    K_3 : 0.2,
  
    "0b100" : 0.4,
    "0b10" : 0.3,
    "0b1" : 0.2
}


cad_display = {
    0 : 0b01000000,
    1 : 0b01111001, 
    2 : 0b00100100,
    3 : 0b00110000,
    4 : 0b00011001,
    5 : 0b00010010,
    6 : 0b00000010,
    7 : 0b01111000,
    8 : 0b00000000,
    9 : 0b00010000,
    "OFF" : 0b11111111
}

BUTTONS = {
    "0b1011" : "START",
    "0b1101" : "RESTART",
    "0b1110" : "QUIT"
}

def seven_segment_encoder(num):
    display = 0
    num_digits = 0

    while True:
        digit = num%10
        display |= (cad_display[digit] << 8*num_digits)
        num_digits += 1
        num = num//10
        
        if num == 0:
            break

    for i in range (num_digits, num_digits + (4-num_digits)):
        display |= (cad_display["OFF"] << 8*i)

    return display
