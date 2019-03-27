import queue

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
    global currentPoint, lastMove
    currentPoint = goRight(currentPoint)
    lastMove = 0
    setMaze(currentPoint, '#')

def doMoveLeft():
    global currentPoint, lastMove
    currentPoint = goLeft(currentPoint)
    lastMove = 1
    setMaze(currentPoint, '#')

def doMoveUp():
    global currentPoint, lastMove
    currentPoint = goUp(currentPoint)
    lastMove = 2
    setMaze(currentPoint, '#')

def doMoveDown():
    global currentPoint, lastMove
    currentPoint = goDown(currentPoint)
    lastMove = 3
    setMaze(currentPoint, '#')

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

fileName = "maze_small.txt"
fileInput = open(fileName, "r");

maze = []
queueMove = queue.Queue(maxsize=20)

strMaze = fileInput.read()
print(strMaze)

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

for i in maze:
    print('\n')
    for j in i:
        print(j),
