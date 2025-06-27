import os
import sys

WALKING_SPEED = 0.1
TELEPORT_COOLDOWN = 2
TILESIZE = 40
CURRENT_MAP = "intro" # default value, gets overwritten in startscherm.py

def setMap(newMap):
    CURRENT_MAP = newMap

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    result = os.path.join(base_path, relative_path)
    print(result)
    return result