import pygame
import random
import os, sys
from fcntl import ioctl
import serial

ser = serial.Serial("/dev/ttyUSB0")

debug = False

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934


last_r_disp_data = [0 for i in range (4)]

def file_desc():
  if len(sys.argv) < 2:
    print("Error: expected more command line arguments")
    print("Syntax: %s </dev/device_file>"%sys.argv[0])
    exit(1)

  fd = os.open(sys.argv[1], os.O_RDWR)
  return fd
  
fd = file_desc()

def read_button(fd):
  ioctl(fd, RD_PBUTTONS)
  value = os.read(fd, 4); # read 4 bytes and store in red var
  if(debug):
  	print("red 0x%X"%int.from_bytes(value, 'little'))
  value = int.from_bytes(value, 'little')
  return value
  

def first_b_pres(fd):
  value = 0
  while(value == 0):
    val_read = read_button(fd)
    if(val_read == 0xE):      
      value = 4
    elif(val_read == 0xD):
      value = 3
    elif(val_read == 0xB):
      value = 2
    elif(val_read == 0x7):
      value = 1
  
  return value

def read_switch(fd):
  ioctl(fd, RD_SWITCHES)
  value = os.read(fd, 4); # read 4 bytes and store in red var
  if(debug):
  	print("red 0x%X"%int.from_bytes(value, 'little'))
  value = int.from_bytes(value, 'little')
  return value
  

def check_swirch(fd):
  val = 0
  while (!val):
    val_read = read_switch(fd)
    if (val_read = 0x1):
      val = 1
  return

def set_green_leds(fd, data):
  ioctl(fd, WR_GREEN_LEDS)
  retval = os.write(fd, data.to_bytes(4, 'little'))

def set_red_leds(fd, data):
  ioctl(fd, WR_RED_LEDS)
  retval = os.write(fd, data.to_bytes(4, 'little'))

def to_seg(num):
  if(num == 0):
    return 0xC0
  elif(num == 1):
    return 0xF9
  elif(num == 2):
    return 0xA4
  elif(num == 3):
    return 0xB0
  elif(num == 4):
    return 0x99
  elif(num == 5):
    return 0x92
  elif(num == 6):
    return 0x82
  elif(num == 7):
    return 0xF8
  elif(num == 8):
    return 0x80
  elif(num == 9):
    return 0x90
  else:
    print("Error: invalid digit")
    return -1


def ret_dig(num, pos):
  return num // 10**pos % 10


def send_r_disp(fd, data):
  ioctl(fd, WR_R_DISPLAY)
  retval = os.write(fd, data.to_bytes(4, 'little'))
  print("wrote %d bytes"%retval)
  
  
def r_disp(num, fd):
  if(num > 9999 or num < 0 or str(num).isdigit() == 0):
    print("Error: this number cannot be displayed")
    return -1
  else:
    data = 0
    digit = [0 for i in range(4)] 
    for i in range (4):
      digit[i] = to_seg(ret_dig(num, i))
      print("0x%X" %digit[i])
      if(digit[i] != -1):
        data += digit[i] * 256**i

      last_r_disp_data[i] = digit[i]
    
    print("0x%X" %data)
    send_r_disp(fd, data)
    
    return 0


def r_disp_digit(num, pos, fd):
  if(num > 9999 or num < 0 or str(num).isdigit() == 0):
    print("Error: this number cannot be displayed")
    return -1
  else:
    data = 0
    digit = last_r_disp_data.copy()
    digit[pos] = to_seg(ret_dig(num, 0))
    for i in range (4):
      print("0x%X" %digit[i])
      if(digit[i] != -1):
        data += digit[i] * 256**i

    last_r_disp_data[pos] = digit[pos]
    
    print("0x%X" %data)
    send_r_disp(fd, data)
    return 0

def ret_pos():
    #pygame.time.wait(500)	
    res = ser.readline()
    
    value = float(res.decode())
    print(value, end="\n")
    if(value > 0 and value < 15):
        count = 1
    elif(value >= 15 and value < 30):
        count = 2
    elif(value >= 30 and value < 45):
        count = 3
    elif(value >= 45 and value < 60):
        count = 4
    else: 	
        count = 0
	
    return count
	


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

SHADOW_RED = (50, 0, 0)
SHADOW_GREEN = (0, 50, 0)
SHADOW_BLUE = (0, 0, 50)
SHADOW_YELLOW = (50, 50, 0)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.font.init()

pygame.display.set_caption("Genius Game")

# Define some constants for the game
FONT_SIZE = 32
NUM_BUTTONS = 4
BUTTON_SIZE = 100
BUTTON_MARGIN = 20
SEQUENCE_DELAY = 1000  # milliseconds
PRINT_DELAY = 100
FLASH_DELAY = 500  # milliseconds

# Define the font for displaying text
font = pygame.font.Font(None, FONT_SIZE)

# Define a class for the colored buttons
class Button:
    def __init__(self, color, shadow_color, pos):
        self.shadow_color = shadow_color
        self.color = color
        self.rect = pygame.Rect(pos, (BUTTON_SIZE, BUTTON_SIZE))
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
    
    def shadow_draw(self, surface):
        pygame.draw.rect(surface, self.shadow_color, self.rect)
    
    def flash(self, surface, delay):
        self.draw(surface)
        pygame.display.flip()
        pygame.time.wait(delay)
        pygame.draw.rect(surface, self.shadow_color, self.rect)
        pygame.display.flip()
        pygame.time.wait(delay)

# Set up the colored buttons
button_colors = [RED, GREEN, BLUE, YELLOW]
shadow_button_colors = [SHADOW_RED, SHADOW_GREEN, SHADOW_BLUE, SHADOW_YELLOW]
buttons = []
for i in range(NUM_BUTTONS):
    x = SCREEN_WIDTH/2 - (BUTTON_SIZE + BUTTON_MARGIN)*NUM_BUTTONS/2 + (BUTTON_SIZE + BUTTON_MARGIN)*i
    y = SCREEN_HEIGHT/2 - BUTTON_SIZE/2
    button = Button(button_colors[i], shadow_button_colors[i], (x, y))
    buttons.append(button)

# Set up the game loop
done = False
clock = pygame.time.Clock()
level = 1
sequence = []

set_red_leds(fd, 0x40405555)
set_green_leds(fd, 0x40404055)

while not done:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # Display the instructions
    screen.fill(BLACK)
    if(level == 1):
        text = font.render("Press any key to start", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        pygame.display.flip()
        # Wait for a key press to start the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
    text = font.render(f"level {level}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 + 30 - text.get_height()/2))
    pygame.display.flip()
    r_disp(level, fd)
    pygame.time.wait(1000)
    
    # Clear screen
    screen.fill(BLACK)
    pygame.display.flip()
    
    for button in buttons:
        button.shadow_draw(screen)
    
    pygame.display.flip()
    pygame.time.wait(1000)
    
    # Generate a random sequence of button presses
    if(level == 1):
        sequence = []
    sequence.append(random.randint(0, NUM_BUTTONS-1))
    
    # Display the sequence
    for button_index in sequence:
        buttons[button_index].flash(screen, FLASH_DELAY)
        pygame.time.wait(SEQUENCE_DELAY)
        
    
    # Print your turn
    text = font.render("your turn!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/5 - text.get_height()/2))
    pygame.display.flip()
    pygame.time.wait(100)
    
    # Get the player's input
    correct = True
    player_sequence = []
    for i in range(len(sequence)):
        # Clear any pending events before waiting for a key press
        pygame.event.clear()
        waiting = True
        value = 0
        while waiting and correct:
            #event = pygame.event.wait()
            #value = first_b_pres(fd)
            count = 0
            check_swirch(fd)
            value = ret_pos()
            while(count < 3 and ret_pos() == value):
                print(count)
                count += 1
            if(count < 3):
                value = 0   
            
            if True:
                if value == 1:
                    player_sequence.append(0)
                    buttons[0].flash(screen, FLASH_DELAY)
                    pygame.time.wait(PRINT_DELAY)
                    if player_sequence[i] != sequence[i]:
                        correct = False
                        break
                    waiting = False
                elif value == 2:
                    player_sequence.append(1)
                    buttons[1].flash(screen, FLASH_DELAY)
                    pygame.time.wait(PRINT_DELAY)
                    if player_sequence[i] != sequence[i]:
                        correct = False
                        break
                    waiting = False
                elif value == 3:
                    player_sequence.append(2)
                    buttons[2].flash(screen, FLASH_DELAY)
                    pygame.time.wait(PRINT_DELAY)
                    if player_sequence[i] != sequence[i]:
                        correct = False
                        break
                    waiting = False
                elif value == 4:
                    player_sequence.append(3)
                    buttons[3].flash(screen, FLASH_DELAY)
                    pygame.time.wait(PRINT_DELAY)
                    if player_sequence[i] != sequence[i]:
                        correct = False
                        break
                    waiting = False
                
    # Display the result
    screen.fill(BLACK)
    if correct:
        text = font.render("Congratulations, you win!", True, GREEN)
        level += 1
    else:
        text = font.render("Sorry, you lose!", True, RED)
        level = 1
        screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()

    screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))
    pygame.display.flip()
    pygame.time.wait(3000)
    #pygame.quit()
