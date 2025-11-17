import os

import army
import utils

game = True





while game:
    killTeams = army.ktLoader()
    
    utils.clear()
    utils.draw()
    print("SELECT YOUR KILL TEAM:")
    for kt in killTeams:
        print(kt)
    print("0. Exit Game")
    utils.draw()

    choice = input(">>> ")
    if choice == "0":
        quit()
    else:
        for chosen in range(len(killTeams)):
            chosenKT = killTeams[chosen]
            if choice == chosenKT[0]:
                currentKT = killTeams[chosen][3:]
    utils.draw()
    input(f"You've chosen the [{currentKT}] Kill Team!")

    utils.clear()
    dataLoad = army.dataLoader(currentKT)
    # for i in dumbass:
    #     print(dumbass[i])
    eligibleOps = army.legalOps(currentKT, dataLoad)
    operatorSelection = army.ktBuild(currentKT, eligibleOps[0], eligibleOps[1])
 
    utils.clear()
    print(f"Player A started [{currentKT}] with the following army list:")
    for i in range(len(operatorSelection)):
        print(f"- {operatorSelection[i]}")
    input(">>> ")





    