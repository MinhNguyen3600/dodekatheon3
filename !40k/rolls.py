#/gameOBJ/dicebox.py
 
import math # math.floor() rounds down; math.ceil() rounds up
from numpy import random as rand


# ------------------ RESERVED FOR FUTURE 40k IMPLEMNTATION -------------
# Definition for rolling wound rolls
def wRoll(
    totalSuccessRolls: int,
    weapStr: int,
    opponentTough: int
) -> list:
    
    #Initialize Dice Box
    wDiceBox = [i for i in range(totalSuccessRolls)]

    #Roll Dices into dice box
    for rollPos in range(totalSuccessRolls):
        currRoll = rand.randint(1, 7)
        wDiceBox[rollPos] = currRoll

    #Save roll results for player transparrency
    resWoundDiceBox = wDiceBox

    #determine success conditions
    if weapStr == opponentTough:
        successCond = 4
    elif weapStr > opponentTough:
        successCond = 3
    elif weapStr < opponentTough:
        successCond = 5
    elif weapStr < opponentTough and weapStr <= opponentTough/2:
        successCond = 6
    elif weapStr > opponentTough and weapStr >= opponentTough*2:
        successCond = 2

    print(f"Current Success Condition: {successCond}+")

    # Check for success & crit dices
    wSuccessCtr = 0
    wCritCtr = 0
    for rollPos in range(totalSuccessRolls):
        if wDiceBox[rollPos] >= successCond and not wDiceBox[rollPos] == 6:
            wSuccessCtr += 1
        elif wDiceBox[rollPos] >= successCond and wDiceBox[rollPos] == 6:
            wCritCtr += 1

    finalSuccessRolls = wSuccessCtr + wCritCtr

    return resWoundDiceBox, wSuccessCtr, wCritCtr, finalSuccessRolls, successCond
#-----------------------------------------------------------------------

def rollBox(rollNum: int):
    diceBox = [i for i in range(rollNum)]

    #Roll Dices into dice box
    for rollPos in range(rollNum):
        currRoll = rand.randint(1, 7)
        diceBox[rollPos] = currRoll 

    return diceBox

# Definition for rolling hit rolls
def hRoll(
    rollNum: int,
    bskill: int
):
    
    #Initialize Dice Box
    hDiceBox = [i for i in range(rollNum)]

    failedRolls = 0
    #Roll Dices into dice box
    for rollPos in range(rollNum):
        currRoll = rand.randint(1, 7)
        hDiceBox[rollPos] = currRoll
        if currRoll == 1:
            failedRolls += 1

    #Save hit roll results for player transparrency
    resHitDiceBox = hDiceBox

    # Check for success & crit dices
    hSuccessCtr = 0
    hCritCtr = 0
    for rollPos in range(rollNum):
        if hDiceBox[rollPos] >= bskill and not hDiceBox[rollPos] == 6:
            hSuccessCtr += 1
        elif hDiceBox[rollPos] >= bskill and hDiceBox[rollPos] == 6:
            hCritCtr += 1

    totalSuccessRolls = hSuccessCtr + hCritCtr

    # NOTE: totalSuccessRolls is required for Wound Rolls
    return resHitDiceBox, hSuccessCtr, hCritCtr, totalSuccessRolls, failedRolls

def saveRoll(
    svRoll: int
):
    # Number of Defense dices to do save rolls
    defDice = 3
    defDiceBox = [i for i in range(defDice)]


    # Roll the defense dices
    for rollPos in range(defDice):
        currRoll = rand.randint(1, 7)
        defDiceBox[rollPos] = currRoll

    #Save sv roll results for player transparrency
    saveDiceBox = defDiceBox

    svSuccessCtr = 0
    svCritCtr = 0
    failedSvs = 0
    for rollPos in range(defDice):
        if defDiceBox[rollPos] >= svRoll and defDiceBox[rollPos] !=6:
            svSuccessCtr += 1
        elif defDiceBox[rollPos] >= svRoll and defDiceBox[rollPos] ==6:
            svCritCtr += 1
        elif defDiceBox[rollPos] < svRoll or defDiceBox[rollPos] == 1:
            failedSvs += 1

    return saveDiceBox, svSuccessCtr, svCritCtr, failedSvs
    

