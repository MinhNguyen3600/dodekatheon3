

# -------------------- [Claude] Menu.py's opLoadoutScreen() function def --------------
# def opLoadoutScreen(
#     currentKT: str,
#     selectedData: list
# ) -> dict:
#     ktData = army.opDataLoader(currentKT)
#     loadouts = {}

#     for operative in selectedData:
#         opSelectName = operative["op-name"]
#         realOpName = opSelectName.replace(" ", "-").lower()
#         opName = ktData["operatives"][realOpName]["op-name"]
#         weapons = ktData["operatives"][realOpName]["weapon-opts"]
#         loadout = []

#         utils.clear()
#         print(f"\n{'='*60}")
#         print(f"LOADOUT SELECTION FOR: {opName}")
#         print(f"{'='*60}\n")

#         # STEP 1: Auto add fixed weapons
#         fixed = weapons.get("fixed", {})
#         if fixed:
#             print("--- FIXED WEAPONS (Auto-equipped) ---")
#             for actionType in ["shoot", "melee"]:  # ✓ FIXED: Separate the loops properly
#                 if actionType in fixed and fixed[actionType]:  # ✓ Check if actionType exists and has weapons
#                     for weaponRef in fixed[actionType]:  # ✓ FIXED: Nested loop for weapons
#                         currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
#                         if currWeaponData:
#                             weapon = currWeaponData.copy()
#                             loadout.append(weapon)
#                             print(f"  [{actionType.upper()}] {weapon['weapon-name']}")
#                         else:
#                             print(f"  Warning: weapon [{weaponRef}] not found for {opName} (fixed)")
#             print()  # Add spacing

#         # STEP 2: Determine available selection types and build candidateTypes list
#         candidateTypes = []  # ✓ FIXED: Initialize as empty list
        
#         if "hard-selection" in weapons and any(weapons["hard-selection"].values()):
#             candidateTypes.append("hard-selection")
            
#         if "free-selection" in weapons and any(weapons["free-selection"].values()):
#             candidateTypes.append("free-selection")

#         print(f"DEBUG - Candidate Types: {candidateTypes}")  # Debug line

#         # STEP 3: Handle selection based on available types
#         if not candidateTypes:
#             # No selections available
#             print("No additional weapon selections available for this operative.")
#             loadouts[realOpName] = loadout
#             loadouts[opName] = loadout
#             input("Press Enter to continue >>> ")
#             continue  # ✓ FIXED: Skip to next operative

#         elif len(candidateTypes) == 1:
#             # Only one type available - auto-select it
#             weapSelect = candidateTypes[0]
#             print(f"Auto-selecting: {weapSelect.replace('-', ' ').title()}\n")

#         else:
#             # Multiple types available - let player choose
#             print("--- CHOOSE WEAPON SELECTION TYPE ---")
#             for i, selType in enumerate(candidateTypes, 1):
#                 if selType == "hard-selection":
#                     print(f"{i}. HARD SELECTION - Choose specific weapons (manual pick)")
#                 elif selType == "free-selection":
#                     print(f"{i}. FREE SELECTION - Equip all available weapons (auto-equip)")

#             # Force player to choose
#             weapSelect = None
#             while weapSelect is None:
#                 try:
#                     choice = int(input("\nYou MUST choose a selection type: ")) - 1
#                     if 0 <= choice < len(candidateTypes):
#                         weapSelect = candidateTypes[choice]
#                         print(f"\n✓ Selected: {weapSelect.replace('-', ' ').title()}\n")
#                     else:
#                         print("Invalid choice! Please select a valid option.")
#                 except ValueError:
#                     print("Please enter a number.")

#         # STEP 4A: Process Hard Selection
#         if weapSelect == "hard-selection":
#             hardSelection = weapons["hard-selection"]

#             for actionType in ["shoot", "melee"]:
#                 if actionType not in hardSelection or not hardSelection[actionType]:
#                     continue

#                 options = hardSelection[actionType]

#                 # Auto-select if only 1 option
#                 if len(options) == 1:
#                     selectedName = options[0]
#                     currWeaponData = getWeaponData(currentKT, actionType, selectedName)
#                     if currWeaponData:
#                         loadout.append(currWeaponData.copy())
#                         print(f"[{actionType.upper()}] Auto-selected (only option): {currWeaponData['weapon-name']}")
#                     else:
#                         print(f"Warning: weapon [{selectedName}] not found for {opName}")
#                     continue

#                 # Multiple options - prompt user
#                 print(f"--- SELECT {actionType.upper()} WEAPON ---")
#                 for i, name in enumerate(options, 1):
#                     displayName = name.replace("-", " ").title()
#                     print(f"  {i}. {displayName}")
                
#                 # Force weapon selection
#                 weaponChosen = False
#                 while not weaponChosen:
#                     try:
#                         choice = int(input(f"Choose {actionType} weapon: ")) - 1
#                         if 0 <= choice < len(options):
#                             selectedName = options[choice]
#                             currWeaponData = getWeaponData(currentKT, actionType, selectedName)
#                             if currWeaponData:
#                                 loadout.append(currWeaponData.copy())
#                                 print(f"✓ Selected: {currWeaponData['weapon-name']}\n")
#                                 weaponChosen = True
#                             else:
#                                 print(f"Warning: weapon [{selectedName}] not found for {opName}")
#                         else:
#                             print("Invalid choice! Please select from the list.")
#                     except ValueError:
#                         print("Please enter a number.")

#         # STEP 4B: Process Free Selection
#         elif weapSelect == "free-selection":
#             freeSelection = weapons["free-selection"]
#             print("--- EQUIPPING FREE SELECTION WEAPONS ---")

#             for actionType in ["shoot", "melee"]:
#                 if actionType in freeSelection and freeSelection[actionType]:  # ✓ Check existence
#                     for weaponRef in freeSelection[actionType]:
#                         currWeaponData = getWeaponData(currentKT, actionType, weaponRef)
#                         if currWeaponData:
#                             loadout.append(currWeaponData.copy())
#                             print(f"  [{actionType.upper()}] {currWeaponData['weapon-name']}")
#                         else:
#                             print(f"  Warning: weapon [{weaponRef}] not found for {opName} (free-selection)")

#         # STEP 5: Store and display final loadout
#         loadouts[realOpName] = loadout
#         loadouts[opName] = loadout

#         print(f"\n{'='*60}")
#         print(f"FINAL LOADOUT FOR {opName}:")
#         if loadout:
#             for i, loadoutDetail in enumerate(loadout, 1):
#                 print(f"  {i}. {loadoutDetail['weapon-name']}")
#         else:
#             print("  (No weapons equipped)")
#         print(f"{'='*60}")
#         input("\nPress Enter to continue to next operative >>> ")

#     return loadouts


# ----------------------- [Claude] Army.py's opDatasheet() Function Def --------------------

def opDatasheet(selectedData: list):
    for datasheet in selectedData:
        # Load operative stats
        opStats = datasheet.get("op-datasheet", {})
        apl = opStats.get("apl", "?")
        mv = opStats.get("mv", "?")
        sv = opStats.get("sv", "?")
        wounds = opStats.get("wounds", "?")

        # Header
        print("\n" + "-" * 100)
        print(f"| [ {datasheet.get('op-name','Unknown'):<20} ]                                | APL: {apl}  M: {mv}  Sv: {sv}  W: {wounds:<5} |")
        print("-" * 100)

        # Get actual equipped weapons from loadout
        weaponsData = datasheet.get("loadout", [])
        
        if not weaponsData:
            # No weapons equipped - show warning
            print("| LOADOUT: No weapons equipped                                                                   |")
            print("-" * 100)
        else:
            # Separate weapons by type
            shootWeapons = []
            meleeWeapons = []
            
            for weapon in weaponsData:
                # Determine weapon type by checking if it has profiles (shoot) or flat stats (melee)
                if "profiles" in weapon:
                    shootWeapons.append(weapon)
                else:
                    meleeWeapons.append(weapon)
            
            # Only display SHOOT section if there are shoot weapons
            if shootWeapons:
                print("|   SHOOT:                                                                                       |")
                print("|     Weapon Name                      | A |Hit| Dmg   | Keywords                                   |")
                print("-" * 100)
                
                for weapon in shootWeapons:
                    profiles = weapon.get("profiles", {})
                    for profileName, profileData in profiles.items():
                        # Format damage
                        dmg = profileData.get("dmg", "")
                        if isinstance(dmg, list) and len(dmg) >= 2:
                            dmgStr = f"{dmg[0]}/{dmg[1]}"
                        else:
                            dmgStr = str(dmg)
                        
                        # Format keywords
                        keywords = ", ".join(profileData.get("weapon-keyword", []))
                        
                        # Print weapon line with profile
                        weaponDisplay = f"{weapon.get('weapon-name','')} ({profileName})"
                        print(f"|     {weaponDisplay:<36} | {profileData.get('atk','?')} | {profileData.get('hit','?')} | {dmgStr:<5} | [{keywords:<40}] |")
                print("-" * 100)
            
            # Only display MELEE section if there are melee weapons
            if meleeWeapons:
                print("|   MELEE:                                                                                       |")
                print("|     Weapon Name                      | A |Hit| Dmg   | Keywords                                   |")
                print("-" * 100)
                
                for weapon in meleeWeapons:
                    atk = weapon.get("atk", "?")
                    hit = weapon.get("hit", "?")
                    
                    # Format damage
                    dmg = weapon.get("dmg", "")
                    if isinstance(dmg, list) and len(dmg) >= 2:
                        dmgStr = f"{dmg[0]}/{dmg[1]}"
                    else:
                        dmgStr = str(dmg)
                    
                    # Format keywords
                    keywords = ", ".join(weapon.get("weapon-keyword", []))
                    
                    # Print weapon line
                    print(f"|     {weapon.get('weapon-name',''):<36} | {atk} | {hit} | {dmgStr:<5} | [{keywords:<40}] |")
                print("-" * 100)

        # Op Skills (if any)
        skills = datasheet.get("op-skills", {})
        if skills:
            print("| SKILLS:                                                                                        |")
            for skillName, desc in skills.items():
                print(f"|   {skillName}: {desc:<88} |")
            print("-" * 100)
        
        # Op Keywords
        keywords = ", ".join(datasheet.get("op-keyword", []))
        print(f"| KEYWORDS: [{keywords:<85}] |")
        print("-" * 100)