#/menu.py
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
        print("M. Pick from pre-existing list of killteam operatives")
        utils.draw()

        choice = input(">>> ").lower()
        if choice == "0":
            quit()
        elif choice == "N" or choice == "n":
            currentKT = "Angels of Death"
            chosenVal = "n"
            loaded = True
            break
        elif choice == "m":
            currentKT = "Angels of Death"
            chosenVal = "m"
            loaded = True
            break
        else:
            for chosen in range(len(killTeams)):
                chosenKT = killTeams[chosen]
                if choice == chosenKT[0]:
                    currentKT = utils.nameToKey(ktNames[chosen])
                    print(currentKT)
                    chosenVal = None  # ✓ Initialize this!
                    loaded = False
                    break

                else:
                    print("Invalid choice! Please try again.")
                    input("Press Enter...")
                    continue  # Retry

    utils.draw()
    input(f"You've chosen the [{currentKT}] Kill Team!")

    return currentKT, loaded, chosenVal


def opSelectScreen(
    currentKT: str, 
    loaded: bool,
    chosenVal: str
) -> list[str]:
    if loaded is True and chosenVal == "n":
        operatorSelection = ["Space Marine Captain", "Intercessor Warrior", "Intercessor Warrior", "Elimnator Sniper", "Assault Intercessor Grenadier","Intercessor Gunner"]
    
    elif loaded is True and chosenVal == "m":
        opSelect = [
            ["Space Marine Captain", "Intercessor Warrior", "Intercessor Warrior", "Elimnator Sniper", "Assault Intercessor Grenadier","Intercessor Gunner"],
            ["Assault Intercessor Sargeant", "Assault Intercessor Warrior", "Assault Intercessor Warrior", "Assault Intercessor Grenadier","Intercessor Gunner", "Heavy Intercessor Gunner"],
            ["Intercessor Sargeant", "Intercessor Warrior", "Intercessor Warrior", "Intercessor Warrior", "Intercessor Gunner", "Heavy Intercessor Gunner"],
        ]

        utils.clear()
        print(f"\n{'='*60}")
        print("---------- SELECT YOUR PRE-BUILT OPERATIVE SELECTION")
        for listNum, opLists in enumerate(opSelect, 1):
            print(f"{listNum}. {opLists}")
            for opNum, opList in enumerate(opSelect[listNum - 1], 1):
                print(f"    {opNum}. {opList}")
        print(f"\n{'='*60}")

        while True:
            try:
                choice = int(input(">>> "))
                if 1 <= choice <= len(opSelect):
                    operatorSelection = opSelect[choice - 1]
                    break
                else:
                    print(f"Invalid choice! Please select 1-{len(opSelect)}.")
            except ValueError:
                print("Not a valid number!")

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

        utils.clear()
        print(f"\n{'='*60}")
        print(f"LOADOUT SELECTION FOR: {opName}")
        print(f"{'='*60}\n")

        #Auto add default (fixed) weapon opt
        fixed = weapons.get("fixed", {})
        if fixed:
            # FIX: removed duplicated nested loop; iterate once over fixed[actionType]
            print("--- FIXED WEAPONS (Auto-equipped) ---")
            for actionType in ["shoot", "melee"]:
                if actionType in fixed and fixed[actionType]:
                    for weaponRef in fixed[actionType]:
                        currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
                        #Create a seperate copy of "weapon" dictionary inside the "fixed" dictionary
                        if currWeaponData:
                            weapon = currWeaponData.copy()  
                            loadout.append(weapon) #add weapon dicts (from fixed dict) into loadout weapon list
                            print(f"  [{actionType.upper()}] {weapon['weapon-name']}")
                            input(" Continue >>>")
                        else:
                            print(f"Warning: weapon [{weaponRef}] not found for {opName} (fixed)")
            print("-----")

        # ----------------------------------------------------
        candidateType = []

        if "hard-selection" in weapons and any(weapons["hard-selection"].values()):
            candidateType.append("hard-selection")

        if "free-selection" in weapons and any(weapons["free-selection"].values()):
            candidateType.append("free-selection")

        print(f"Candidate Types: {candidateType}")

        if not candidateType:
            print("No additional weapon selections available for this operative.")
            loadouts[realOpName] = loadout
            loadouts[opName] = loadout
            input("Press Enter to continue >>> ")
            continue

        elif len(candidateType) == 1:
            weapSelect = candidateType[0]
            print(f"Auto-selecting: {utils.keyToName(weapSelect)}\n")

        else:
            # present the available selection types to the player
            print("--- CHOOSE WEAPON SELECTION TYPE ---")
            for i, candidType in enumerate(candidateType, 1):
                if candidType == "hard-selection":
                    print(f"{i}. HARD SELECTION - Choose specific weapons (manual pick)")
                elif candidType == "free-selection":
                    print(f"{i}. FREE SELECTION - Equip all available weapons (auto-equip)")

            # Reinitialize weapSelect here instead of before 
            weapSelect = None
            while weapSelect is None:
                try:
                    choice = int(input(">>> ")) - 1
                    if 0 <= choice < len(candidateType):
                        weapSelect = candidateType[choice]
                        print(f"\nSelected: {utils.keyToName(weapSelect)}\n")
                        input(" Continue >>>")
                    else:
                        print("Invalid choice! Please select a valid option.")
                except ValueError:
                    print("Please input a number.")
                    

        #Hard Selection (user input)
        if weapSelect == "hard-selection":
            hardSelection = weapons[weapSelect]

            for actionType in ["shoot", "melee"]:
                if actionType not in weapons["hard-selection"] or not hardSelection[actionType]:
                    continue

                options = hardSelection[actionType]  # list of weapon refs

                # only 1 hard selection results in it being the default selection
                # modified by hand
                # fix provided by gpt
                if len(options) == 1: 
                    #next() loops through the iter() function which loops through each name-detail keypair inside options list using .items()
                    selectedName = options[0]
                    currWeaponData = getWeaponData(currentKT, actionType, selectedName)
                    if currWeaponData:
                        loadout.append(currWeaponData.copy())
                        print(f"[{actionType.upper()}] Auto-selected (only option): {currWeaponData['weapon-name']}")
                        input(" Continue >>>")
                    else:
                        #load weapon details
                        print(f"Warning: weapon [{selectedName}] not found for {opName}")
                    continue

                # for lists with multiple Hard Selection options, prompts user input
                print(f"--- SELECT {actionType.upper()} WEAPON ---")
                #prints a list of all selectable weap options
                #takes the weapon names in the options list, get its index, then loop through the entire list 
                for i, name in enumerate(options, 1):
                    displayName = name.replace("-", " ").title()
                    print(f"{i}. {displayName}")
                
                # Intalize weapon choosing screen
                weaponChosen = False
                while not weaponChosen:
                    
                    try:    
                        choice = int(input(f"Choose {actionType} weapon: ")) - 1 #reduce for index starts at 0
                        if 0 <= choice < len(options): #ensure answer stays within limit
                            # 1. Find if the player's selected weapon name (which is the key dict) is inside options dict list
                            # 2. Loads selected name of weap in
                            # 3. loads its details in via the selectedName key from the details dict
                            selectedName = options[choice]
                            currWeaponData = getWeaponData(currentKT, actionType, selectedName)
                            if currWeaponData:
                                loadout.append(currWeaponData.copy())
                                print(f"Selected: {currWeaponData['weapon-name']}\n")
                                input(" Continue >>>")
                                weaponChosen = True
                            else:
                                print(f"Warning: weapon [{selectedName}] not found for {opName}")
                        else:
                            print("Invalid choice! Please select from the list.")
                    except ValueError:
                        print("Please input a number.")
                        continue
                    
        # -------------------------
        # 4) If player chose free-selection -> add all free-selection refs
        # -------------------------
        # Free Selection is added by default:
        if weapSelect == "free-selection":
            freeSelection = weapons["free-selection"]
            print("--- EQUIPPING FREE SELECTION WEAPONS ---")

            for actionType in ["shoot", "melee"]:
                if actionType in freeSelection and freeSelection[actionType]:
                    for weaponRef in freeSelection[actionType]:
                        currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
                        if currWeaponData:
                            loadout.append(currWeaponData.copy())
                            print(f"  [{actionType.upper()}] {currWeaponData['weapon-name']}")
                            input(" Continue >>>")
                        else:
                            print(f"Warning: weapon [{weaponRef}] not found for {opName} (free-selection)")

        # # If player didn't choose anything (weapSelect is None) but there is a free-selection, you may want to add it:
        # elif weapSelect is None and "free-selection" in weapons:
        #     # conservative default: add free-selection automatically
        #     for actionType in weapons.get("free-selection", {}):
        #         for weaponRef in weapons["free-selection"][actionType]:
        #             currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
        #             if currWeaponData:
        #                 loadout.append(currWeaponData.copy())

        loadouts[realOpName] = loadout
        loadouts[opName] = loadout

        print(f"\n{'='*60}")
        print(f"Loadout for [{opName}] completed!")
        print(f"FINAL LOADOUT FOR {opName}:")
        if loadout:
            for i, loadoutDetail in enumerate(loadout, 1):
                print(f"{i}. {loadoutDetail['weapon-name']}")
        else:
            print("  (No weapons equipped)")

        print(f"{'='*60}")
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