import menu
import utils
import army


print("===---------------------------------------===")
currentKT, loaded = menu.ktSelectScreen()
print("----------------------")
selectedOps = menu.opSelectScreen(currentKT, loaded)
print(f"Test.py Output: {selectedOps}")
print("----------------------")
opData = army.getOpData(currentKT, selectedOps)
print(f"Test.py Output: {opData}")
print("----------------------")
opLoadouts = menu.opLoadoutScreen(currentKT, opData)
print(f"Test.py Output: {opLoadouts}")
print("----------------------")
finalOpData = army.finalizeOp(currentKT, opData, opLoadouts)
print(f"Test.py Output: {finalOpData}")
print("----------------------")
army.opDatasheet(finalOpData)
print("===---------------------------------------===")