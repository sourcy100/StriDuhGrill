
from typing import *
import pygame
import sys, os
import yaml

pygame.init()

os.system('cls' if os.name == 'nt' else 'clear')

global_ids = {}

preferences = yaml.safe_load(open('preferences.yaml'))

GUIScale = preferences['GuiScale']

ScaleX = lambda x: x * GUIScale

screen_width = ScaleX(240)
screen_height = ScaleX(360)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Strip The Grill')

clock = pygame.time.Clock()

key_list = pygame.key.get_pressed

all_on = preferences['cloth-list'] # TODO: none
on = [True] * len(all_on)

debug_mode = preferences['debugMode']

def add(obj: pygame.Surface, x: float, y: float):
    screen.blit(obj, (x, y))

def image_load(path):

    result = pygame.image.load(path)
    return pygame.transform.scale(result, (ScaleX(result.get_width() * 0.8), ScaleX(result.get_height() * 0.8)))


def updateX(addon):

    global on, all_on

    for key in addon:
        try:
            on[key] = not on[key]
        except IndexError:
            if debug_mode: print('Outta range error')

xg, yg = (ScaleX(-20), ScaleX(25))
places = {
    'pre_tr': (xg + ScaleX(70),  yg + ScaleX(228)),
    'pre_bra': (xg + ScaleX(92),  yg + ScaleX(102)),
    'bra': (xg + ScaleX(92),  yg + ScaleX(102)),
    'tr': (xg + ScaleX(55),  yg + ScaleX(225)),
    'tsh': (xg + ScaleX(65),  yg + ScaleX(102)),
    'sh': (xg + ScaleX(60),  yg + ScaleX(94)),
    'sk': (xg + ScaleX(40),  yg + ScaleX(240)),
    'gl': (xg + ScaleX(133), yg + ScaleX(58)),
}

def draw_girl():

    global global_ids

    girl = image_load('.\\textures\\grill.png')
    for item in os.listdir('.\\textures\\cloth'):
        global_ids.update({item[:-4]: image_load(f'textures\\cloth\\{item}')})

    add(girl, xg, yg)

    for place in list(places.keys()):
        if place in all_on and on[all_on.index(place)]: add(global_ids[place], *places[place])

while True:

    for event in pygame.event.get():
        keys = key_list()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

    n = [i - 30 for i, t in enumerate(key_list()) if t]
    if n and debug_mode: print(n)
    updateX(n)

    screen.fill(int(preferences['bgColor'][1:], 16))
    if debug_mode: print(on)
    draw_girl()

    pygame.display.flip()
    clock.tick(10)