import army 
import os

game = True


# --------- Utilities ----------
def draw():
    print("Xx----------------------xX")

def clear():
    os.system("cls")


while game:
    killTeams = army.ktLoader()

    draw()
    print("SELECT YOUR KILL TEAM:")
    for kt in killTeams:
        print(kt)
    draw()

    choice = input(">>> ")

    for chosen in range(len(killTeams)):
        chosenKT = killTeams[chosen]
        if choice == chosenKT[0]:
            currentKT = killTeams[chosen][3:]

    draw()
    print(currentKT)
    input(f"You've chosen the [{currentKT}] Kill Team!")

    clear()

    dataLoad = army.dataLoader(currentKT)
    # for i in dumbass:
    #     print(dumbass[i])
    eligibleOps = army.legalOps(currentKT, dataLoad)
    army.ktBuild(currentKT, eligibleOps[0], eligibleOps[1])






    