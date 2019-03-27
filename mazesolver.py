def manhattanDistance(p1, p2):
    return abs(p1[0]-p2[0])+abs(p1[1]-p2[1])

def goRight(point):
    point += (1, 0)

def goLeft(point):
    point += (-1, 0)

def goUp(point):
    point += (0, -1)

def goDown(point):
    point += (0, 1)

fileName = "maze_small.txt"
fileInput = open(fileName, "r");

maze = []

strMaze = fileInput.read()
print(strMaze)

listStrMaze = strMaze.split('\n')
for i in range(0,len(listStrMaze)-1):
    listPerLine = list(listStrMaze[i])
    maze.append(listPerLine)

for i in range(0, len(maze)):
    if maze[i][0] == '0':
        startingPoint = (0,i)

for i in range(0, len(maze)):
    if maze[i][len(maze)-1] == '0':
        finishPoint = (len(maze)-1,i)

currentPoint = startingPoint
