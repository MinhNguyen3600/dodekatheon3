#
# Initiallly developed inside the "while menu" loop in run.py, seperated its definition over here for 
# clarity & future class creation

import army
import utils


def ktSelectScreen():
    killTeams = army.ktLoader()
    
    while True:
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
            loaded = True
            break
        else:
            for chosen in range(len(killTeams)):
                chosenKT = killTeams[chosen]
                if choice == chosenKT[0]:
                    currentKT = killTeams[chosen][3:]
                    loaded = False
                    break
            else:
                print("Invalid choice! Please try again.")
                input("Press Enter...")
                continue  # Retry

    utils.draw()
    input(f"You've chosen the [{currentKT}] Kill Team!")

    return currentKT, loaded

def opSelectScreen(currentKT: str, loaded: bool):
    if loaded:
        operatorSelection = ["Space Marine Captain", "Elimnator Sniper", "Assault Intercessor Grenadier","Intercessor Gunner", "Intercessor Warrior", "Intercessor Warrior"]
    
    else:
        utils.clear()
        dataLoad = army.dataLoader(currentKT)
        eligibleOps = army.legalOps(currentKT, dataLoad)
        operatorSelection = army.ktBuild(currentKT, eligibleOps[0], eligibleOps[1])
        
    return operatorSelection

def opLoadoutScreen(operatorSelection: list):
    print("Operative Loadout Selection Screen - Not Implemented Yet")
    input("Press Enter to continue...")
    return operatorSelection

def armyDisplayScreen(currentKT: str, operatorSelection: list):
    opData = army.ktDataLoader(currentKT, operatorSelection)

    utils.clear()
    print(f"Player A started [{currentKT}] with the following army list:")
    for i, op in enumerate(operatorSelection, 1):
        print(f"{i}. {op}")
    
    utils.draw()
    print("Your Operatives' Datasheets: ")
    army.opDatasheet(opData)

    utils.draw()
    input(">>> ")

