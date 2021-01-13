
from pygame import *
from AlexIreneTim import *
import random
import math

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

# Load the fish images needed.
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

#def Save(name):
        #global fishSliderValue, predatorSliderValue, plantLifeSliderValue
        #file = open(name , "w")
        #file.write(str(fishSliderValue) + "\n")
        #file.write(str(predatorSliderValue)  + "\n")
        #file.write(str(plantLifeSliderValue) + "\n")
        #file.close()

#def Load(name):
        #global fishSliderValue, predatorSliderValue, plantLifeSliderValue
        #file = open(name, "r")  
        #values = [line.rstrip('\n') for line in file]
        #fishSliderValue, predatorSliderValue, plantLifeSliderValue = values[0], values[1], values[2]
        #file.close()
        #running = True

class Lily(sprite.Sprite): 
        def __init__(self): 
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


lily_list = sprite.Group()

def Plants():
        global numberOfPlant
        for i in range(numberOfPlant):        
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
        parent.append(i)
        size.append(1)
        deltaX.append(0)
        deltaY.append(0)
        fishDeathTime.append(-1)
    numberOfFish += newFish

# A function that recursively gets the leader of a school of fish.
# This function is optimized to the scenario that the user calls it with the same parameters multiple times without changing the schools.
def getLeader(i):
    if (i >= numberOfFish):
        print(numberOfFish)
        for j in range(numberOfFish):
            print(fishDeathTime[j],end = " ")
        print()
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