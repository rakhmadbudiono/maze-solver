from colorama import Fore, Back, Style
import queue, sys

def manhattanDistance(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def goRight(point):
    return (point[0]+1, point[1])

def goLeft(point):
    return (point[0]-1, point[1])

def goUp(point):
    return (point[0], point[1]-1)

def goDown(point):
    return (point[0], point[1]+1)

def isFinish():
    return currentPoint == finishPoint

def obstacleCheck(point):
    return maze[point[1]][point[0]]

def setMaze(point, c):
    global maze
    maze[point[1]][point[0]] = c

def doMoveRight():
    global currentPoint, lastMove, predList
    pred = currentPoint
    currentPoint = goRight(currentPoint)
    lastMove = 0
    predList.append((pred, currentPoint))

def doMoveLeft():
    global currentPoint, lastMove, predList
    pred = currentPoint
    currentPoint = goLeft(currentPoint)
    lastMove = 1
    predList.append((pred, currentPoint))

def doMoveUp():
    global currentPoint, lastMove, predList
    pred = currentPoint
    currentPoint = goUp(currentPoint)
    lastMove = 2
    predList.append((pred, currentPoint))

def doMoveDown():
    global currentPoint, lastMove, predList
    pred = currentPoint
    currentPoint = goDown(currentPoint)
    lastMove = 3
    predList.append((pred, currentPoint))

def moveBacktrack(tupleMove):
    global currentPoint
    currentPoint = tupleMove[0]
    if tupleMove[1] == 0:
        doMoveRight()
    if tupleMove[1] == 1:
        doMoveLeft()
    if tupleMove[1] == 2:
        doMoveUp()
    if tupleMove[1] == 3:
        doMoveDown()

def isDeadEnd():
    count = 0
    if not (obstacleCheck(goRight(currentPoint)) == '1'):
        count = count + 1
    if not (obstacleCheck(goLeft(currentPoint)) == '1'):
        count = count + 1
    if not (obstacleCheck(goUp(currentPoint)) == '1'):
        count = count + 1
    if not (obstacleCheck(goDown(currentPoint)) == '1'):
        count = count + 1
    return count == 1

def isAnyDecision():
    count = 0
    if not (obstacleCheck(goRight(currentPoint)) == '1'):
        count = count + 1
    if not (obstacleCheck(goLeft(currentPoint)) == '1'):
        count = count + 1
    if not (obstacleCheck(goUp(currentPoint)) == '1'):
        count = count + 1
    if not (obstacleCheck(goDown(currentPoint)) == '1'):
        count = count + 1
    return count > 2

def queueListing():
    global queueMove
    listDistance = []

    if not (obstacleCheck(goRight(currentPoint)) == '1'):
        listDistance.append((0, manhattanDistance(goRight(currentPoint), finishPoint)))
    if not (obstacleCheck(goLeft(currentPoint)) == '1'):
        listDistance.append((1, manhattanDistance(goLeft(currentPoint), finishPoint)))
    if not (obstacleCheck(goUp(currentPoint)) == '1'):
        listDistance.append((2, manhattanDistance(goUp(currentPoint), finishPoint)))
    if not (obstacleCheck(goDown(currentPoint)) == '1'):
        listDistance.append((3, manhattanDistance(goDown(currentPoint), finishPoint)))

    listDistance.sort(key=lambda tup: tup[1])

    for i in listDistance:
        queueMove.put((currentPoint, i[0]))
    #make queue w/ (point, move) w/ shortest distance priority

def goWithFlow():
    if not (lastMove == 1) and not (obstacleCheck(goRight(currentPoint)) == '1'):
        doMoveRight()
    elif not (lastMove == 0) and not (obstacleCheck(goLeft(currentPoint)) == '1'):
        doMoveLeft()
    elif not (lastMove == 3) and not (obstacleCheck(goUp(currentPoint)) == '1'):
        doMoveUp()
    elif not (lastMove == 2) and not (obstacleCheck(goDown(currentPoint)) == '1'):
        doMoveDown()

def popUntil(point):
    global predList
    while not (predList[len(predList)-1][1] == point):
        predList.pop(len(predList)-1)
        if(len(predList) == 0):
            break

fileName = "maze_xlarge.txt"
fileInput = open(fileName, "r");

maze = []
predList = []
queueMove = queue.Queue()

strMaze = fileInput.read()

listStrMaze = strMaze.split('\n')
for i in range(0,len(listStrMaze)-1):
    listPerLine = list(listStrMaze[i])
    maze.append(listPerLine)

for i in range(0, len(maze)):
    if maze[i][0] == '0':
        startingPoint = (0,i)
        break

for i in range(0, len(maze)):
    if maze[i][len(maze)-1] == '0':
        finishPoint = (len(maze)-1,i)
        break

currentPoint = startingPoint


doMoveRight()
while not isFinish():
    if isAnyDecision():
        queueListing()
        moveBacktrack(queueMove.get())
    elif isDeadEnd():
        moveBacktrack(queueMove.get())
    else:
        goWithFlow()

setMaze(startingPoint, '#')
while not (len(predList) == 0):
    markPoint = predList[len(predList)-1][1]
    setMaze(markPoint, '#')
    popUntil(predList[len(predList)-1][0])

for i in range(0,len(maze[1])):
    sys.stdout.write('\n')
    sys.stdout.flush()
    for j in range(0,len(maze[1])):
        if maze[i][j] == '1':
            sys.stdout.write(Back.BLACK + " ")
            sys.stdout.flush()
        elif maze[i][j] == '#':
            sys.stdout.write(Back.GREEN + " ")
            sys.stdout.flush()
        elif maze[i][j] == '0':
            sys.stdout.write(Back.WHITE + " ")
            sys.stdout.flush()

sys.stdout.write('\n')
sys.stdout.flush()
