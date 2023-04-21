import pygame
import os, sys
from fcntl import ioctl
from tiles import *
from spritesheet import Spritesheet
from player import Player

def fixTo6(str1):
    if(len(str1) == 5):
        str1 = str1[:2] + "0" + str1[2:]
    if(len(str1) == 4):
        str1 = str1[:2] + "00" + str1[2:]
    if(len(str1) == 3):
        str1 = str1[:2] + "000" + str1[2:]    
    return str1

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
pygame.init()
DISPLAY_W, DISPLAY_H = 640, 480
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 20)
TARGET_FPS = 60

if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

fd = os.open(sys.argv[1], os.O_RDWR)

ioctl(fd, RD_PBUTTONS)

################################# START MUSIC #################################
#if pygame.mixer:
#        pygame.mixer.music.load('sound.mp3')
#        pygame.mixer.music.play(-1)

################################# LOAD PLAYER AND SPRITESHEET###################################
spritesheet = Spritesheet('spritesheet.png')
player = Player()
flagWin = 0
#################################### LOAD THE LEVEL #######################################
map = TileMap('mapacsv.csv', spritesheet)
player.position.x, player.position.y = map.start_x, map.start_y

################################# GAME LOOP ##########################
while running:
    dt = clock.tick(60) * .001 * TARGET_FPS
    ################################# CHECK PLAYER INPUT #################################

    red = os.read(fd, 4);
    val = fixTo6(bin(red[0]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
    if(val[2] == '0'):
        player.UP_KEY = True
    if(val[3] == '0'):
        player.DOWN_KEY = True
    if(val[4] == '0'):
        player.facing = 1
        player.LEFT_KEY = True
    if(val[5] == '0'):
        player.facing = -1
        player.RIGHT_KEY = True    
        #if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_LEFT:
        #        player.facing = 1
        #        player.LEFT_KEY = True
        #    elif event.key == pygame.K_RIGHT:
        #        player.facing = -1
        #        player.RIGHT_KEY = True
        #    elif event.key == pygame.K_UP:
        #        player.UP_KEY = True
        #    elif event.key == pygame.K_DOWN:
        #        player.DOWN_KEY = True


    if(val[2] == '1'):
        player.UP_KEY = False
    if(val[3] == '1'):
        player.DOWN_KEY = False
    if(val[4] == '1'):
        player.LEFT_KEY = False
    if(val[5] == '1'):
        player.RIGHT_KEY = False
        #if event.type == pygame.KEYUP:
        #    if event.key == pygame.K_LEFT:
        #        player.LEFT_KEY = False
        #    elif event.key == pygame.K_RIGHT:
        #        player.RIGHT_KEY = False
        #    elif event.key == pygame.K_UP:
        #        player.UP_KEY = False
        #    elif event.key == pygame.K_DOWN:
        #        player.DOWN_KEY = False


    ################################# UPDATE/ Animate SPRITE #################################
    player.update(dt, map.tiles, player.facing)
    ################################# UPDATE WINDOW AND DISPLAY #################################
    canvas.fill((64,73,115)) # Fills the entire screen with light blue
    map.draw_map(canvas)
    player.draw(canvas)
    window.blit(canvas, (0,0))
    pygame.display.update()