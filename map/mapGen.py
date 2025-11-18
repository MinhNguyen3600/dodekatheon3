import pandas as pd
import numpy as np
from numpy import random

# playerA = ["◇", "◆"]
# playerB = ["□", "■"]

# playerPieceList = ["◇", "□", "◆", "■"]
# terrainPieceList = ["⬜", "█", ""]


def dfMatrix():
    withinLimit = True
    alphabet =  "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    colLim = 21 # not size of alphabet, Dataframe only displays up to 23 characters before cutting the middle section
    rowLim = 16

    # RowChoice = input("Row num: ")
    # ColumnChoice= input("Column num: ")

    ColumnChoice = "21"
    RowChoice = "15"

    mtxCol = [] # Column NAME list | Internal | Multiple | Multiple Values
    mtxRow = [] # Row NAME list | External | Singular | Multiple Values
    dataList = [] # list as data frame 

    while withinLimit:
            
        if int(ColumnChoice) > colLim or int(RowChoice) > rowLim:
            print(f"Map/Board size exceeds limit! Please keep Column size WITHIN {colLim} and row size WITHIN {rowLim}")
            withinLimit = False
        else:
            # Create a list of rows and column NAMES
            for rownum in range(int(RowChoice)):
                mtxRow.append(str(rownum + 1)) 

            for colnum in range(int(ColumnChoice)):
                colStr = " " + alphabet[colnum] + " "
                mtxCol.append(colStr)

            # print(mtxCol)
            # print(mtxRow)

            # Create actual 2D data list
            for rLabel in mtxRow:
                row = [] # temp 2D row to build dataframe (DO NOT LEAVE THIS OUTSIDE)
                for cLabel in mtxCol:
                    row.append("   ")   # build x-axis

                dataList.append(row)   # build y-axis

            # # Turn 2D data list into a data frame
            # Redundant as function returns all 3 data
            # KEEP IN MIND TO REUSE IT DO NOT DELETE
            # df = pd.DataFrame(data, index=mtxRow, columns=mtxCol)

            # res = [df, data]
            withinLimit = False
            return(dataList, mtxRow, mtxCol)

def killZone(dataList: list):
    currMap = dataList[0]
    currMapRow = dataList[1]
    currMapCol = dataList[2]

    vertTerrainPos = {
        (5, 5): " | ",
        (5, 6): " | ",
        (10, 10): " - ",
        (11, 10): " - "
    }

    # oh wow, so you can define both x, y positions as the key in the dict,
    # then you can add it here as the row & columnn IDs; the terrain then
    # becomes the value, which you could also parse into the condition loop, 
    for (rowID, colID), terrain in vertTerrainPos.items():
        if 0 <= rowID < len(currMap) and 0 <= colID <len (currMap[0]):
            currMap[rowID][colID] = terrain
        else:
            print(f"[DEBUG] Warning: Position ({rowID}, {colID}) out of bounds.")

    return currMap

# Calc the distance between 2 objects based on their x,y pos on the board 
# Using EUCLID'S DISTANCE FORMULA: [d = √[(x2 – x1)2 + (y2 – y1)2]]
def distIn(p1: list, p2: list):
    dx = abs(p1[0] - p2[0])
    dy = abs(p1[1] - p2[1])
    return ((dx ** 2) + (dy ** 2)) ** 0.5

# Legend:
#   - currX: current player's x-position on the board
#   - currY: current player's y-position on the board
#   - radius: current player's eligible move distance on the board

def drawRadius(currX: int, currY: int, radius: int, mapData: list):
    
    rowLen = len(mapData)
    colLen = len(mapData[0])
    # threshold = 0.5
    legalMove = []
    for y in range(rowLen):
        for x in range(colLen):
            distance = distIn((currX, currY), (x, y))
            if distance <= radius:
                if mapData[y][x].strip() == "":
                    mapData[y][x] = "[ ]"
                    legalMove.append((x,y)) 
    return legalMove
            


def printCircle(mapData: list, rowLabel, colLabel):
    # header
    header = "   " + "".join(f"{c:>3}" for c in colLabel)
    print(header)
    print()
    for i, row in enumerate(mapData):
        print(f"{rowLabel[i]:>2}" + "".join(row))


# currMapData, currMapRow, currMapCol = dfMatrix()

# currX = 10
# currY = 7

# radius = int(input(">>> "))

# drawRad = drawRadius(currX, currY, radius, currMapData)
# printCircle(currMapData, currMapRow, currMapCol)
# print(drawRad)

# --------- Tests before implementation --------- 
# listSth = [[1, 2, 3],[4, 5, 6],[7,8,9]]
# n = len(listSth)
# # for integer in range(len(listSth)):
# if n % 2 == 1:
#     centerNum = n // 2
#     centerRow = listSth[centerNum]
#     centerVal = centerRow[centerNum]
#     if listSth[centerNum] in listSth and listSth[centerNum][centerNum]:
#         print(f"The center of the row list is {centerRow} at position {centerNum}")
#         print(f"The center of the column list is {centerVal} at position [{centerNum}][{centerNum}]")
# ---------  ---------  ---------  ---------  --------- 

# --------- Miscelaneous Tests --------- 
# df = pd.DataFrame(dfMatrix()[0], index = dfMatrix()[1], columns = dfMatrix()[2])

# initMap = dfMatrix()
# mapWTerrain = killZone(initMap)
# df = pd.DataFrame(mapWTerrain, index = initMap[1], columns = initMap[2])

# print(df)
