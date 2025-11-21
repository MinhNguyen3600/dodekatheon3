import json
import string

import utils

# player = {
#     "Operative Selection":[]
# }

AllKillTeams = ["Angels of Death", "Plague Marines"]
def loadData():
    try:       
        with open("data/datasheet.json", "r") as f:
            loadedData = json.load(f) # load json data objects   

    except OSError:
        print("!!!No loadable save file found!!!")

    return loadedData    
    
def ktLoader():
    loadedData = loadData()
    eligibleKT = list(loadedData.keys())
    killTeamList = []
    counter = 0
    for i in range(len(AllKillTeams)):
        for j in range(len(eligibleKT)):
            if AllKillTeams[i] == eligibleKT[j]:
                counter += 1
                exportString = str(counter) + ". " + eligibleKT[j]
                killTeamList.append(exportString)
    return killTeamList

def dataLoader(currentKT: str):
    loadedData = {}
    ktDict = loadData()
    for ktName, ktInfo in ktDict.items():
        datasheets = ktInfo.get("Operative Datasheets", [])

        operatives = {}
        for ops in datasheets:  # ops is dict
            name = ops["Op Name"]
            operatives[name] = ops
        
        selection_rules = ktInfo.get("Operative Selection", [])

        loadedData[ktName] = {
            "operatives": operatives,
            "selection_rules": selection_rules
        }
        return loadedData
    
def legalOps(currentKT: str, loadedData: dict): #data taken from chosen kill team, passed through dataLoader()
    # for operator in ktData["operatives"]:
    selectableOperatives = []
    ktOperatives = loadedData[currentKT]["operatives"]
    ktSelection = loadedData[currentKT]["selection_rules"]
    for operatives in ktOperatives:
        selectableOperatives.append(operatives)

    return ktSelection, ktOperatives

def ktBuild(currentKT: str, ktSelection: list, selectableOperatives: list):
    select = ktSelection[0]
    alphabet =  string.ascii_uppercase # for all caps alphabet like "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    roleMatch = {}
    
    ktBuild = True
    opSelection = []
    
    while ktBuild:
        utils.clear()
        print(f"Your chosen Kill Team [{currentKT}] has the following selectable operatives:")
        opIndex = 1
        roleIndex = 0
        for roles, roleOptions in select.items():
            opt = roleOptions.get("options", [])
            matches = []

            # Loop for loading list of options for matching later
            for ops in selectableOperatives:
                if ops in opt:
                    matches.append(ops)

            # Only printing items out if it matches the options 
            if matches: 
                letter = alphabet[roleIndex]
                limit = roleOptions.get("limit", 0)

                print(f"{letter}. Selectable [{roles}] (Limit: {limit}):")

                for opIndex, op in enumerate(matches, 1):
                    print(f"    {opIndex}. {op}")

                roleMatch[letter] = (matches, limit)
                roleIndex += 1

        choice = input(">>> ").upper()

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
                if limit == 0:
                    opSelection.append(selectedOp)
                    print(f"Selected: {selectedOp}")
                    input(">>> ")
                elif opCount >= limit:
                    print(f"Cannot select more than {limit} operatives for the role [{roles}]!")
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

def ktDataLoader(currKT: str, opSelect: list):
    loadedData = dataLoader(currKT)
    opData = loadedData[currKT]["operatives"]
    selectedData = []

    for opName in opSelect:
        if opName in opData:
            operative = opData[opName]
            selectedData.append(operative)

        else:
            print(f"Waning: Operative [{opName}] not found in datasheets for {currKT}")

    return selectedData # Tuple: (raw_list, processed_list)

def opDatasheet(selectedData: list):
    for operative in selectedData:
        #Entire section written by Grok
        # START --->/
        # Data Sheet
        datasheet = operative['Op Data Sheet']

        # Print operative card
        print("\n" + "-" * 100)
        print(f"| [ {operative['Op Name']:<20} ]                                | APL: {datasheet['APL']}  M: {datasheet['Move']}  Sv: {datasheet['Save']}  W: {datasheet['Wounds']:<5} |")
        print("-" * 100)
        
        # Weapon Options
        weapons = operative['Weapon Options']
        hasWeapons = False
        for category in ['Free Selection', 'Hard Selection']:
            if category in weapons and weapons[category]:
                print(f"| {category:<98}:                                                                                   |")
                for actionType in ['Shoot', 'Melee', 'Fixed']:
                    if actionType in weapons[category]and weapons[category][actionType]:
                        hasWeapons = True
                        print(f"|   {actionType}:                                                                                         |")
                        print("|     Weapon Name                      | A |Hit| Dmg   | Keywords                                   |")
                        print("-" * 100)
                        for weaponName, details in weapons[category][actionType].items():
                            if isinstance(details['dmg'], list):
                                dmg = f"{details['dmg'][0]}/{details['dmg'][1]}" 
                            else: 
                                dmg = details['dmg']
                            
                            if 'Weapon Keyword' in details:
                                keywords = ", ".join(details['Weapon Keyword']) 
                            else: 
                                keywords = ""
                            print(f"|     {weaponName:<30}   | {details['atk']} | {details['hit']} | {dmg:<5} | [{keywords:<40}] |")
                        print("-" * 100)
        if not hasWeapons:
            print("| Weapons: None                                                                                  |")
            print("-" * 100)

        # Op Skills (if any)
        skills = operative.get('Op Skills', {})
        if skills:
            print("| Skills:                                                              |")
            for skill_name, desc in skills.items():
                print(f"|   {skill_name}: {desc:<58} |")
        else:
            pass

        print("-" * 100)
        # Op Keywords
        keywords = ", ".join(operative['Op Keyword'])
        print(f"| [{keywords:<64}]                             |")
        print("-" * 100)
        # /---> END

    
#Entire section written by Grok
# START --->/
# Process into game-ready dict
def processForGamePhases(selectedData: list):
    operative_data_list = []  # Processed list for game looping

    for operative in selectedData:
        processed_op = {
            'name': operative['Op Name'],
            'stats': operative['Op Data Sheet'],  # {'APL': 3, 'Move': 6, ...}
            'weapons': [],  # List of all weapons (shoot + melee)
            'skills': operative.get('Op Skills', {}),
            'keywords': operative['Op Keyword']
        }
        
        # Flatten weapons from all categories
        weapons = operative['Weapon Options']
        for category in ['Free Selection', 'Hard Selection']:
            if category in weapons:
                for action_type in ['Shoot', 'Melee']:
                    if action_type in weapons[category]:
                        for weapon_name, details in weapons[category][action_type].items():
                            details['name'] = weapon_name
                            details['category'] = category
                            details['action_type'] = action_type
                            processed_op['weapons'].append(details)
        
        operative_data_list.append(processed_op)
    
    return operative_data_list
    # /---> END


