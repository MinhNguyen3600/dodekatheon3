import json
import string

import utils





AllKillTeams = ["angels-of-death", "plague-marines"]

# Post-data/datasheet.json restructuring:
# ✅Works!
def loadData() -> dict:
    try:       
        with open("data/datasheet.json", "r") as f:
            loadedData = json.load(f) # load json data objects   

    except OSError:
        print("!!!No loadable save file found!!!")

    return loadedData  
    
# Post-data/datasheet.json restructuring:
# ✅Works! (after modifying AllKillTeams list to include dict keys that matches ones in datasheet)
# For listing existing kill teams, nothing else otherwise
def ktLoader() -> list:
    loadedData = loadData()
    eligibleKT = list(loadedData.keys())
    killTeamList = []
    counter = 0
    for i in range(len(AllKillTeams)):
        for j in range(len(eligibleKT)):
            if AllKillTeams[i] == eligibleKT[j]:
                counter += 1
                exportString = str(counter) + ". " + loadedData[eligibleKT[j]]["killteam-name"]
                killTeamList.append(exportString)

    return killTeamList

# Post-data/datasheet.json restructuring:
# ✅Works! (updated to load operatives sequentially depending on currently selected KT)
def opDataLoader(currentKT: str) -> dict:
    ktDict = loadData()
    ktInfo = ktDict[currentKT]
    datasheets = ktInfo.get("operative-datasheets", {})

    operatives = {}
    for opKey, opData in datasheets.items():  # ops is dict
        opCopy = opData.copy()
        opCopy["op-id"] = opKey

        # AI gen
        opCopy["op-keyword"] = [str(k).lower() for k in opCopy.get("op-keyword")]

        operatives[opKey] = opCopy
    
    selectionRules = ktInfo.get("operative-selection", {})

    ktLoadedData = {
        "operatives": operatives,
        "weapons": ktInfo.get("weapons", {}),
        "killteam-name": ktInfo.get("killteam-name", currentKT.replace("-", " ").title()),   # replaces dashes with spaces, and capitalizes first character of each word.
        "selection-rules": selectionRules
    }
    return ktLoadedData

# legalOps() func removed for being a redundant operative data loader & never called    

# Post-data/datasheet.json restructuring:
# ✅Works! (So many changed, I literally cannot list, but second part of the 
# function, after "if len(opSelection) == 6:" is remains basically the same)
def ktBuild(currentKT: str, ktLoadedOps: dict):
    alphabet =  string.ascii_uppercase # for all caps alphabet like "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    ktBuild = True
    opSelection = []

    ktDisplayName = currentKT.replace("-", " ").title()

    # load init data from ktLoadedOps (which is from opDataLoader)
    ktOps = ktLoadedOps["operatives"]
    ktSelect = ktLoadedOps["selection-rules"]

    #--------------------------
    opOrder = list(ktOps.keys())
    opDisplay = {}
    opKeySets = {}

    for opName, opData in ktOps.items():
        opDisplayName = opName.replace("-", " ").title()
        opDisplay[opName] = opData.get("op-name", opDisplayName)

        opKeyWord = opData.get("op-keyword", [])
        opKeySets[opName] = set()

        for k in opKeyWord:
            opKeySets[opName].add(str(k).lower())
    
    #--------------------------

    while ktBuild:
        utils.clear()
        print(f"Your chosen Kill Team [{ktDisplayName}] has the following selectable operatives:")
        
        roleIndex = 0
        roleMatch = {}

        for roleName, roleOptions in ktSelect.items():
            options = roleOptions.get("options", [])
            limit = roleOptions.get("limit", None)
            matches = []

            opKeyList = []
            for opt in options:
                if isinstance(opt, str) and opt in ktOps:
                    if opt in ktOps:
                        opKeyList.append(opt)

            for old in opKeyList:   
                if old not in matches:
                    matches.append(old)

            # Loop for loading list of options for matching later
            
            optList = []
            for opt in options:
                if isinstance(opt, str) and opt not in opKeyList:
                    optList.append(opt.lower())

            if optList:
                for opName in opOrder:
                    if opName in matches:
                        continue
                
                    kws = opKeySets.get(opName, set())

                    for opKeyword in optList:
                        if opKeyword in kws:
                            matches.append(opName)
                            break

            if not matches:
                continue

            # Only printing items out if it matches the options 
            letter = alphabet[roleIndex]
            if limit is None:
                displayLimit = "Unlimited"
            else:
                displayLimit = limit

            print(f"{letter}. Selectable [{roleName}] (Limit: {displayLimit}):")

            for opIndex, op in enumerate(matches, 1):
                print(f"    {opIndex}. {opDisplay.get(op, op)}")

            roleMatch[letter] = (matches, limit)
            roleIndex += 1
        # Show current roster
        print(f"\nCurrent roster ({len(opSelection)}/6):")
        if opSelection:
            for i, name in enumerate(opSelection, 1):
                print(f"   {i}. {opDisplay.get(name, name)}")
        else:
            print("   — Empty —")

        if len(opSelection) == 6:
            print("\n*** ROSTER FULL — 6/6 OPERATIVES SELECTED ***")
            input("\nPress Enter to confirm...")
            break

        choice = input(">>> ").upper()
        if choice == "Q":
            break
        elif choice == "R":
            continue

        if len(opSelection) == 6:
            break
        elif len(choice) >= 2 and choice[0] in roleMatch and isinstance(int(choice[1:]), int):
            letter = choice[0]
            try:
                num = int(choice[1:]) - 1
            except ValueError:
                print("Invalid number!")
                continue
            matches, limit = roleMatch[letter]
            if 0 <= num < len(matches):
                selectedOp = matches[num]
                opCount = 0
                for sel in opSelection:
                    if sel in matches:
                        opCount += 1
                if limit is None:
                    opSelection.append(selectedOp)
                    print(f"Selected: {selectedOp}")
                    input(">>> ")
                elif opCount >= limit:
                    print(f"Cannot select more than {limit} operatives for the role [{roleName}]!")
                    input(">>> ")
                    continue
                else:
                    opSelection.append(selectedOp)
                    print(f"Selected: {selectedOp}")
                    input(">>> ")
            else:
                print("Invalid number!")
        else:
            print("Invalid input!")

    return opSelection  

# Entire section written by Grok*
# * Later modified heavily by me due to new structure
# START --->/

# FORMER ktDataLoader is split into 2 of the following functions:

# Post-data/datasheet.json restructuring:
# ✅Works! (Updated:
# 1. opName -> realOpName when attempting to call operative keys
# 2. truned opList from a Dict to a List for easier indexing)
def getOpData(currKT: str, opSelect: list):
    if opSelect and isinstance(opSelect[0], dict):
        return opSelect

    ktData = opDataLoader(currKT)
    opList = []

    for opName in opSelect:
        realOpName = opName.replace(" ", "-").lower()
        if opName in ktData["operatives"][realOpName]["op-name"]:
            opList.append(ktData["operatives"][realOpName])

    selectedOp = []
    for opName in opSelect:
        realOpName = opName.replace(" ", "-").lower()
        for i in range(len(opList)):
            if opName in opList[i]["op-name"]:
                selectedOp.append(opList[i])
            # else:
            #     print(f"Warning: Operative [{opName}] not found in {currKT}")
        
    return selectedOp

# Post-data/datasheet.json restructuring:
# [WIP] Heavily reliant on /menu.py's opLoadoutScreen() func to output loadouts dict.
def finalizeOp(
    currKT: str, 
    opSelect: list, 
    loadouts: dict
) -> list:
    ktData = opDataLoader(currKT)
    opDictFinal = ktData["operatives"]
    # print(f"FinalizeOp()'s opDictFinal: \n{opDictFinal}")
    finalOps = []

    for op in opSelect:
        opName = op.get("op-name")
        realOpName = opName.replace(" ", "-").lower()

        if realOpName not in opDictFinal:
            print(f"Warning: Operative [{opName["op-name"]}] missing!")
            continue
        
        opCopy = opDictFinal[realOpName].copy()
        opLoadout = loadouts.get(opName)
    
        if opLoadout is None:
            opLoadout = loadouts.get(realOpName, [])
       
        opCopy["loadout"] = opLoadout
        finalOps.append(opCopy)

    return finalOps

# partial fix handwritten
# full fix provided by gpt
def opDatasheet(selectedData: list):
    for datasheet in selectedData:
        # print(f"OpDatasheet()'s selectedData: {selectedData}")
        #Entire section written by Grok
        # START --->/
        # Load data from datasheet:
        opStats = datasheet.get("op-datasheet", {})
        apl = opStats.get("apl", "?")
        mv = opStats.get("mv", "?")
        sv = opStats.get("sv", "?")
        wounds = opStats.get("wounds", "?")

        # header
        print("\n" + "-" * 100)
        print(f"| [ {datasheet.get('op-name','Unknown'):<20} ]                                | APL: {apl}  M: {mv}  Sv: {sv}  W: {wounds:<5} |")
        print("-" * 100)

        # weaponSelection = what the operative may choose (datasheet)
        weaponSelection = datasheet.get("weapon-opts", {})
        # weaponsData (loadout) = actual selected weapon dictionaries (list)
        weaponsData = datasheet.get("loadout", [])  # list of weapon dicts
        hasWeapons = False

        for category in ["free-selection", "hard-selection", "fixed"]:
            if category in weaponSelection and weaponSelection[category]:
                print(f"| {category:<98}:                                                                                   |")
                for actionType in ["shoot", "melee"]:
                    refs = weaponSelection[category].get(actionType, [])
                    if refs:
                        hasWeapons = True
                        print(f"|   {actionType}:                                                                                         |")
                        print("|     Weapon Name                      | A |Hit| Dmg   | Keywords                                   |")
                        print("-" * 100)

                        # for each referenced weapon key in the datasheet selection list
                        for weaponRef in refs:
                            # print(weaponRef)
                            # try to find the corresponding selected weapon dict in weaponsData
                            matched = None
                            for wdict in weaponsData:
                                wname = wdict.get("weapon-name", "")
                                wname = wname.replace(" ", "-").lower()
                                # print(wname)
                                if wname == weaponRef:
                                    matched = wdict
                                    break

                            if not matched:
                                # not found in selected loadout — warn and continue
                                # print(f"Warning: weapon [{weaponRef}] not found in loadout for {datasheet.get('op-name')}")
                                continue

                            # matched is a weapon dict; either has 'profiles' (shoot multi-profile) or flat stats (melee)
                            if "profiles" in matched and isinstance(matched["profiles"], dict):
                                profiles = matched["profiles"]
                                for currentProfile, profileData in profiles.items():
                                    # profileData may hold atk/hit/dmg/weapon-keyword
                                    dmg = profileData.get("dmg", "")
                                    if isinstance(dmg, list) and len(dmg) >= 2:
                                        dmgStr = f"{dmg[0]}/{dmg[1]}"
                                    else:
                                        dmgStr = str(dmg)

                                    keywords = ""
                                    if "weapon-keyword" in profileData:
                                        keywords = ", ".join(profileData.get("weapon-keyword", []))

                                    # print an informative line (profile then details)
                                    print(f"| {matched.get('weapon-name','') + ' ('+ currentProfile +')':<30}   | {profileData.get('atk','?')} | {profileData.get('hit','?')} | {dmgStr:<5} | [{keywords:<40}] |")
                                print("-" * 100)
                            else:
                                # melee or single-profile flattened weaponData
                                atk = matched.get("atk", "?")
                                hit = matched.get("hit", "?")
                                dmg = matched.get("dmg", "")
                                if isinstance(dmg, list) and len(dmg) >= 2:
                                    dmgStr = f"{dmg[0]}/{dmg[1]}"
                                else:
                                    dmgStr = str(dmg)
                                keywords = ""
                                if "weapon-keyword" in matched:
                                    keywords = ", ".join(matched.get("weapon-keyword", []))

                                print(f"|     {matched.get('weapon-name',''):<30}   | {atk} | {hit} | {dmgStr:<5} | [{keywords:<40}] |")
                                print("-" * 100)

        if not hasWeapons:
            print("| Weapons: None                                                                                  |")
            print("-" * 100)

        # Op Skills (if any)
        skills = datasheet.get("op-skills", {})
        if skills:
            print("| Skills:                                                              |")
            for skillName, desc in skills.items():
                print(f"|   {skillName}: {desc:<58} |")
        # Op Keywords
        keywords = ", ".join(datasheet.get("op-keyword", []))
        print("-" * 100)
        print(f"| [{keywords:<64}]                             |")
        print("-" * 100)
        # # /---> END

# # Process into game-ready dict
# def processForGamePhases(selectedData: list):
#     opeDataList = []  # Processed list for game looping

#     for operative in selectedData:
#         processed_op = {
#             'name': operative['Op Name'],
#             'stats': operative['Op Data Sheet'],  # {'APL': 3, 'Move': 6, ...}
#             'weapons': [],  # List of all weapons (shoot + melee)
#             'skills': operative.get('Op Skills', {}),
#             'keywords': operative['Op Keyword']
#         }
        
#         # Flatten weapons from all categories
#         weapons = operative['Weapon Options']
#         for category in ['Free Selection', 'Hard Selection']:
#             if category in weapons:
#                 for actionType in ['Shoot', 'Melee']:
#                     if actionType in weapons[category]:
#                         for weaponName, details in weapons[category][actionType].items():
#                             details['name'] = weaponName
#                             details['category'] = category
#                             details['action_type'] = actionType
#                             processed_op['weapons'].append(details)
        
#         opeDataList.append(processed_op)
    
#     return opeDataList
    # /---> END


#-----------------------------------
# NOTE: 'None' object that serves as a placeholder when you need to specify that 
# a variable doesn't hold any valid data or when a function doesn't return any value.
# def ktDataLoader(currKT: str, opSelect: list, loadouts: dict = None)
#-----------------------------------
