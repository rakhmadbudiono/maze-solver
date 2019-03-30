from colorama import init, Fore, Back, Style
import os, sys, queue
from collections import deque

init()

class Node:
	def __init__(self, symbol = "", visited = False, parent = None):
		self.symbol = symbol
		self.visited = visited
		self.parent = parent

def goRight(point):
    return (point[0], point[1]+1)

def goLeft(point):
    return (point[0], point[1]-1)

def goUp(point):
    return (point[0]-1, point[1])

def goDown(point):
    return (point[0]+1, point[1])

def isFinish():
    return currentPoint == finishPoint

def obstacleCheck(point):
    return maze[point[1]][point[0]]

def setMaze(point, c):
    global strMaze
    strMaze[point[0]][point[1]] = c

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

#File Input
print("Pilih file maze-nya :")
path = "maze"
dirs = os.listdir(path)
i = 0
for file in dirs:
	i = i + 1
	print(str(i) + ". " + file)
print("0. Keluar")
pilihan = int(input("Pilih nomor berapa? "))

if(pilihan == 0):
	exit()

i = 1
fileName = ""
for file in dirs:
	if(i == pilihan):
		fileName = file
	i = i+1

if (fileName == ""):
	print("Pilihan tidak tersedia.")
	exit()

fileName = ("maze/"+fileName)

#Baca File
fileInput = open(fileName)
strMaze = fileInput.readlines()
fileInput.close()
nArr = []

maze = []
predList = []
queueMove = queue.Queue()

#Mindahin map
for i in range(len(strMaze)):
	strMaze[i] = strMaze[i].rstrip()
	nArr.append([])
	for j in range(len(strMaze[i])):
		nArr[i].append(Node(strMaze[i][j], False, None))

#Posisi Mulai
for i in range(len(strMaze)):
	if (strMaze[i][0] == '0'):
		srow = i
		scol = 0

#Posisi Akhir
for i in range(len(strMaze)):
	if (strMaze[i][len(strMaze[0])-1] == '0'):
		frow = i
		fcol = len(strMaze[0])-1

que = deque([])
currentPoint = (srow,scol)

doMoveRight()
#BFS Algorithm
while(True):
	#Cek atas
	if (strMaze[currentPoint[0] - 1][currentPoint[1]] == "0"):
		if(nArr[currentPoint[0] - 1][currentPoint[1]].visited == False):
			nArr[currentPoint[0] - 1][currentPoint[1]].visited = True
			nArr[currentPoint[0] - 1][currentPoint[1]].parent = (currentPoint[0], currentPoint[1])
			if(strMaze[currentPoint[0] - 1][currentPoint[1]] == strMaze[frow][fcol]):
				epos = (currentPoint[0]-1, currentPoint[1])
				break
			que.append((currentPoint[0]-1, currentPoint[1]))
	
	#Cek bawah
	if (strMaze[currentPoint[0] + 1][currentPoint[1]] == "0"):
		if(nArr[currentPoint[0] + 1][currentPoint[1]].visited == False):
			nArr[currentPoint[0] + 1][currentPoint[1]].visited = True
			nArr[currentPoint[0] + 1][currentPoint[1]].parent = (currentPoint[0], currentPoint[1])
			if(strMaze[currentPoint[0] + 1][currentPoint[1]] == strMaze[frow][fcol]):
				epos = (currentPoint[0]+1, currentPoint[1])
				break
			que.append((currentPoint[0]+1, currentPoint[1]))

	#Cek kiri
	if (strMaze[currentPoint[0]][currentPoint[1] - 1] == "0"):
		if(nArr[currentPoint[0]][currentPoint[1] - 1].visited == False):
			nArr[currentPoint[0]][currentPoint[1] - 1].visited = True
			nArr[currentPoint[0]][currentPoint[1] - 1].parent = (currentPoint[0], currentPoint[1])
			if(strMaze[currentPoint[0]][currentPoint[1] - 1] == strMaze[frow][fcol]):
				epos = (currentPoint[0], currentPoint[1]-1)
				break
			que.append((currentPoint[0], currentPoint[1]-1))

	#Cek kanan
	if (strMaze[currentPoint[0]][currentPoint[1] + 1] == "0"):
		if(nArr[currentPoint[0]][currentPoint[1] + 1].visited == False):
			nArr[currentPoint[0]][currentPoint[1] + 1].visited = True
			nArr[currentPoint[0]][currentPoint[1] + 1].parent = (currentPoint[0], currentPoint[1])
			if(strMaze[currentPoint[0]][currentPoint[1] + 1] == strMaze[frow][fcol]):
				epos = (currentPoint[0], currentPoint[1]+1)
				break
			que.append((currentPoint[0], currentPoint[1]+1))

	try:
		currentPoint = que.popleft()
	except IndexError:
		print("Maze ini tidak ada solusi")
		fail = True
		break

arr2 = []
for i in range(len(strMaze)):
	arr2.append([])
	arr2[i] = list(strMaze[i])

pos = epos
length = 0
while (True):
	pos = nArr[pos[0]][pos[1]].parent
	if (strMaze[pos[0]][pos[1]] == strMaze[srow][scol]):
		length = length+1
		break
	else:
		length = length + 1
		arr2[pos[0]][pos[1]] = "#"

for i in range(0,len(arr2[1])):
	sys.stdout.write('\n')
	sys.stdout.flush()
	for j in range(0,len(arr2[1])):
		if (arr2[i][j] == "1"):
			sys.stdout.write(Back.BLACK + " ")
			sys.stdout.flush()
		elif (arr2[i][j] == "#"):
			sys.stdout.write(Back.GREEN + " ")
			sys.stdout.flush()
		elif (arr2[i][j] == "0"):
			sys.stdout.write(Back.WHITE + " ")
			sys.stdout.flush()
		elif (arr2[i][j] == "s"):
			sys.stdout.write(Back.RED + " ")
			sys.stdout.flush()
		elif (arr2[i][j] == "e"):
			sys.stdout.write(Back.RED + " ")
			sys.stdout.flush()

