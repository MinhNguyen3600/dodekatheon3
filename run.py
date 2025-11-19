import os
import msvcrt
import pandas as pd
import numpy as np
from numpy import random

import army
import utils
import map.mapGen as mapGen

# -------- Initialize game data & condition -------- 
game = True
menu = True

initMap, initRow, initCol = mapGen.dfMatrix()
mapWTerrain = mapGen.killZone([initMap, initRow, initCol])

y_len = len(mapWTerrain)
x_len = len(mapWTerrain[0])

x = 0
y = y_len - 1

mapWTerrain[y][x] = "[P]"  # Place initial player

# -------- MENU -------- 
while menu:
    killTeams = army.ktLoader()
    
    utils.clear()
    utils.draw()
    print("SELECT YOUR KILL TEAM:")
    for kt in killTeams:
        print(kt)
    print("0. Exit Game")
    print("N. Load existing kill team list")
    utils.draw()

    choice = input(">>> ")
    if choice == "0":
        quit()
    elif choice == "N" or choice == "n":
        currentKT = "Angels of Death"
        operatorSelection = ["Space Marine Captain", "Elimnator Sniper", "Assault Intercessor Grenadier","Intercessor Gunner", "Intercessor Warrior", "Intercessor Warrior"]
        opData = army.ktDataLoader(currentKT, operatorSelection)

        utils.draw()
        input(f"You've chosen the [{currentKT}] Kill Team!")
    else:
        for chosen in range(len(killTeams)):
            chosenKT = killTeams[chosen]
            if choice == chosenKT[0]:
                currentKT = killTeams[chosen][3:]
        utils.draw()
        input(f"You've chosen the [{currentKT}] Kill Team!")

        utils.clear()
        dataLoad = army.ktDataLoader(currentKT)
        eligibleOps = army.legalOps(currentKT, dataLoad)
        operatorSelection = army.ktBuild(currentKT, eligibleOps[0], eligibleOps[1])
        opData = army.dataLoader(currentKT, operatorSelection)
    
    
    utils.clear()
    print(f"Player A started [{currentKT}] with the following army list:")
    for i in range(len(operatorSelection)):
        print(f"- {operatorSelection[i]}")
    
    utils.draw()
    input(">>> ")

    menu = False
    game = True


# -------- GAME -------- 
# CHANGE NOTES: 
#   1. Refactored, initial game loop is self-written based on Python RPGgame's bottom game loop
# This version is after feeding that written version to the GPT to fix update player piece
# placement & terrain blocking/interaction issue
#   2. Player piece "⬜" is replaced by "[P]"
while game:
    utils.clear()
    utils.draw()
    print(f"COORDINATES: \n  X: {x}\n  Y: {y}")
    utils.draw()

    # Single map print per loop (mapWTerrain must reflect current player pos)
    print(pd.DataFrame(mapWTerrain, index=initRow, columns=initCol).to_string())

    print("0. QUIT GAME")
    print("1. MOVE")

    utils.draw()

    dest = input(">>> ")

    if dest == "0":
        game = False
        break

    if dest == "1":
        maxDist = 6
        while True:
            utils.draw()
            print(f"Select a tile you wish to move (1 - {maxDist}")
            utils.draw()
            
            # Grok suggests putting it inside try-except 
            try: 
                rad = int(input(">>> "))
                if rad < 1 or rad > maxDist:
                    print("Too far! Please try again")
                    continue
                break
            except ValueError:
                print("MUST BE A NUMBER! TRY AGAIN.")
                continue

        # clear any previous temporary markers "[ ]"
        utils.stripper(x_len, y_len, mapWTerrain)

        legalMove = mapGen.drawRadius(x, y, rad, mapWTerrain)

        print(pd.DataFrame(mapWTerrain, index=initRow, columns=initCol).to_string())
        utils.draw()
        print(f"You've chosen to move to {rad}. Please select the tile you wish to move to.")
        utils.draw()
        dist = input(">>> ").upper()

        
        targetCol = " " + dist[0] + " " # to mach initCol format with spaces 
        targetRow = dist[1:]

        #Grok suggests putting these in try-except again, but targetX & targetY each get thrown one
        try:
            targetX = initCol.index(targetCol)
        except ValueError:
            print("Invalid column!")
            input(">>> ")
            utils.stripper(x_len, y_len, mapWTerrain)
            continue

        try:
            targetY = initRow.index(targetRow)
        except ValueError:
            print("Invalid row!")
            input(">>> ")
            utils.stripper(x_len, y_len, mapWTerrain)
            continue

        if (targetX, targetY) not in legalMove:
            print("That tile is not reachable this move.")
            input("Press Enter...")
            utils.stripper(x_len, y_len, mapWTerrain)
            continue

        newX, newY = targetX, targetY

    # Bounds check
    if not (0 <= newX < x_len and 0 <= newY < y_len):
        print("Blocked by terrain!")
        input("Press Enter...")
        utils.stripper(x_len, y_len, mapWTerrain)
        continue

    # Collision check 
    dest_cell = mapWTerrain[newY][newX].strip()
    if dest_cell in ("|", "-"):
        # blocked by terrain
        print("Blocked by terrain!")
        input("Press Enter...")
        utils.stripper(x_len, y_len, mapWTerrain)
        continue

    # Move is valid: clear previous pos, update coordinates, place player marker
    mapWTerrain[y][x] = "   "    # clear old
    utils.stripper(x_len, y_len, mapWTerrain)

    x, y = newX, newY           # commit movetar
    mapWTerrain[y][x] = "[P]"     # place marker

    utils.clear()
    print(pd.DataFrame(mapWTerrain, index=initRow, columns=initCol).to_string())    
    input("Move complete. Press Enter to continue...")
    


    