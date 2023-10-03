import numpy as np
import random
import sys

#%%
def makeSpecificGrid():
    grid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
                grid[xx][yy] = np.random.randint(1,5)
    grid[9][8] = 5
    grid[8][9] = -5
    for yy in range(2,8):
        grid[0][yy] = 0
        grid[1][yy] = 0
        grid[2][yy] = 0
        grid[3][yy] = 0
        grid[4][yy] = 0
        grid[5][yy] = 0
        grid[6][yy] = 0
    for xx in range(0,2):
        grid[xx][0] = 0
        grid[xx][1] = 0
        grid[xx][8] = 0
        grid[xx][9] = 0
    grid[2][0] = 3 
    grid[9][9] = 0
    print(grid)
    return grid

grid = makeSpecificGrid()

#%%

def aStarSearch(grid):
    heuristicGrid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
            heuristicGrid[xx][yy] = 10*(xx+yy)
            
    for yy in range(2,8):
        heuristicGrid[0][yy] = -10
        heuristicGrid[1][yy] = -10
        heuristicGrid[2][yy] = -10
        heuristicGrid[3][yy] = -10
        heuristicGrid[4][yy] = -10
        heuristicGrid[5][yy] = -10
        heuristicGrid[6][yy] = -10
    for xx in range(0,2):
        heuristicGrid[xx][0] = -10
        heuristicGrid[xx][1] = -10
        heuristicGrid[xx][8] = -10
        heuristicGrid[xx][9] = -10
    for i in range(0,9):
        heuristicGrid[i][i] = 20
        
           
    #heuristicGrid = np.transpose(heuristicGrid)
    #heuristicGrid = np.flip(heuristicGrid)
    heuristicGrid[2][0] = 100
    print(heuristicGrid)
    #print(heuristicGrid)
    bestForPosition = np.zeros((10,10),dtype=np.int16)
    # for yy in range(2,8):
    #     bestForPosition[0][yy] = -10
    #     bestForPosition[1][yy] = -10
    #     bestForPosition[2][yy] = -10
    #     bestForPosition[3][yy] = -10
    #     bestForPosition[4][yy] = -10
    #     bestForPosition[5][yy] = -10
    #     bestForPosition[6][yy] = -10
    # for xx in range(0,2):
    #     bestForPosition[xx][0] = -10
    #     bestForPosition[xx][1] = -10
    #     bestForPosition[xx][8] = -10
    #     bestForPosition[xx][9] = -10
    
    #print(bestForPosition)
    #visitedList = {}
    #visitedList[(9,9)] = heuristicGrid[9,9]
    currentlyActiveList = []
    currentPosition = (9,9)
    currentlyActiveList.append( (currentPosition,heuristicGrid[9][9]) ) # coordinates, a* value
    temp = 0
    ## find max values
    while currentlyActiveList:
        temp += 1
        currentlyActiveList = \
            [(coords, score) for (coords, score) in currentlyActiveList if coords != currentPosition]

        if currentPosition[0]>0:
            possPosition1x = currentPosition[0]-1
            possPosition1y = currentPosition[1]
            aStarScore1 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                +grid[possPosition1x][possPosition1y] \
                +heuristicGrid[possPosition1x][possPosition1y]
            currentlyActiveList.append( ((possPosition1x, possPosition1y), aStarScore1))
            bestForPosition[possPosition1x][possPosition1y] =\
                max( bestForPosition[currentPosition[0]][currentPosition[1]]
                      + grid[possPosition1x][possPosition1y],\
                  bestForPosition[possPosition1x][possPosition1y])

        if currentPosition[1]>0:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]-1
            aStarScore2 = bestForPosition[currentPosition[0]][currentPosition[1]] \
                +grid[possPosition2x][possPosition2y] \
                +heuristicGrid[possPosition2x][possPosition2y]
            currentlyActiveList.append( ((possPosition2x, possPosition2y), aStarScore2))
            bestForPosition[possPosition2x][possPosition2y] =\
                max( bestForPosition[currentPosition[0]][currentPosition[1]]
                      + grid[possPosition2x][possPosition2y],\
                  bestForPosition[possPosition2x][possPosition2y])

        sorted_by_second = currentlyActiveList.sort(key=lambda tuple: tuple[1], reverse=True)
        #print("currently active: ",currentlyActiveList)
        if not currentlyActiveList:
            break
        currentPosition = currentlyActiveList[0][0]
        #print(currentPosition)
        #print(grid)
        #print(bestForPosition)
        #input()
    ## construct best path
    #print(bestForPosition)
    pathGrid = np.zeros( (10,10), dtype=np.int8) #just for illustration
    path = []
    currentPosition = (9,9)
    path.append( (9,9) )
    pathGrid[9][9] = True
    while currentPosition != (0,0):

        if currentPosition[0] > 0:
            possPosition1x = currentPosition[0]-1
            possPosition1y = currentPosition[1]
            pos1 = True
        if currentPosition[1] > 0:
            possPosition2x = currentPosition[0]
            possPosition2y = currentPosition[1]-1
            pos2 = True
        pos1Bigger = bestForPosition[possPosition1x][possPosition1y]>\
            bestForPosition[possPosition2x][possPosition2y]
        if (pos1 and not pos2) or (pos1 and pos2 and pos1Bigger):
            path.append( (possPosition1x,possPosition1y) )
            pathGrid[possPosition1x][possPosition1y] = 1
            currentPosition = (possPosition1x,possPosition1y)
        if (pos2 and not pos1) or (pos1 and pos2 and not pos1Bigger):
            path.append( (possPosition2x,possPosition2y) )
            pathGrid[possPosition2x][possPosition2y] = 1
            currentPosition = (possPosition2x,possPosition2y)
        if len(path) >= 20:
            break

    print(grid)
    print(path)
    print(np.transpose(pathGrid))
    return path

def aStar2(grid):
    heuristicGrid = np.zeros((10,10),dtype=np.int16)
    for xx in range(10):
        for yy in range(10):
            heuristicGrid[xx][yy] = 10 
    for yy in range(2,8):
        heuristicGrid[0][yy] = 0
        heuristicGrid[1][yy] = 0
        heuristicGrid[2][yy] = 0
        heuristicGrid[3][yy] = 0
        heuristicGrid[4][yy] = 0
        heuristicGrid[5][yy] = 0
        heuristicGrid[6][yy] = 0
    for xx in range(0,2):
        heuristicGrid[xx][0] = 0
        heuristicGrid[xx][1] = 0
        heuristicGrid[xx][8] = 0
        heuristicGrid[xx][9] = 0
            
    print(heuristicGrid)
    
    bestForPosition = np.zeros((10,10),dtype=np.int16)
    #visitedList = {}
    #visitedList[(9,9)] = heuristicGrid[9,9]
    currentlyActiveList = []
    start = [np.random.randint(1,10),np.random.randint(1,10)]
    currentPosition = (start[0],start[1])
    currentlyActiveList.append( (currentPosition,heuristicGrid[9][9]) ) # coordinates, a* value
    temp = 0
    ## find max values
    while len(currentlyActiveList) != 20:
        temp += 1
        currentlyActiveList = [(coords, score) for (coords, score) in currentlyActiveList if coords != currentPosition]

        if currentPosition[0] > 0:
            choice = np.random.randint(1,3)
            if choice == 1:
                possPosition1x = currentPosition[0] - 1
                possPosition1y = currentPosition[1]
                aStarScore1 = bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition1x][possPosition1y] + heuristicGrid[possPosition1x][possPosition1y]
                currentlyActiveList.append( ((possPosition1x, possPosition1y), aStarScore1))
                bestForPosition[possPosition1x][possPosition1y] =  max( bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition1x][possPosition1y], bestForPosition[possPosition1x][possPosition1y])
            if choice == 2:
                possPosition1x = currentPosition[0] + 1
                if possPosition1x >= 10:
                    possPosition1x = 9
                possPosition1y = currentPosition[1]
                aStarScore1 = bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition1x][possPosition1y] + heuristicGrid[possPosition1x][possPosition1y]
                currentlyActiveList.append( ((possPosition1x, possPosition1y), aStarScore1))
                bestForPosition[possPosition1x][possPosition1y] =  max( bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition1x][possPosition1y], bestForPosition[possPosition1x][possPosition1y])
                
        if currentPosition[1] > 5:
            choice = np.random.randint(1,3)
            if choice == 1:
                possPosition2x = currentPosition[0]
                possPosition2y = currentPosition[1] - 1
                aStarScore2 = bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition2x][possPosition2y] + heuristicGrid[possPosition2x][possPosition2y]
                currentlyActiveList.append( ((possPosition2x, possPosition2y), aStarScore2))
                bestForPosition[possPosition2x][possPosition2y] = max( bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition2x][possPosition2y], bestForPosition[possPosition2x][possPosition2y])
            if choice == 2:
                possPosition2x = currentPosition[0]
                possPosition2y = currentPosition[1] + 1
                if possPosition2y >= 10: 
                    possPosition2y = 9
                aStarScore2 = bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition2x][possPosition2y] + heuristicGrid[possPosition2x][possPosition2y]
                currentlyActiveList.append( ((possPosition2x, possPosition2y), aStarScore2))
                bestForPosition[possPosition2x][possPosition2y] = max( bestForPosition[currentPosition[0]][currentPosition[1]] + grid[possPosition2x][possPosition2y], bestForPosition[possPosition2x][possPosition2y])

        sorted_by_second = currentlyActiveList.sort(key=lambda tuple: tuple[1], reverse=True)
        #print("currently active: ",currentlyActiveList)
        if not currentlyActiveList:
            break
        currentPosition = currentlyActiveList[0][0]
        #print(currentPosition)
        #print(grid)
        #print(bestForPosition)
        #input()

    ## construct best path
        #print(bestForPosition)
        pathGrid = np.zeros( (10,10), dtype=np.int8) #just for illustration
        path = []
        currentPosition = currentPosition
        path.append( (currentPosition) )
        #pathGrid[9][9] = True

        while currentPosition[0] != (0,0):
            if currentPosition[0] > 0:
                possPosition1x1 = currentPosition[0] - 1
                possPosition1x2 = currentPosition[0] + 1
                possPosition1y = currentPosition[1]
                if possPosition1x2 >= 10:
                    possPosition1x2 = 9
                
            if bestForPosition[possPosition1x1][possPosition1y] > bestForPosition[possPosition1x2][possPosition1y]:
                possPosition1x = possPosition1x1
                
            elif bestForPosition[possPosition1x1][possPosition1y] < bestForPosition[possPosition1x2][possPosition1y]:
                possPosition1x = possPosition1x2
    
            if possPosition1x != None:
                pos1 = True
                print("pos1 = ", pos1, "Position1x = ", possPosition1x)
                
            if currentPosition[1] > 5 and pos1 == True:
                possPosition2x = currentPosition[0]
                possPosition2y1 = currentPosition[1] - 1
                possPosition2y2 = currentPosition[1] + 1
                if possPosition2y2 >= 10:
                    possPosition2y2 = 9
                    
            if bestForPosition[possPosition2x][possPosition2y1] > bestForPosition[possPosition2x][possPosition2y2]:
                possPosition2y = possPosition2y1

            elif bestForPosition[possPosition2x][possPosition2y1] < bestForPosition[possPosition2x][possPosition2y2]:
                possPosition2y = possPosition2y2

            if possPosition2y != None:
                pos2 = True
                print("pos2 = ", pos2, "Position2y = ", possPosition2y)

    
            pos1Bigger = bestForPosition[possPosition1x][possPosition1y] > bestForPosition[possPosition2x][possPosition2y]
            
            if (pos1 and not pos2) or (pos1 and pos2 and pos1Bigger):
                path.append( (possPosition1x,possPosition1y) )
                pathGrid[possPosition1x][possPosition1y] = 1
                currentPosition = (possPosition1x,possPosition1y)
            if (pos2 and not pos1) or (pos1 and pos2 and not pos1Bigger):
                path.append( (possPosition2x,possPosition2y) )
                pathGrid[possPosition2x][possPosition2y] = 1
                currentPosition = (possPosition2x,possPosition2y)
            
        print(grid)
        print(path)
        print(pathGrid)
        return(path)

