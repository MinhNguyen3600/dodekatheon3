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



def opLoadoutScreen(operatorSelection: list, currentKT: str):
    loadouts = {}
    selectedData = army.getOpData(currentKT, operatorSelection)  # Get full operative data

    for operative in selectedData:
        opName = operative["Op Name"]
        weapons = operative["Weapon Options"]
        loadout = []

        #Auto add default (fixed) weapon opt
        if "Fixed" in weapons:
            for actionType in weapons["Fixed"]:
                for name, details in weapons["Fixed"][actionType].items():

                    #Create a seperate copy of "weapon" dictionary inside the "fixed" dictionary
                    weapon = details.copy()  
                    
                    #load weapon details
                    weapon["name"] = name
                    weapon["Action Type"] = actionType
                    loadout.append(weapon) #add weapon dicts (from fixed dict) into loadout weapon list
  
        #Hard Selection (user input)
        if "Hard Selection" in weapons:
            for actionType in ["Shoot", "Melee"]:
                if actionType in weapons ["Hard Selection"]:
                    options = weapons["Hard Selection"][actionType]

                    # empty hard selection list skips this option
                    if len(options) == 0: 
                        continue    

                    # only 1 hard selection results in it being the default selection
                    elif len(options) == 1: 
                        #next() loops through the iter() function which loops through each name-detail keypair inside options list using .items()
                        name, details = next(iter(options.items())) 

                        weapon = details.copy() 
                        
                        #load weapon details
                        weapon["name"] = name
                        weapon["Action Type"] = actionType
                        loadout.append(weapon)

                    # for lists with multiple Hard Selection options, prompts user input
                    else: 
                        utils.clear()
                        print(f"Select {actionType} weapon for {opName} (Hard Selection):")

                        #prints a list of all selectable weap options
                        #takes the weapon names in the options list, get its index, then loop through the entire list 
                        for i, name in enumerate(options, 1):
                            print(f"{i}. {name}")
                        
                        while True:
                            choice = int(input(">>> ")) - 1 #reduce for index starts at 0
                            if isinstance(choice, int):
                                if 0 <= choice < len(options): #ensure answer stays within limit

                                    # 1. Find if the player's selected weapon name (which is the key dict) is inside options dict list
                                    # 2. Loads selected name of weap in
                                    # 3. loads its details in via the selectedName key from the details dict
                                    selectedName = list(options.keys())[choice]
                                    details = options[selectedName]
                                    
                                    # 4. Create a copy of the details dict as the weapon dict, same loop as other options
                                    weapon = details.copy()

                                    #load weapon details
                                    weapon["name"] = name
                                    weapon["Action Type"] = actionType
                                    loadout.append(weapon)
                                    
                                    break #exit the "while True" loop
                                else:
                                    print("Invalid choice!")
                            else:
                                print("Incorrect input! Please input a number!")
                        
        # Free Selection is added by default:
        if "Free Selection" in weapons:
            for actionType in weapons["Free Selection"]:
                for name, details in weapons["Free Selection"][actionType].items():
                    weapon = details.copy()

                    #load weapon details
                    weapon["name"] = name
                    weapon["Action Type"] = actionType
                    loadout.append(weapon)

        loadouts[opName] = loadout
        print(f"Loadout for {opName} completed! Selected loadout:")
        for i, name in enumerate(loadout, 1):
            print(f"{i}. {name}")
        input(">>> ")

    return loadouts

def armyDisplayScreen(currentKT: str, operatorSelection: list):
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

