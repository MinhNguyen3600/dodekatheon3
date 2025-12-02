#
# Initiallly developed inside the "while menu" loop in run.py, seperated its definition over here for 
# clarity & future class creation

import army
import utils



def ktSelectScreen():
    # killTeams and ktNames are essentially the same lists
    # kts loaded via ktLoader are the same, the only difference is:
    # - the first element of ktLoader returns a numbered list, with a numbered "{number}. {ktName}"
    # - the second element of the ktloader returns the same lists, with the same positions, but only the ktNames
    killTeams = army.ktLoader()[0]
    ktNames = army.ktLoader()[1]
    
    while True:
        # utils.clear()
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
                    currentKT = utils.nameToKey(ktNames[chosen])
                    print(currentKT)
                    loaded = False
                    break

                else:
                    print("Invalid choice! Please try again.")
                    input("Press Enter...")
                    continue  # Retry
            break
    utils.draw()
    input(f"You've chosen the [{currentKT}] Kill Team!")

    return currentKT, loaded


def opSelectScreen(
    currentKT: str, 
    loaded: bool
) -> list[str]:
    if loaded is True:
        operatorSelection = ["Space Marine Captain", "Elimnator Sniper", "Assault Intercessor Grenadier","Intercessor Gunner", "Intercessor Warrior", "Intercessor Warrior"]
    
    elif loaded is False:
        utils.clear()
        dataLoad = army.opDataLoader(currentKT)
        operatorSelection = army.ktBuild(currentKT, dataLoad)
        
    else:
        print("Error loading ktData: army.opSelectScreen()-related error")
    return operatorSelection

# handwritten code
# simplification provided by gpt
def getWeaponData(
    currKT: str,
    weaponType: str, 
    weaponNameRef: str,
) -> dict:
    ktData = army.opDataLoader(currKT)
    weaponDict = ktData.get("weapons",{})
    typeDict = weaponDict.get(weaponType, {})
    return typeDict.get(weaponNameRef)
        
# GenAI
# -> Later heavily modified by me after data/datasheet.json restructure
def opLoadoutScreen(
    currentKT: str,
    selectedData: list
) -> dict: # returns a list of weapon dictionaries
    ktData = army.opDataLoader(currentKT)
    loadouts = {}

    for operative in selectedData:
        opSelectName = operative["op-name"]
        realOpName = opSelectName.replace(" ", "-").lower()
        opName = ktData["operatives"][realOpName]["op-name"]
        weapons = ktData["operatives"][realOpName]["weapon-opts"]
        loadout = []

        #Auto add default (fixed) weapon opt
        if "fixed" in weapons:
            for actionType in list(weapons["fixed"].keys()):
                for weaponRef in weapons["fixed"][actionType]:
                    currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
                    #Create a seperate copy of "weapon" dictionary inside the "fixed" dictionary
                    weapon = currWeaponData.copy()  
                    if not currWeaponData:
                        print(f"Warning: weapon [{weaponRef}] not found for {opName} (fixed)")
                        continue
                    loadout.append(weapon) #add weapon dicts (from fixed dict) into loadout weapon list
  
        #Hard Selection (user input)
        if "hard-selection" in weapons:
            for actionType in ["shoot", "melee"]:
                if actionType in weapons["hard-selection"]:
                    options = weapons["hard-selection"][actionType] # options is a List

                    # empty hard selection list skips this option
                    if len(options) == 0: 
                        continue    

                    # only 1 hard selection results in it being the default selection
                    # modified by hand
                    # fix provided by gpt
                    elif len(options) == 1: 
                        #next() loops through the iter() function which loops through each name-detail keypair inside options list using .items()
                        selectedName = options[0]
                        currWeaponData = getWeaponData(currentKT, actionType, selectedName)
                        if currWeaponData:
                            loadout.append(currWeaponData.copy())
                        else:
                            #load weapon details
                            print(f"Warning: weapon [{selectedName}] not found for {opName}")

                    # for lists with multiple Hard Selection options, prompts user input
                    else: 
                        utils.clear()
                        print(f"Select {actionType} weapon for {realOpName} (Hard Selection):")

                        #prints a list of all selectable weap options
                        #takes the weapon names in the options list, get its index, then loop through the entire list 
                        for i, name in enumerate(options, 1):
                            displayName = name.replace("-", " ").title()
                            print(f"{i}. {displayName}")
                        
                        while True:
                            choice = int(input(">>> ")) - 1 #reduce for index starts at 0
                            if isinstance(choice, int):
                                if 0 <= choice < len(options): #ensure answer stays within limit

                                    # 1. Find if the player's selected weapon name (which is the key dict) is inside options dict list
                                    # 2. Loads selected name of weap in
                                    # 3. loads its details in via the selectedName key from the details dict
                                    selectedName = list(options)[choice]
                                    currWeaponData = getWeaponData(currentKT, actionType, selectedName)
                                    if not currWeaponData:
                                        print(f"Warning: weapon [{selectedName}] not found for {opName}")
                                        break
                                    # 4. Create a copy of the details dict as the weapon dict, same loop as other options
                                    weapon = currWeaponData.copy()

                                    #load weapon details
                                    loadout.append(weapon)
                                    
                                    break #exit the "while True" loop
                                else:
                                    print("Invalid choice!")
                            else:
                                print("Incorrect input! Please input a number!")
                        
        # Free Selection is added by default:
        if "free-selection" in weapons:
            for actionType in list(weapons["free-selection"].keys()):
                for weaponRef in weapons["free-selection"][actionType]:
                    currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
                    if not currWeaponData:
                        print(f"Warning: weapon [{weaponRef}] not found for {opName} (free-selection)")
                        continue
                    weapon = currWeaponData.copy()

                    #load weapon details
                    loadout.append(weapon)

        loadouts[realOpName] = loadout
        loadouts[opName] = loadout

        print(f"Loadout for [{opName}] completed! Selected loadout:")
        for i, loadoutDetail in enumerate(loadout, 1):
            print(f"{i}. {loadoutDetail['weapon-name']}")
        input(">>> ")

    return loadouts

def armyDisplayScreen(
        currentKT: str, 
        operatorSelection: list
):
    # if operatorSelection already finalized
    if operatorSelection and isinstance(operatorSelection[0], dict):
        opData = operatorSelection
        # build a list of printable names for display
        for op in opData:
            opName = op.get("Op Name", str(op)) 
    else:
        loadoutData = opLoadoutScreen(operatorSelection, currentKT)
        opData = army.finalizeOp(currentKT, operatorSelection, loadoutData)
        opName = operatorSelection

    utils.clear()
    print(f"Player A started [{currentKT}] with the following army list:")
    for i, op in enumerate(opName, 1):
        print(f"{i}. {op}")
    
    utils.draw()
    print("Your Operatives' Datasheets: ")
    army.opDatasheet(opData)

    utils.draw()
    input(">>> ")

# for info in ktSelectScreen():
#     print(info)