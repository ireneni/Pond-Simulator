from pygame import *
from simulationFunctions import *
from AlexIreneTim import *
import random
import math
#init()

running = True
menu = True
dayFrames = ["day1.png", "day2.png"]
nightFrames = ["night1.png", "night2.png"]
frames = dayFrames
flowers = image.load("reeds.png")
rock = image.load("rock.png")
timePaused = 0
paused = False
myClock = time.Clock()
