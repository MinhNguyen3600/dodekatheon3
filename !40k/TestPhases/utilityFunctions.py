"""
Utility functions for dice rolling, parsing, and data loading
"""
import re


def rollD6() -> int:
    """Roll a single D6"""
    import rolls
    return rolls.rollBox(1)[0]


def rollD3() -> int:
    """Roll a D3"""
    d6Result = rollD6()
    if d6Result in [1, 2]:
        return 1
    elif d6Result in [3, 4]:
        return 2
    else:
        return 3


def parseDiceNotation(value) -> int:
    """Parse dice notation and return the result"""
    if isinstance(value, int):
        return value
    
    valueStr = str(value).upper().replace(" ", "")
    pattern = r'^(\d*)D([36])([+\-]\d+)?$'
    match = re.match(pattern, valueStr)
    
    if not match:
        try:
            return int(value)
        except:
            print(f"Warning: Could not parse '{value}', defaulting to 1")
            return 1
    
    numDice = int(match.group(1)) if match.group(1) else 1
    diceType = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    total = 0
    rollResults = []
    
    if diceType == 6:
        for _ in range(numDice):
            roll = rollD6()
            rollResults.append(roll)
            total += roll
    elif diceType == 3:
        for _ in range(numDice):
            roll = rollD3()
            rollResults.append(roll)
            total += roll
    
    finalTotal = total + modifier
    
    diceNotation = f"{numDice if numDice > 1 else ''}D{diceType}"
    if modifier > 0:
        diceNotation += f"+{modifier}"
    elif modifier < 0:
        diceNotation += f"{modifier}"
    
    print(f"Rolling {diceNotation}: {rollResults} = {total}", end="")
    if modifier != 0:
        print(f" {'+' if modifier > 0 else ''}{modifier} = {finalTotal}")
    else:
        print()
    
    return max(1, finalTotal)


def dataLoad(controlUnit: dict, targetUnit: dict):
    """Extract unit data from unit dictionaries"""
    cuName = controlUnit["Name"]
    cuPiece = controlUnit["Piece"]
    cuProfile = controlUnit["Profile"]
    cuWeapons = controlUnit["Weapons"]
    cuCount = controlUnit["Model Count"]
    cuKeywords = controlUnit["Keyword"]

    tuName = targetUnit["Name"]
    tuPiece = targetUnit["Piece"]
    tuProfile = targetUnit["Profile"]
    tuWeapons = targetUnit["Weapons"]
    tuCount = targetUnit["Model Count"]
    tuKeywords = targetUnit["Keyword"]

    return cuName, cuPiece, cuProfile, cuWeapons, cuCount, cuKeywords, tuName, tuPiece, tuProfile, tuWeapons, tuCount, tuKeywords