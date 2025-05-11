
# "debugis*" - "if debug mode is enables"

from typing import *
import pygame
import sys, os
import yaml

pygame.init()

global_ids = {}

preferencesPath = '%LOCALADDDATA%\\StriDuhGrill' if os.name == 'nt' else os.path.expanduser('~/.striduhgrill')
preferencesFilePath = f'{preferencesPath}{'\\' if os.name == 'nt' else '/'}preferences.yaml'

def recreate_prefs():

    os.system(f'mkdir {preferencesPath}')
    with open(preferencesFilePath, 'w') as prefs:

        prefs.write(
"""

# StripDaGirl Preferences File

GuiScale: 2
bgColor: '#3F2F2F' # (!) 6 symbols with # in start
debugMode: false

cloth-list:
  - sk
  - sh
  - tsh
  - tr
  - bra
  - pre_bra
  - pre_tr

# All: sk, sh, tsh, tr, bra, pre_bra, pre_tr

# Example:
# - sk
# - sh
# - tr
# - bra
"""
        )
        prefs.close()

try:
    preferences = yaml.safe_load(open(preferencesFilePath))
except FileNotFoundError:
    recreate_prefs()
    preferences = yaml.safe_load(open(preferencesFilePath))

GUIScale = preferences['GuiScale'] 

ScaleX = lambda x: x * GUIScale # Function to scale by GUIScale

ticks = 8

screen_width = ScaleX(240)
screen_height = ScaleX(360)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Strip The Grill')

clock = pygame.time.Clock() # Ticks

key_list = pygame.key.get_pressed # Function to track if any keys are pressed

all_on = preferences['cloth-list'] # List of clothes
on = [True] * len(all_on)

debug_mode = preferences['debugMode'] # If debug/developer mode is enabled

add = lambda obj, x, y: screen.blit(obj, (x, y)) # Add object on screen

image_load = lambda path: \
                            pygame.transform.scale(
                                        x := pygame.image.load(path), 
                                        (ScaleX(x.get_width() * 0.8), 
                                         ScaleX(x.get_height() * 0.8))
                            ) # Load an image

def updateX(addon):

    global on

    for key in addon:
        try:
            on[key] = not on[key]
        except IndexError:
            if debug_mode: print('Outta range error')

xg, yg = (ScaleX(-20), ScaleX(25)) # X and Y of girl
places = {
    'pre_tr': (xg + ScaleX(70),  yg + ScaleX(228)),
    'pre_bra': (xg + ScaleX(92),  yg + ScaleX(102)),
    'bra': (xg + ScaleX(92),  yg + ScaleX(102)),
    'tr': (xg + ScaleX(55),  yg + ScaleX(225)),
    'tsh': (xg + ScaleX(65),  yg + ScaleX(102)),
    'sh': (xg + ScaleX(60),  yg + ScaleX(94)),
    'sk': (xg + ScaleX(40),  yg + ScaleX(240)),
    'gl': (xg + ScaleX(133), yg + ScaleX(58)),
} # Places of clothes

def draw_girl():

    global global_ids

    girl = image_load('textures/grill.png')
    for item in os.listdir('textures/cloth'):
        global_ids.update({item[:-4]: image_load(f'textures/cloth/{item}')})

    add(girl, xg, yg) # Add girl on screen

    for place in list(places.keys()):
        if place in all_on and on[all_on.index(place)]: 
            add(global_ids[place], *places[place]) # Add clothes step-by-step if they are

while True:

    for event in pygame.event.get():
        keys = key_list()
        if keys[pygame.K_ESCAPE]: # Exit the game by pressing ESC
            pygame.quit()
            sys.exit()

    n = [i - 30 for i, t in enumerate(key_list()) if t] # Check for pressed keys
    if n and debug_mode: print(n) # Print 'em debugis*
    updateX(n) # Update clothes

    screen.fill(int(preferences['bgColor'][1:], 16)) # Fill the background
    if debug_mode: print(on) # Print clothes on the girl debugis*
    draw_girl() # Redraw girl

    pygame.display.flip() # Update screen
    clock.tick(ticks) # Sleep 1/ticks seconds