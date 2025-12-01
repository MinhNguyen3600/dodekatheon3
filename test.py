import menu
import utils
import army

currentKT = "angels-of-death"
currentKT = "angels-of-death"
opDataLoad = army.opDataLoader(currentKT)


print("===---------------------------------------===")
# print(army.ktLoader())
print("----------------------")
# print(opDataLoad)
# print("===---------------------------------------===")
# ktOpSelect = ktBuild(currentKT, opDataLoad)
ktOpSelect = ["Space Marine Captain", "Elimnator Sniper", "Assault Intercessor Grenadier","Intercessor Gunner", "Intercessor Warrior", "Intercessor Warrior"]
selectedOps = army.getOpData(currentKT, ktOpSelect)
print("----------------------")
# for i in range(len(selectedOps)):
#     print(selectedOps[i])
opLoad = menu.opLoadoutScreen(currentKT, selectedOps)
print("----------------------")
finalSelecOps = army.finalizeOp(currentKT, selectedOps, opLoad)
# print(finalSelecOps)
# for i in range(len(finalSelecOps)):
#     print(finalSelecOps[i]['loadout'])

print("----------------------")
# print(army.opDataLoader(currentKT)["operatives"])
print(army.opDatasheet(finalSelecOps))
print("===---------------------------------------===")