import json
import string

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
    roleIndex = 0

    print(f"Your chosen Kill Team [{currentKT}] has the following selectable operatives:")

    for roles, roleOptions in select.items():
        opt = roleOptions.get("options", [])
        opIndex = 1
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

            roleMatch[letter] = matches
            roleIndex += 1

    choice = input(">>> ").upper()
    opSelection = []
    # while len(opSelection) <= 6 # asdasdsd
    if len(choice) >= 2 and choice[0] in roleMatch and isinstance(int(choice[1:]), int):
        letter = choice[0]
        num = int(choice[1:]) - 1
        matches = roleMatch[letter]

        if 0 <= num < len(matches):
            selectedOp = matches[num]
            opSelection.append("selectedOp")
            print(f"Selected: {selectedOp}")
        else:
            print("Invalid number!")
    else:
        print("Invalid input!")
