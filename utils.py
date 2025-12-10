import os

# --------- Utilities ----------
def draw():
    print("Xx----------------------xX")

def clear():
    os.system("cls")

def stripper(xLen: int, yLen: int, mapWTerrain: list):
    for ry in range(yLen):
        for rx in range(xLen):
            if mapWTerrain[ry][rx].strip() == "[ ]":
                mapWTerrain[ry][rx] = "   "

def nameToKey(name: str):
    keyName = name.replace(" ", "-").lower()
    return keyName

def keyToName(keyword: str):
    nameName = keyword.replace("-", " ").title()
    return nameName