from pygame import *
from math import *
from simulationFunctions import *
from main import *
import random
import sys
init()
mixer.init()

SIZE = (1000,700)
screen = display.set_mode(SIZE)

#Variables used in order to determine which function will be used inside the main game loop
menu = True
mainMenu = True
optionsPage = False
creditsPage = False
sound = False
mainSimBool = False
pauseMenuBool = False
startingScreen = False
saveConfigBool = False
dayMode = True

#Creats a timer to be used to creat the 60 fps
myClock = time.Clock()

#Creats a font which will be used later to display text
fontBauhaus = font.SysFont("Bauhaus 93", 30)
dayMode = fontBauhaus.render("AM", 1, (0,0,0))    
nightMode = fontBauhaus.render("PM", 1, (0,0,0))    

#These pictures are loaded in early in order to form the loading gif
loading1 = image.load("loading1.png")
loading2 = image.load("loading2.png")
loading3 = image.load("loading3.png")
loading4 = image.load("loading4.png")
loading5 = image.load("loading5.png")
warning = image.load("warning.png")

#creats a function called loading which puts together pictures that will form a gif
def loading():
    for evnt in event.get():
        if (evnt.type == QUIT):
            menu = False     
    screen.blit(loading1, (125, 50, 800, 600))
    time.wait(50)
    display.flip()
    screen.blit(loading2, (125, 50, 800, 600))
    time.wait(50)
    display.flip()
    screen.blit(loading3, (125, 50, 800, 600))
    time.wait(50)
    display.flip()
    screen.blit(loading4, (125, 50, 800, 600))
    time.wait(50)
    display.flip()
    screen.blit(loading5, (125, 50, 800, 600))
    time.wait(50)
    display.flip()    

#Calls in the gif function while other images load
loading()
#Loads in images which will be used for the Main Menu gif
menuPic1 = image.load("mainMenu (1).gif")
menuPic2 = image.load("mainMenu (2).gif")
menuPic3 = image.load("mainMenu (3).gif")
menuPic4 = image.load("mainMenu (4).gif")
menuPic5 = image.load("mainMenu (5).gif")
menuPic6 = image.load("mainMenu (6).gif")
menuPic7 = image.load("mainMenu (7).gif")
menuPic8 = image.load("mainMenu (8).gif")
menuPic9 = image.load("mainMenu (9).gif")
menuPic10 = image.load("mainMenu (10).gif")
menuPic11 = image.load("mainMenu (11).gif")
menuPic12 = image.load("mainMenu (12).gif")
menuPic13 = image.load("mainMenu (13).gif")
menuPic14 = image.load("mainMenu (14).gif")
#Puts all the pictures in a lists
menuBackgroundList = [menuPic1, menuPic2, menuPic3, menuPic4, menuPic5, menuPic6, menuPic7, menuPic8, menuPic9, menuPic10, menuPic11,
                      menuPic12, menuPic13, menuPic14]

#Loads in text graphics for the main menu page
seaLifeSimulation = image.load("seaLifeSimulation.png")
initiateSim = image.load("initiateSim.png")
initiateSimSelect = image.load("initiateSimSelect.png")
settings = image.load("settings.png")
settingsSelect = image.load("settingsSelect.png")
quit = image.load("quit.png")
#Calls in the gif function while other images load
loading()
#Loads in pictures needed for the settings page
coreBackground = image.load("settingsCoreGraphics.png")
dayNightWheel = image.load("dayNightWheel.png")
credits = image.load("credits.png")
creditsSelect = image.load("creditsSelect.png")
initSim = image.load("initSim.png")
initSimSelect = image.load("initSimSelect.png")
returnHome = image.load("returnHome.png")
returnHomeSelect = image.load("returnHomeSelect.png")
saveSettings = image.load("saveSettings.png")
saveSettingsSelect = image.load("saveSettingsSelect.png")
fishSlider = image.load("smallFishSlider.png")
predatorSlider = image.load("predatorSlider.png")
plantLifeSlider = image.load("plantLifeSlider.png")
saveDropDown = image.load("saveDropDown.png")
saveOneSelect = image.load("saveOneSelect.png")
saveTwoSelect = image.load("saveTwoSelect.png")
saveThreeSelect = image.load("saveThreeSelect.png")
creditsText = image.load("creditsText.png")
creditsGreyFilter = image.load("greyFilter.png")
mixer.music.load("antManThemeSong.mp3")

#Loads in the grphics needed for the play/pause screen
playPauseButton = image.load("playPauseButton.png")
playPauseButtonSelect = image.load("playPauseButtonSelect.png")
mainMenuRectSelect = image.load("mainMenuRectSelect.png")
saveConfigRectSelect = image.load("saveConfigRectSelect.png")
restartSimRectSelect = image.load("restartSimRectSelect.png")
resumeSimRectSelect = image.load("resumeSimRectSelect.png")
volumeOnSymbol = image.load("volumeOnSymbol.png")
volumeOffSymbol = image.load("volumeOffSymbol.png")
volumeRectSelect = image.load("volumeRectSelect.png")
pauseMenuSkeleton = image.load("pauseMenuSkeleton.png")

#Loads in pictures for the saving to screen
saveMenuSkeleton = image.load("saveMenuSkeleton.png")
returnButtonSelect = image.load("returnButtonSelect.png")
save1Select = image.load("save1Select.png")
save2Select = image.load("save2Select.png")
save3Select = image.load("save3Select.png")
savedSettings = image.load("savedSettings.png")

#Displaying the warning screen before starting the program
tempNum = 0
while tempNum < 100:
    for evnt in event.get():
        if (evnt.type == QUIT):
            menu = False  
    screen.blit(warning,(0, 0, 800, 600))
    display.flip()
    tempNum += 1

#Variables storing integar values used for displaying gif and for positioning/transforming of pictures
mainMenuCounter = 0
degreeIncreasement = 0
tempDegree = 0
saveOption = 1

#Used to store values for important values such as initial values for fish, predator and plant life.
fishSliderValue = 5
predatorSliderValue = 5
plantLifeSliderValue = 5

saveCreditsText = 650

fishSliderPos = -160
predatorSliderPos = -160
plantLifeSliderPos = -160

beforePauseTick = 0
ticksPassed = 0

savedTarget = 0
saveProcess = 0

day = True
restart = False

WHITE = (255, 255, 255)
checkList = [15, -20, -55, -90, -125, -160, -195, -235, -270, -305, -340]

#Creats a function to use for the Main Menu 
def drawMainMenuPage():
    init()
    #Globalizing variables needed for this part of the simulation
    global mainMenuCounter, mainMenu, optionsPage, mainSimBool, creditsPage
    mx, my = mouse.get_pos()
    for evnt in event.get():
        if (evnt.type == QUIT):
            menu = False 
        if evnt.type == MOUSEBUTTONDOWN:
            if 838 < mx < 950 and 360 < my < 420:
                menu = False 
                sys.exit()
            if 745 < mx < 953 and 307 < my < 345:
                optionsPage = True
                mainMenu = False
            if 680 < mx < 950 and 250 < my < 285:
                mainSimBool = True
                mainMenu = False
     
    if mainMenuCounter > 120:
        mainMenuCounter = 0
    else:
        mainMenuCounter += 1  

    screen.blit(menuBackgroundList[mainMenuCounter//12], (0, 0))
    screen.blit(seaLifeSimulation, (0, 0))
    screen.blit(initiateSim, (0, 0))
    screen.blit(settings, (0, 0))
    screen.blit(quit, (818, 318))
    
    if 680 < mx < 950 and 250 < my < 285:
        screen.blit(initiateSimSelect, (0, 0))
    elif 745 < mx < 953 and 307 < my < 345:
        screen.blit(settingsSelect, (0, 0))
        
#Function used in order to round the sliders to a certain spot inorder to demonstrate the 0 to 10 scaling
def sliderRounding(value):
    tempNum = abs(checkList[0] - value)
    position = 0
    for i in range(0, 11):
        if tempNum > abs(checkList[i] - value):
            tempNum = abs(checkList[i] - value)
            position = i
    return checkList[position], position


def creditsScreen():
    #Globalizing variables needed for this part of the simulation
    global tempDegree, degreeIncreasement, saveCreditsText, creditsPage, optionsPage
    for evnt in event.get():
        if evnt.type == QUIT:
            saveCreditsText = 650
            mixer.music.rewind()
        if evnt.type == KEYDOWN:
            saveCreditsText = 650
            mixer.music.rewind()
    tempDegree += degreeIncreasement
    tempDayNightWheel = transform.rotate(dayNightWheel, tempDegree)    
    screen.blit(coreBackground, (0, 0))
    screen.blit(tempDayNightWheel, (205 - abs(65*sin((1/28.65)*tempDegree)), 380 - abs(65*sin((1/28.65)*tempDegree))))
    screen.blit(fishSlider, (0, fishSliderPos))
    screen.blit(predatorSlider, (0, predatorSliderPos))
    screen.blit(plantLifeSlider, (0, plantLifeSliderPos))  
    screen.blit(saveSettings, (0, 0))
    screen.blit(initSim, (0, 0))    
    screen.blit(credits, (0, 0))  
    screen.blit(returnHome, (0, 0))
    screen.blit(creditsGreyFilter, (0, 0))
    screen.blit(creditsText, (0, saveCreditsText))
    saveCreditsText -= 1
    if saveCreditsText < -700:
        creditsPage = False
        optionsPage = True
        mixer.music.stop()

#Creating a function used to change the positioning of the sliders, used in the main Options function
def  sliderMovement():
    #Globalizing variables needed for this part of the simulation
    global fishSliderPos, predatorSliderPos, plantLifeSliderPos, fishSliderValue, predatorSliderValue, plantLifeSliderValue
    #Sets the values of each variable so they can be displayed
    fishSliderText = fontBauhaus.render(str(fishSliderValue), 1, (0,0,0))
    predatorSliderText = fontBauhaus.render(str(predatorSliderValue), 1, (0,0,0))
    plantLifeSliderText = fontBauhaus.render(str(plantLifeSliderValue), 1, (0,0,0))    
    #Puts the values of the mouse buttons and positions
    button = mouse.get_pressed()
    x, y = mouse.get_pos()    
    #Used to display the values where the slider is
    if predatorSliderValue == 10:
        predatorTextPos = 752
    else:
        predatorTextPos = 762
    if fishSliderValue == 10:
        fishTextPos = 607
    else:
        fishTextPos = 617  
    if plantLifeSliderValue == 10:
        plantLifeTextPos = 897
    else:
        plantLifeTextPos = 907     
    #If the button is pressed down, the values and sliders change accordingly
    if button[0] != 0:
        if 600 < x < 655:
            if 455 < y:
                fishSliderPos = 15
            elif 80 > y:
                fishSliderPos = -340
            else:
                fishSliderPos = y - 420
            screen.blit(predatorSliderText, Rect(predatorTextPos, predatorSliderPos + 405,400,400))
            screen.blit(plantLifeSliderText, Rect(plantLifeTextPos, plantLifeSliderPos + 405,400,400))              
        elif 745 < x < 800:
            if 455 < y:
                predatorSliderPos = 15
            elif 80 > y:
                predatorSliderPos = -340
            else:
                predatorSliderPos = y - 420
            screen.blit(fishSliderText, Rect(fishTextPos, fishSliderPos + 405,400,400))
            screen.blit(plantLifeSliderText, Rect(plantLifeTextPos, plantLifeSliderPos + 405,400,400))              
        elif 890 < x < 945:
            if 455 < y:
                plantLifeSliderPos = 15
            elif 80 > y:
                plantLifeSliderPos = -340
            else:
                plantLifeSliderPos = y - 420
            screen.blit(fishSliderText, Rect(fishTextPos, fishSliderPos + 405,400,400))
            screen.blit(predatorSliderText, Rect(predatorTextPos, predatorSliderPos + 405,400,400))      
    else:
        #Displays all the values accordingly at the position of the slider
        plantLifeSliderPos, plantLifeSliderValue = sliderRounding(plantLifeSliderPos)
        predatorSliderPos, predatorSliderValue = sliderRounding(predatorSliderPos)
        fishSliderPos, fishSliderValue = sliderRounding(fishSliderPos)   
        screen.blit(fishSliderText, Rect(fishTextPos, fishSliderPos + 405,400,400))
        screen.blit(predatorSliderText, Rect(predatorTextPos, predatorSliderPos + 405,400,400))
        screen.blit(plantLifeSliderText, Rect(plantLifeTextPos, plantLifeSliderPos + 405,400,400))           

#Function used to draw the main options page, including sliders and preset buttons which utilises file systems
def drawOptionPage():
    #Globalizing variables needed for this part of the simulation
    global mainSimBool, mainMenu, optionsPage, creditsPage, tempDegree, degreeIncreasement, plantLifeSliderPos, predatorSliderPos, fishSliderPos, saveOption,day
    #Gets the position of mouse by x and y values
    mx, my = mouse.get_pos()
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        if evnt.type == MOUSEBUTTONDOWN:
            # This looks for which the mouse was pressed down on, and does what needs to be processed
            if 190 < mx < 523 and 250 < my < 334 and saveOption == 1:
                optionsPage = False
                creditsPage = True
                mixer.music.play()
            elif 190 < mx < 525 and 150 < my < 235 and saveOption == 1:
                mainSimBool = True
                optionsPage = False
            elif 0 < mx < 145 and 0 < my < 700:
                mainMenu = True
                optionsPage = False
            if saveOption == -1:
                if 195 < mx < 525 and 140 < my < 200:
                    openSaves("save1.txt")
                elif 195 < mx < 525 and 210 < my < 260:
                    openSaves("save2.txt")
                elif 195 < mx < 525 and 270 < my < 330:
                    openSaves("save3.txt")            
            if 367 < mx < 453 and 540 < my < 620 and tempDegree != 180:
                degreeIncreasement = 20
            elif 264 < mx < 348 and 440 < my < 526 and tempDegree != 0:
                degreeIncreasement = 20
            elif 190 < mx < 525 and 65 < my < 140:
                saveOption = saveOption*(-1)   
            elif tempDegree != 180 and tempDegree != 0:   
                degreeIncreasement = 20
            else:
                degreeIncreasement = 0         
    
    #Changing the rotation of the day and night mode, to so it repersents the day and night choices
    tempDegree += degreeIncreasement
    if tempDegree == 0:
        day = True
    else:
        day = False     
    tempDayNightWheel = transform.rotate(dayNightWheel, tempDegree)
    screen.blit(coreBackground, (0, 0))
    screen.blit(tempDayNightWheel, (205 - abs(65*sin((1/28.65)*tempDegree)), 380 - abs(65*sin((1/28.65)*tempDegree))))
    
    #Displaying the grphical slider that is at the position of the values
    screen.blit(fishSlider, (0, fishSliderPos))
    screen.blit(predatorSlider, (0, predatorSliderPos))
    screen.blit(plantLifeSlider, (0, plantLifeSliderPos))
    screen.blit(saveSettings, (0, 0))
    if saveOption != -1:
        screen.blit(initSim, (0, 0))    
        screen.blit(credits, (0, 0))           
    screen.blit(returnHome, (0, 0))
    
    #Changes the appearence of the buttons once a mouse button is over it
    if 160 < mx < 550 and 30 < my <360:
        if 190 < mx < 525 and 65 < my < 140:
            screen.blit(saveSettingsSelect, (0, 0))      
        if saveOption == -1:
            screen.blit(saveDropDown, (0, 140)) 
            if 195 < mx < 525 and 140 < my < 200:
                screen.blit(saveOneSelect, (0, 140))
            elif 195 < mx < 525 and 210 < my < 260:
                screen.blit(saveTwoSelect, (0, 140))
            elif 195 < mx < 525 and 270 < my < 330:
                screen.blit(saveThreeSelect, (0, 140))
        else:
            if 190 < mx < 525 and 150 < my < 235:
                screen.blit(initSimSelect, (0, 0))
            elif 190 < mx < 525 and 250 < my < 335:
                screen.blit(creditsSelect, (0, 0))         
    elif 0 < mx < 145 and 0 < my < 700:
        screen.blit(returnHomeSelect, (0, 0))
        saveOption = 1
    else:
        saveOption = 1    
    
    if tempDegree == 180 or tempDegree == 0:
        degreeIncreasement = 0
    elif tempDegree == 360:
        tempDegree = 0
        degreeIncreasement = 0
    #Calls in the sliderMovement function which will change the positioning of the sliders and display the values
    sliderMovement()

#This function containes the components used to creat the main simulation
def mainSimulation():
    global mainSimBool, mainMenu, pauseMenuBool, startingScreen, saveConfigBool, savedTarget, beforePauseTick, saveProcess, restart
    mx, my = mouse.get_pos()
    if pauseMenuBool:
        if saveConfigBool == False:
            screen.blit(pauseMenuSkeleton, (0, 0))
            if 230 < mx < 770 and 235 < my < 517 and saveConfigBool == False:
                if 510 < mx < 760 and 455 < my < 508:
                    screen.blit(resumeSimRectSelect, (0, 0))
                elif 238 < mx < 478:
                    if 240 < my < 298:
                        screen.blit(mainMenuRectSelect, (0, 0))
                    elif 372 < my < 430:
                        screen.blit(restartSimRectSelect, (0, 0))
                    elif 305 < my < 365:
                        screen.blit(saveConfigRectSelect, (0, 0))
                    elif 455 < my < 510:
                        screen.blit(volumeRectSelect, (0, 0))
            if int(mixer.music.get_volume()) == 1:
                screen.blit(volumeOnSymbol, (0, 0))
            else:
                screen.blit(volumeOffSymbol, (0, 0))
            fishSliderText = fontBauhaus.render(str(fishSliderValue), 1, (0,0,0))
            predatorSliderText = fontBauhaus.render(str(predatorSliderValue), 1, (0,0,0))
            plantLifeSliderText = fontBauhaus.render(str(plantLifeSliderValue), 1, (0,0,0))    
            screen.blit(fishSliderText, Rect(690, 280, 400,400))
            screen.blit(predatorSliderText, Rect(690, 310, 400,400))
            screen.blit(plantLifeSliderText, Rect(690, 340, 400,400))
            if tempDegree == 180:
                screen.blit(nightMode, Rect(690, 390, 400,400))
            else:
                screen.blit(dayMode, Rect(690, 390, 400,400))
        else:
            screen.blit(saveMenuSkeleton, (0, 0))
            if savedTarget == saveProcess:
                if 305 < mx < 580:
                    if 233 < my < 287:
                        screen.blit(save1Select, (0, 0))
                    elif 320 < my < 380:
                        screen.blit(save2Select, (0, 0))
                    elif 412 < my < 470:
                        screen.blit(save3Select, (0, 0))
                elif 617 < mx < 690 and 230 < my < 470:
                    screen.blit(returnButtonSelect, (0, 0))
            else:
                screen.blit(savedSettings, (0, 0))
                saveProcess += 1 
    for evnt in event.get():
        if evnt.type == QUIT:
            menu = False
        #From here on is what will happen if mouse button is pressed down and the mouse is in one of the designated hit boxes
        if evnt.type == MOUSEBUTTONDOWN:
            if 10 < mx < 72 and 15 < my < 52 and pauseMenuBool == False:
                beforePauseTick = time.get_ticks()
                pauseMenuBool = not pauseMenuBool
            elif 10 < mx < 72 and 15 < my < 52:
                ticksPassed = beforePauseTick - time.get_ticks()
                pauseMenuBool = not pauseMenuBool 
                restart = False
                #simulationFunction(True)
            if pauseMenuBool == True and saveConfigBool == False:
                if 510 < mx < 760 and 455 < my < 508:
                    pauseMenuBool = False
                    restart = False
                if 238 < mx < 478:
                    if 240 < my < 298:
                        mainSimBool = False
                        pauseMenuBool = False
                        restart = False
                        mainMenu = True
                    elif 372 < my < 430:
                        restart = True
                    elif 305 < my < 365:
                        saveConfigBool = not saveConfigBool
                    elif 455 < my < 510:
                        if int(mixer.music.get_volume()) == 1:
                            mixer.music.set_volume(0)
                        else:
                            mixer.music.set_volume(1)
            elif pauseMenuBool == True and saveConfigBool == True:
                if 305 < mx < 580:
                    if 233 < my < 287 and saveProcess == savedTarget:
                        Save("save1.txt")
                        savedTarget += 25
                    elif 320 < my < 380 and saveProcess == savedTarget:
                        Save("save2.txt")
                        savedTarget += 25
                    elif 412 < my < 470 and saveProcess == savedTarget:
                        Save("save3.txt")
                        savedTarget += 25
                elif 617 < mx < 690 and 230 < my < 470:
                    saveConfigBool = False            
    mx, my = mouse.get_pos()
    if 10 < mx < 72 and 15 < my < 52:
        screen.blit(playPauseButtonSelect, (0, 0))
    else:
        screen.blit(playPauseButton, (0, 0))

def ifPause():
    return pauseMenuBool

def Restart():
    return restart

def ifMainMenu():
    return mainMenu
    
#Creats a function to display the graphic interface for the pause menu page
def pauseMenu(screen):
    global pauseMenuBool, saveProcess
    mx, my = mouse.get_pos()
    if saveConfigBool == False:
        screen.blit(pauseMenuSkeleton, (0, 0))
        if 230 < mx < 770 and 235 < my < 517 and saveConfigBool == False:
            if 510 < mx < 760 and 455 < my < 508:
                screen.blit(resumeSimRectSelect, (0, 0))
            elif 238 < mx < 478:
                if 240 < my < 298:
                    screen.blit(mainMenuRectSelect, (0, 0))
                elif 372 < my < 430:
                    screen.blit(restartSimRectSelect, (0, 0))
                elif 305 < my < 365:
                    screen.blit(saveConfigRectSelect, (0, 0))
                elif 455 < my < 510:
                    screen.blit(volumeRectSelect, (0, 0))
        if int(mixer.music.get_volume()) == 1:
            screen.blit(volumeOnSymbol, (0, 0))
        else:
            screen.blit(volumeOffSymbol, (0, 0))
        fishSliderText = fontBauhaus.render(str(fishSliderValue), 1, (0,0,0))
        predatorSliderText = fontBauhaus.render(str(predatorSliderValue), 1, (0,0,0))
        plantLifeSliderText = fontBauhaus.render(str(plantLifeSliderValue), 1, (0,0,0))    
        screen.blit(fishSliderText, Rect(690, 280, 400,400))
        screen.blit(predatorSliderText, Rect(690, 310, 400,400))
        screen.blit(plantLifeSliderText, Rect(690, 340, 400,400))
        if tempDegree == 180:
            screen.blit(nightMode, Rect(690, 390, 400,400))
        else:
            screen.blit(dayMode, Rect(690, 390, 400,400))
    else:
        screen.blit(saveMenuSkeleton, (0, 0))
        if savedTarget == saveProcess:
            if 305 < mx < 580:
                if 233 < my < 287:
                    screen.blit(save1Select, (0, 0))
                elif 320 < my < 380:
                    screen.blit(save2Select, (0, 0))
                elif 412 < my < 470:
                    screen.blit(save3Select, (0, 0))
            elif 617 < mx < 690 and 230 < my < 470:
                screen.blit(returnButtonSelect, (0, 0))
        else:
            screen.blit(savedSettings, (0, 0))
            saveProcess += 1

#Creats a function used to take information from a file
def openSaves(name):
    global tempDegree, fishSliderValue, predatorSliderValue, plantLifeSliderValue, fishSliderPos, predatorSliderPos, plantLifeSliderPos
    file = open(name, "r")  
    values = [line.rstrip('\n') for line in file]
    fishSliderValue, predatorSliderValue, plantLifeSliderValue, tempDegree = values[0], values[1], values[2], values[3]
    tempDegree = int(tempDegree)
    fishSliderPos = 15 - (35*int(fishSliderValue))
    predatorSliderPos = 15 - (35*int(predatorSliderValue))
    plantLifeSliderPos = 15 - (35*int(plantLifeSliderValue))    
    file.close()

#Creats a function to save to a file of need
def Save(name):
    file = open(name , "w")
    file.write(str(fishSliderValue) + "\n")
    file.write(str(predatorSliderValue)  + "\n")
    file.write(str(plantLifeSliderValue) + "\n")
    file.write(str(tempDegree) + "\n")
    file.close()
    # Load the fish images needed.
    
# Notes on Mathematics in the following program:
# All angles in this program are written in the range [0,360).
# The angles start from 0 degrees being the direct right of the point and 180 degrees being the direct left.
# The angle increases as the line representing the angle rotates counter-clockwise.
# The x and y coordinates are written according to pygame standards, with (0,0) being the top left corner.

# Notes on Computer Science data structures and algorithms used in the following program.
# The program uses Disjoint-set (Union Find) Data Structure to quickly join different school of fish.
# A school of fish can be seen as a disjoint set.
# The Disjoint-set variables used are parent and size. The functions it uses are getLeader(i), and join(i,j).
# The splitDeadFishSchool(fishAttacked) function is not optimized although it also deals with schools of fish.

# -- Editorial by Alex

# Load the images.
images = [transform.rotate(image.load("koi1.png"),90),transform.rotate(image.load("koi2.png"),90)]

# Declare variables for the number of fish and the number of predators.
numberOfFish = fishSliderValue
numberOfPredators = predatorSliderValue
numberOfPlant = plantLifeSliderValue

# Declare constants used in the program.
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SIZE = (1000,700)
FISH_TURN_SPEED = 5
FISH_TURN_RANGE = 45
FISH_TURN_TIME_RANGE_LOW = 500
FISH_TURN_TIME_RANGE_HIGH = 1000
FISH_SPEED = 5
FISH_TURN_RADIUS = 30
FLOCK_JOIN_DEGREE = 90
FLOCK_JOIN_DISTANCE = 70

lastRespawn = 0
RESPAWN_TIME = 20000
RESPAWN_SCALE = 1.5

# Declare lists used to keep track of the fish in the program.
fishImages = []
currentDegree = []  # degree of the direction that the fish is facing
turnEnd = []        # the time of the last turn at boundary
fishX = []          # coordinate of koi fish when not turning
fishY = []          # coordinate of koi fish when not turning
turnCentreX = []    # coordinate of point that the fish is revolving around
turnCentreY = []    # coordinate of point that the fish is revolving around
resultingX = []     # updated coordinate of koi fish when turning
resultingY = []     # updated coordinate of koi fish when turning
turning = []        # indicates if the fish is turning
turnDirection = []  # 1: turning left, -1: turning right
degreeChanged = []  # how many degrees the fish has turned from the start of the rotation
turnDegree = []     # how many degrees the fish needs to turn to face the centre
nextTurn = []       # the time of the next turn in milliseconds from the start of the program
boundary = []
fishTypes = []      # type of koi fish
parent = []         # parent of this fish in the school
size = []           # size of the school (only accurate for leader of school)
deltaX = []         # difference in x coordinate from leader of school to member of school
deltaY = []         # difference in x coordinate from leader of school to member of school
fishDeathTime = []  # time of the fish's death, -1 if the fish is not dead

# Set up variables regarding the predator.
lastAttack = 0
underAttack = False
predatorX = 0
predatorY = 0
predatorDegree = 0
fishToAttack = -1
predatorImage = transform.rotate(image.load("swordfish.png"),270)
PREDATOR_FOOD_TIME = 60000
PREDATOR_KILL_RANGE = 30
PREDATOR_SPEED = 20
fishAttacked = False

waterTime = 0
opacity = 200

class Lily(sprite.Sprite): 
    def __init__(self):  #randomly selects image and location of lily
        sprite.Sprite.__init__(self)
        self.image = random.choice([image.load('lily1.png'), image.load('lily2.png'), image.load('lily3.png')])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(250,900)
        self.rect.y = random.randint(100,600)
    def draw(self, screen, opacity):
        temp = Surface((self.image.get_width(), self.image.get_height())).convert()   
        temp.blit(screen, (-self.rect.x, -self.rect.y))        
        temp.blit(self.image, (0, 0))
        temp.set_alpha(opacity)  
        screen.blit(temp, self.rect)
        #image of lily is blitted onto a temporary surface so only the image's opacity is affected


lily_list = sprite.Group()
def Plants():
    global numberOfPlant
    for i in range(plantLifeSliderValue):        
        lily_list.add(Lily())

# Set up variables regarding dead fish skeleton.
skeletonImage = transform.rotate(image.load("deadfish.png"),180)
SKELETON_TIME = 3000    # time to show the skeleton for

# A function that sets the number of fish and predators in the simulation.
def setNumberOfFishAndPredators(fish,predators):
    global numberOfFish,numberOfPredators
    numberOfFish = fish
    numberOfPredators = predators

# A function that clears all the list variables in the simulation.
def clearLists():
    global fishImages,currentDegree,turnEnd,fishX,fishY,turnCentreX,turnCentreY,resultingX,resultingY,turning,turnDirection
    global degreeChanged,turnDegree,nextTurn,boundary,fishTypes,parent,size,deltaX,deltaY,fishDeathTime

    del fishImages[ : ]
    del currentDegree[ : ]
    del turnEnd[ : ]
    del fishX[ : ]
    del fishY[ : ]
    del turnCentreX[ : ]
    del turnCentreY[ : ]
    del resultingX[ : ]
    del resultingY[ : ]
    del turning[ : ]
    del turnDirection[ : ]
    del degreeChanged[ : ]
    del turnDegree[ : ]
    del nextTurn[ : ]
    del boundary[ : ]
    del fishTypes[ : ]
    del parent[ : ]
    del size[ : ]
    del deltaX[ : ]
    del deltaY[ : ]
    del fishDeathTime[ : ]

# A function that resets most variables to their default value.
# This function needs to be called when simulation starts and restarts.
def resetImportantVariables():
    global fishImages,currentDegree,turnEnd,fishX,fishY,turnCentreX,turnCentreY,resultingX,resultingY,turning,turnDirection
    global degreeChanged,turnDegree,nextTurn,boundary,fishTypes,parent,size,deltaX,deltaY,fishDeathTime,numberOfFish
    global underAttack,fishAttacked
    clearLists()
    underAttack = False
    fishAttacked = False
    
# A function that updates time variables after the user resumes the simulation.
def resumeAfterPause(elapsedTime):
    global nextTurn,fishDeathTime,turnEnd,lastAttack,lastRespawn

    for i in range(numberOfFish):
        nextTurn[i] += elapsedTime
        if (fishDeathTime[i] != -1):
            fishDeathTime[i] += elapsedTime
        turnEnd[i] += elapsedTime
        lastAttack += elapsedTime
        lastRespawn += elapsedTime

# A function that can be used to calculate the angle between two points in terms of one of the points.
# Using variable names in the function, the function calculates the angle of (otherPointX,otherPointY) when viewed from (centrePointX,centrePointY).
def getDegreeAroundPoint(centrePointX,centrePointY,otherPointX,otherPointY):
    # Calculate the slope between the two points.
    if (otherPointX == centrePointX):
        slope = "INF"
    else:
        slope = (centrePointY - otherPointY) / (otherPointX - centrePointX)
        # Calculate the angle with trigonometry. This is not the final result because the angle may be improperly orientated.
        degree = (math.degrees(math.atan(slope)) + 360) % 360

    # Use case work to calculate the final angle using the slope.
    if (slope == "INF"):
        if (centrePointY < otherPointY):
            degree = 270
        else:
            degree = 90
    elif (slope > 0):
        if (centrePointY < otherPointY):
            degree += 180
    elif (slope < 0):
        if (centrePointY > otherPointY):
            degree += 180
    else:
        if (centrePointX > otherPointX):
            degree += 180
    degree %= 360

    # Return the resulting angle.
    return degree

# A function that adds default values to the list variables.
def initializeListVariables(newFish):
    global fishImages,currentDegree,turnEnd,fishX,fishY,turnCentreX,turnCentreY,resultingX,resultingY,deltaX,deltaY,boundary
    global turning,turnDirection,degreeChanged,nextTurn,turnDegree,numberOfFish,parent,size,fishTypes,fishDeathTime
    # According to how many fish are new, add the appropriate number of elements into the lists.
    for i in range(newFish):
        fishType = random.randint(0,len(images) - 1)
        boundary.append(100)
        fishImages.append(images[fishType])
        fishTypes.append(fishType)
        currentDegree.append(random.randint(0,359))
        turnEnd.append(-1000)
        fishX.append(random.randint(200,SCREEN_WIDTH - 200))
        fishY.append(random.randint(200,SCREEN_HEIGHT - 200))
        turnCentreX.append(0)
        turnCentreY.append(0)
        resultingX.append(0)
        resultingY.append(0)
        turning.append(False)
        turnDirection.append(0)
        degreeChanged.append(0)
        nextTurn.append(0)
        turnDegree.append(0)
        parent.append(len(size))
        size.append(1)
        deltaX.append(0)
        deltaY.append(0)
        fishDeathTime.append(-1)
    numberOfFish += newFish

# A function that recursively gets the leader of a school of fish.
# This function is optimized to the scenario that the user calls it with the same parameters multiple times without changing the schools.
def getLeader(i):
    if (parent[i] == i):
        return i
    else:
        parent[i] = getLeader(parent[i])    # stores the result in the parent list so that same parameter calls are faster
        return parent[i]

# A function that joins two schools of fish efficiently. The parameters are members of the different schools that need to be joined.
def join(i,j):
    global currentDegree,parent,size,deltaX,deltaY

    a = getLeader(i)
    b = getLeader(j)
    # Another optimization made in the Disjoint-set Data Structure is checking for the size of the two schools.
    # This ensures that the smaller group is joined into the bigger group and thus the depth in the combined set is smaller.
    if (size[a] > size[b]):
        # Join school led by b into school led by a.
        size[a] += size[b]
        for i in range(numberOfFish):
            if (getLeader(i) == b):
                # Update the distance to the new leader of the group, and ensure all fish in the school face the same direction.
                currentDegree[i] = currentDegree[a]
                deltaX[i] = fishX[i] - fishX[a]
                deltaY[i] = fishY[i] - fishY[a]
        parent[b] = a
    else:
        # Join school led by a into school led by b.
        size[b] += size[a]
        for i in range(numberOfFish):
            if (getLeader(i) == a):
                # Update the distance to the new leader of the group, and ensure all fish in the school face the same direction.
                currentDegree[i] = currentDegree[b]
                deltaX[i] = fishX[i] - fishX[b]
                deltaY[i] = fishY[i] - fishY[b]
        parent[a] = b

# A function that splits a school of fish after the leader is dead.
def splitDeadFishSchool(i):
    global parent,size,currentDegree,numberOfFish

    for j in range(numberOfFish):
        if (getLeader(j) == i and j != i):
            # Make each fish become a new group.
            parent[j] = j
            size[j] = 1
            # Generate a random degree for the fish to swim in.
            currentDegree[j] = random.randint(0,359)

# A function that updates the joining of schools of fish.
def school():
    global currentDegree,size,parent,fishX,fishY

    # Pick each pair of fish.
    for i in range(numberOfFish):
        for j in range(numberOfFish):
            # Make sure they are in different groups.
            if (getLeader(i) != getLeader(j)):
                # Check if the leader fish of the two schools are dead or in the middle of a turn.
                if ((not turning[getLeader(i)]) and (not turning[getLeader(j)]) and 
                    (fishDeathTime[getLeader(i)] == -1) and (fishDeathTime[getLeader(j)] == -1)):
                    tempDegree = (currentDegree[getLeader(i)] + 360 - currentDegree[getLeader(j)]) % 360
                    # Check if the two schools are close and have similar orientations.
                    if ((fishX[getLeader(i)] - fishX[getLeader(j)]) ** 2 + 
                        (fishY[getLeader(i)] - fishY[getLeader(j)]) ** 2 < FLOCK_JOIN_DISTANCE ** 2 and
                        min(tempDegree,360 - tempDegree) < FLOCK_JOIN_DEGREE):
                        join(i,j)

# A function that determines the location of a turning fish and draws it on the screen.
def turnAroundPoint(screen,img,pointX,pointY,radius,degreeFromPoint,i):
    global resultingX,resultingY

    # Calculate the coordinates of the fish by using the point it is revolving around.
    imgX = pointX + math.cos(math.radians(degreeFromPoint)) * radius
    imgY = pointY - math.sin(math.radians(degreeFromPoint)) * radius

    # Update the coordinates.
    resultingX[i] = imgX
    resultingY[i] = imgY

    # Draw it on the screen.
    w,h = img.get_rect().size
    screen.blit(img,(imgX - w / 2,imgY - h / 2))

# A function that organizes all the movements in the simulation.
def moveFish(screen):
    global fishImages,currentDegree,turnEnd,fishX,fishY,turnCentreX,turnCentreY,resultingX,resultingY,predatorX,predatorY
    global turning,turnDirection,degreeChanged,nextTurn,turnDegree,deltaX,deltaY,underAttack,lastAttack,fishToAttack,predatorDegree
    global fishAttacked,numberOfFish

    # Use a for loop to iterate through each fish because the numberOfFish may change.
    i = 0
    while (i < numberOfFish):
        # Check if the fish is alive.
        if (fishDeathTime[i] == -1):
            # Check if the fish is a leader.
            if (getLeader(i) == i):
                # Check if the fish is turning.
                if (turning[i]):
                    # Change the degree of the fish.
                    degreeChanged[i] += FISH_TURN_SPEED
                    currentDegree[i] = (currentDegree[i] + FISH_TURN_SPEED * turnDirection[i]) % 360

                    # Check if the fish should stop turning.
                    if (degreeChanged[i] > turnDegree[i]):
                        turning[i] = False
                        turnEnd[i] = time.get_ticks()
                        fishX[i] = resultingX[i]
                        fishY[i] = resultingY[i]

                else:
                    # If the fish is not turning, and the time for the next shift has reached, the fish can shift its angle randomly.
                    if (time.get_ticks() - turnEnd[i] > 500 and time.get_ticks() > nextTurn[i]):
                        currentDegree[i] = (currentDegree[i] + random.randint(-FISH_TURN_RANGE,FISH_TURN_RANGE)) % 360
                        nextTurn[i] = time.get_ticks() + random.randint(FISH_TURN_TIME_RANGE_LOW,FISH_TURN_TIME_RANGE_HIGH)

                # Hold the rotated image of the fish in a variable.
                koi = transform.rotate(fishImages[i],currentDegree[i])

                # Check if the fish is turning.
                if (turning[i]):
                    # Calculate the degree from the fish to the turning centre.
                    turnCentreDegree = (currentDegree[i] + turnDirection[i] * 90 + 360) % 360

                    # Call the function with the second last parameter being the degree from the turning centre to the fish.
                    turnAroundPoint(screen,koi,turnCentreX[i],turnCentreY[i],FISH_TURN_RADIUS,(turnCentreDegree + 180) % 360,i)

                else:
                    # If the fish is not turning, continue its regular movement.
                    # Update the coordinates and draw the fish.
                    fishX[i] += (FISH_SPEED * math.cos(math.radians(currentDegree[i])))
                    fishY[i] -= (FISH_SPEED * math.sin(math.radians(currentDegree[i])))
                    w,h = koi.get_rect().size
                    screen.blit(koi,(fishX[i] - w / 2,fishY[i] - h / 2))

                    # Check if it is time to turn again if it has been over a second from the last turn.
                    if (time.get_ticks() - turnEnd[i] > 1000):
                        if (fishX[i] > SCREEN_WIDTH - boundary[i] or fishY[i] > SCREEN_HEIGHT - boundary[i] or
                            fishX[i] < boundary[i] or fishY[i] < boundary[i]):
                            # It is time to turn again. Assign variables needed for the turn.
                            turning[i] = True
                            resultingX[i] = fishX[i]
                            resultingY[i] = fishY[i]
                            turnDirection[i] = random.randint(0,1)
                            if (turnDirection[i] == 0):
                                turnDirection[i] = -1
                            turnCentreDegree = (currentDegree[i] + turnDirection[i] * 90) % 360
                            degreeChanged[i] = 0

                            # Find the turning centre of this rotation.
                            turnCentreX[i] = fishX[i] + FISH_TURN_RADIUS * math.cos(math.radians(turnCentreDegree))
                            turnCentreY[i] = fishY[i] - FISH_TURN_RADIUS * math.sin(math.radians(turnCentreDegree))

                            # Find the centre of the water.
                            centreX = SCREEN_WIDTH / 2
                            centreY = SCREEN_HEIGHT / 2

                            # Calculate the degree from the turning centre to the centre of the water.
                            tempDegree = getDegreeAroundPoint(turnCentreX[i],turnCentreY[i],centreX,centreY)

                            # Calculate the distance between the turning centre and the centre of the water.
                            distance = ((turnCentreX[i] - centreX) ** 2 + (centreY - turnCentreY[i]) ** 2) ** 0.5

                            # Form a right triangle with the tangent point, the turning centre and the centre of the water.
                            # Using the triangle, calculate the angle that the fish should be at after the turn.
                            # Then, calculate the degree that the fish should turn to get to the ending position.
                            tempDegree = (tempDegree + 360 - turnDirection[i] * math.degrees(math.acos(FISH_TURN_RADIUS / distance))) % 360
                            degreeFromCentre = (currentDegree[i] - turnDirection[i] * 90 + 360) % 360
                            if (turnDirection[i] == 1):
                                turnDegree[i] = (tempDegree + 360 - degreeFromCentre) % 360
                            else:
                                turnDegree[i] = (degreeFromCentre + 360 - tempDegree) % 360

            else:
                # If the fish is not a leader, simply follow the leader's movements.
                currentDegree[i] = currentDegree[getLeader(i)]
                if (turning[getLeader(i)]):
                    fishX[i] = resultingX[getLeader(i)] + deltaX[i]
                    fishY[i] = resultingY[getLeader(i)] + deltaY[i]
                else:
                    fishX[i] = fishX[getLeader(i)] + deltaX[i]
                    fishY[i] = fishY[getLeader(i)] + deltaY[i]

                # Draw the fish onto the screen
                koi = transform.rotate(fishImages[i],currentDegree[i])
                w,h = koi.get_rect().size
                screen.blit(koi,(fishX[i] - w / 2,fishY[i] - h / 2))

        elif (time.get_ticks() - fishDeathTime[i] <= SKELETON_TIME):    # fish had just died
            # Display a skeleton in the fish's place.
            skeleton = transform.rotate(skeletonImage,currentDegree[i])
            w,h = skeleton.get_rect().size
            if (turning[i]):
                screen.blit(skeleton,(resultingX[i] - w / 2,resultingY[i] - h / 2))
            else:
                screen.blit(skeleton,(fishX[i] - w / 2,fishY[i] - h / 2))
        else:
            # The fish had been dead for a long time.
            # Change some parent values so that the deletion of the element does not effect other relations in the disjoint sets.
            for j in range(numberOfFish):
                if (getLeader(j) > i):
                    parent[j] = getLeader(j) - 1

            # Delete the fish from the list
            del fishImages[i]
            del currentDegree[i]
            del turnEnd[i]
            del fishX[i]
            del fishY[i]
            del turnCentreX[i]
            del turnCentreY[i]
            del resultingX[i]
            del resultingY[i]
            del turning[i]
            del turnDirection[i]
            del degreeChanged[i]
            del turnDegree[i]
            del nextTurn[i]
            del boundary[i]
            del fishTypes[i]
            del parent[i]
            del size[i]
            del deltaX[i]
            del deltaY[i]
            del fishDeathTime[i]
            i -= 1
            numberOfFish -= 1
        i += 1

    # Check if the predator fish is attacking.
    if (underAttack):
        # Check if the targeted fish is not yet attacked.
        if (not fishAttacked):
            # Get the coordinates of the targeted fish.
            if (turning[fishToAttack]):
                attackedX = resultingX[fishToAttack]
                attackedY = resultingY[fishToAttack]
            else:
                attackedX = fishX[fishToAttack]
                attackedY = fishY[fishToAttack]

            # Check if the distance between the targeted fish and the predator is close.
            distance = ((predatorX - attackedX) ** 2 + (predatorY - attackedY) ** 2) ** 0.5
            if (distance < PREDATOR_KILL_RANGE):
                # The targeted fish is killed.
                fishDeathTime[fishToAttack] = time.get_ticks()
                fishAttacked = True
                splitDeadFishSchool(fishToAttack)

            # Change the predator's orientation if the targeted fish is not killed yet.
            # This ensures that the predator will always be chasing after the target.
            if (not fishAttacked):
                predatorDegree = getDegreeAroundPoint(predatorX,predatorY,attackedX,attackedY)

        # Update the predator's coordinates.
        predatorX += math.cos(math.radians(predatorDegree)) * PREDATOR_SPEED
        predatorY -= math.sin(math.radians(predatorDegree)) * PREDATOR_SPEED

        # Draw the predator onto the screen.
        predator = transform.rotate(predatorImage,predatorDegree)
        w,h = predator.get_rect().size
        screen.blit(predator,(predatorX - w / 2,predatorY - h / 2))

        # If the predator is outside of the screen and has killed the target, end this attack.
        if (((((predatorX - w / 2) < 0 or (predatorX - w / 2) > SCREEN_WIDTH) and 
              ((predatorX + w / 2) < 0 or (predatorX + w / 2) > SCREEN_WIDTH)) or
             (((predatorY - h / 2) < 0 or (predatorY - h / 2) > SCREEN_HEIGHT) and
              ((predatorY + h / 2) < 0 or (predatorY + h / 2) > SCREEN_HEIGHT))) and
            fishAttacked):
            underAttack = False

        # Emergency situation: in case the predator does not kill a fish in time,
        # or if the direction that was determined made killing the fish impossible, end this attack.
        # In new code, this should never happen, but it is left here for unconsidered scenarios.
        if (numberOfPredators > 0):
            if (time.get_ticks() - lastAttack > PREDATOR_FOOD_TIME * 2 / numberOfPredators):
                underAttack = False
    else:
        if (numberOfPredators > 0):     # prevent division by zero
            # Check if it is time to launch a new attack.
            if (time.get_ticks() - lastAttack > PREDATOR_FOOD_TIME / numberOfPredators):
                # Launch a new attack.
                underAttack = True
                fishAttacked = False
                fishToAttack = getLeader(random.randint(0,numberOfFish - 1))    # randomly choose a target
                lastAttack = time.get_ticks()

                # Get the target's coordinates.
                if (turning[fishToAttack]):
                    attackedX = resultingX[fishToAttack]
                    attackedY = resultingY[fishToAttack]
                else:
                    attackedX = fishX[fishToAttack]
                    attackedY = fishY[fishToAttack]

                # Generate an angle that the predator will come in at.
                tempDegree = random.randint(0,359)
                predatorDegree = (tempDegree + 180) % 360

                # Find the coordinates that the predator will start at by doing case work.
                predator = transform.rotate(predatorImage,predatorDegree)
                w,h = predator.get_rect().size
                if (tempDegree == 90):      # special case: used to prevent undefined tangent value
                    predatorX = attackedX
                    predatorY = -h / 2
                elif (tempDegree == 270):   # special case: used to prevent undefined tangent value
                    predatorX = attackedX
                    predatorY = SCREEN_HEIGHT + h / 2
                else:
                    # Calculate the degrees to each corner of the window.
                    degreeToTopLeft = getDegreeAroundPoint(attackedX,attackedY,0,0)
                    degreeToTopRight = getDegreeAroundPoint(attackedX,attackedY,SCREEN_WIDTH,0)
                    degreeToBottomLeft = getDegreeAroundPoint(attackedX,attackedY,0,SCREEN_HEIGHT)
                    degreeToBottomRight = getDegreeAroundPoint(attackedX,attackedY,SCREEN_WIDTH,SCREEN_HEIGHT)

                    # Determine which side the predator will be immediately outside of with case work.
                    # Then, calculate the coordinates of the starting position of the predator.
                    if (tempDegree > degreeToTopRight and tempDegree <= degreeToTopLeft):
                        predatorY = -h / 2
                        predatorX = attackedX + ((attackedY - predatorY) / math.tan(math.radians(tempDegree)))
                    elif (tempDegree > degreeToTopLeft and tempDegree <= degreeToBottomLeft):
                        predatorX = -w / 2
                        predatorY = attackedY - ((predatorX - attackedX) * math.tan(math.radians(tempDegree)))
                    elif (tempDegree > degreeToBottomLeft and tempDegree <= degreeToBottomRight):
                        predatorY = SCREEN_HEIGHT + h / 2
                        predatorX = attackedX + ((attackedY - predatorY) / math.tan(math.radians(tempDegree)))
                    else:
                        predatorX = SCREEN_WIDTH + w / 2
                        predatorY = attackedY - ((predatorX - attackedX) * math.tan(math.radians(tempDegree)))
#def editSaves()
running = True
menu = True
dayFrames = ["day1.png", "day2.png"]
nightFrames = ["night1.png", "night2.png"]
frames = dayFrames
flowers = image.load("reeds.png")
rock = image.load("rock.png")
timePaused = 0
paused = False

while running:  
    #changes background depending on user input on the settings page
    if day:
        frames = dayFrames
        lilyGrow = True 
    else:
        frames = nightFrames
        flowers = image.load("flowers.png")
        lilyGrow = False
    frame = frames[0]
    #variable init for simulation
    BACKGROUND_OCEAN = image.load(frame)
    initializeListVariables(fishSliderValue)
    Plants() 
    setNumberOfFishAndPredators(fishSliderValue,predatorSliderValue)    
    while (menu):
        mixer.music.stop()
        if mainMenu == True:
            mixer.music.stop()            
            drawMainMenuPage()
        elif optionsPage == True:
            drawOptionPage()	
        elif creditsPage == True:
            creditsScreen()
        if mainSimBool == True:
            #set lilies to only grow at night
            if day:
                frames = dayFrames
                lilyGrow = True 
            else:
                frames = nightFrames
                flowers = image.load("flowers.png")
                lilyGrow = False
            lily_list.empty()
            Plants()            
            frame = frames[0]
            BACKGROUND_OCEAN = image.load(frame)            
            resetImportantVariables()
            initializeListVariables(fishSliderValue)
            setNumberOfFishAndPredators(fishSliderValue,predatorSliderValue) 
            mixer.music.load("up.mp3")
            mixer.music.play(-1)                  
            menu = False
        display.flip()
        myClock.tick(60)  
        
    while mainSimBool:  
        for evnt in event.get():
            if (evnt.type == QUIT):
                running = False
        screen.blit(BACKGROUND_OCEAN, (0,0))
        if mainMenu:
            menu = True        
            mainSimBool = False
            #resumes after pause menu, adjusts time variables to account for time paused
        #made a function as there was an error where variable only became true during click
        if not ifPause():
            if paused:
                resumeAfterPause(time.get_ticks()-timePaused)
                paused = False
            moveFish(screen)
            school()
        else:
            if not paused:
                timePaused = time.get_ticks()
                paused = True
            if Restart():
                resetImportantVariables()
                initializeListVariables(fishSliderValue)
                setNumberOfFishAndPredators(fishSliderValue,predatorSliderValue)  
                           
        if numberOfFish == 0:
            mixer.music.stop()            
            mainMenu = True        
            mainSimBool = False            
            
        screen.blit(flowers, (5,420))
        screen.blit(rock, (40,365))
        #draws lilies and respawns fish
        for lily in lily_list:
            lily.draw(screen, opacity)
            
        if (time.get_ticks() - lastRespawn > RESPAWN_TIME):
            initializeListVariables(int(numberOfFish * (RESPAWN_SCALE - 1)))
            lastRespawn = time.get_ticks()   
        #controls lily opacity and changes background frames
        if time.get_ticks()- waterTime > 200:
            waterTime = time.get_ticks()
            if frame == frames[0]:
                frame = frames[1]
                BACKGROUND_OCEAN = image.load(frame)
            elif frame == frames[1]:
                frame = frames[0]
                BACKGROUND_OCEAN = image.load(frame) 
            if lilyGrow:
                opacity += 4
                if opacity > 200:
                    opacity -= 3
                    if opacity > 250:
                        lilyGrow = False
            else:
                if day:
                    opacity -= 10
                    if opacity < 30:
                        lilyGrow = True
                        lily_list.empty()
                        Plants()  
        mainSimulation()
        display.flip()
    menu = True  
    
