import rolls as rolls
import weaponAbilityDict as wad
import re

# Test control Unit dict


# ============================================
# COMMAND PHASE IMPLEMENTATION
# ============================================

def commandPhase(game_state):
    """
    Execute the command phase with proper ability timing.
    
    Args:
        game_state: Dictionary containing:
            - "attacker_unit": dict
            - "defender_unit": dict
            - "attacker_count": int
            - "defender_count": int
            - "oath_target": str or None
    
    Returns:
        Updated game_state after command phase
    """
    
    print("\n" + "="*60)
    print("COMMAND PHASE")
    print("="*60)
    
    # START OF COMMAND PHASE
    print("\n--- START OF COMMAND PHASE ---")
    game_state = process_start_of_command(game_state)
    
    # END OF COMMAND PHASE
    print("\n--- END OF COMMAND PHASE ---")
    game_state = process_end_of_command(game_state)
    
    print("\n" + "="*60)
    print("COMMAND PHASE COMPLETE")
    print("="*60 + "\n")
    
    return game_state


def process_start_of_command(game_state):
    """Process abilities that trigger at START of command phase"""
    
    attacker = game_state["attacker_unit"]
    defender = game_state["defender_unit"]
    
    faction_ability = attacker.get("Faction Ability")
    
    # Oath of the Moment (Space Marines)
    if faction_ability == "Oath of the Moment":
        game_state = activate_oath_of_moment(attacker, defender, game_state)
    
    return game_state


def process_end_of_command(game_state):
    """Process abilities that trigger at END of command phase"""
    
    attacker = game_state["attacker_unit"]
    faction_ability = attacker.get("Faction Ability")
    
    # Reanimation Protocols (Necrons)
    if faction_ability == "Reanimation Protocols":
        game_state = activate_reanimation_protocols(attacker, game_state)
    
    return game_state


def activate_oath_of_moment(attacker_unit, defender_unit, game_state):
    """
    Space Marines: Oath of the Moment
    Timing: START of command phase
    Effect: Select one enemy unit as oath target
    """
    
    print(f"\n[{attacker_unit['Name']}] Activating OATH OF THE MOMENT...")
    
    # Set the defender as the oath target
    game_state["oath_target"] = defender_unit["Name"]
    
    print(f"✓ Oath Target selected: {defender_unit['Name']}")
    print("  Effect: Re-roll hit rolls when targeting this unit")
    
    # Check if attacker has unit-specific ability tied to Oath
    unit_ability = attacker_unit.get("Ability", {})
    if unit_ability.get("condition") == "isOathTarget":
        print(f"  └─ [{attacker_unit['Name']}] ability '{unit_ability['name']}' is now active!")
        print(f"     Effect: {unit_ability.get('modifier', 'modify')} to {unit_ability.get('target', 'rolls')}")
    
    return game_state


def activate_reanimation_protocols(unit, game_state):
    """
    Necrons: Reanimation Protocols
    Timing: END of command phase
    Effect: Heal D3 wounds OR return destroyed models
    """
    
    print(f"\n[{unit['Name']}] Activating REANIMATION PROTOCOLS...")
    
    # Get current state
    current_count = game_state["attacker_count"]
    max_count = unit["Model Count"]
    max_wounds = unit["Profile"]["w"]
    
    # Use proper wound tracking key
    if "attacker_current_wounds" not in game_state:
        game_state["attacker_current_wounds"] = max_wounds
    
    current_wounds = game_state["attacker_current_wounds"]
    
    print(f"  Current status: {current_count}/{max_count} models, {current_wounds}/{max_wounds} wounds")
    
    # Base effect: Heal damaged models (if unit has models remaining and they're damaged)
    if current_count > 0 and current_wounds < max_wounds:
        healing = rollD3()
        new_wounds = min(current_wounds + healing, max_wounds)
        game_state["attacker_current_wounds"] = new_wounds
        
        print(f"  ✓ Healed {healing} wounds ({current_wounds} → {new_wounds})")
    
    # Special condition: Return destroyed models
    models_destroyed = max_count - current_count
    
    if models_destroyed > 0 and current_count > 0 and max_count > 1:
        # Return 1 model with 1 wound
        game_state["attacker_count"] = current_count + 1
        game_state["attacker_current_wounds"] = 1  # Returned model has 1 wound
        
        print(f"  ✓ Returned 1 destroyed model to the unit!")
        print(f"    Models: {current_count} → {current_count + 1}")
    elif models_destroyed == 0 and current_count > 0 and current_wounds == max_wounds:
        print(f"  No damage taken - Reanimation has no effect")
    elif current_count == 0:
        print(f"  Unit completely destroyed - cannot reanimate")
    
    return game_state


# ============================================
# EXISTING FUNCTIONS (unchanged)
# ============================================

def dataLoad(
    controlUnit: dict,
    targetUnit: dict,
):
    cuName = controlUnit["Name"]            #str
    cuPiece = controlUnit["Piece"]          #str
    cuProfile = controlUnit["Profile"]      #dict
    cuWeapons = controlUnit["Weapons"]      #list
    cuCount = controlUnit["Model Count"]    #int
    cuKeywords = controlUnit["Keyword"]     #list

    tuName = targetUnit["Name"]             #str
    tuPiece = targetUnit["Piece"]           #str
    tuProfile = targetUnit["Profile"]       #dict
    tuWeapons = targetUnit["Weapons"]       #list
    tuCount = targetUnit["Model Count"]     #int
    tuKeywords = targetUnit["Keyword"]      #list

    return cuName, cuPiece, cuProfile, cuWeapons, cuCount, cuKeywords, tuName, tuPiece, tuProfile, tuWeapons, tuCount, tuKeywords


def generateMap():
    mapList = ["o" for i in range(50)]
    return mapList


def mapInit(
    cuPiece: str,
    tuPiece: str
):
    map = generateMap()
    cuPos = 49
    tuPos = 0
    
    map[cuPos] = cuPiece
    map[tuPos] = tuPiece
    
    return map, cuPos, tuPos


def displayMap(currMap: list, cuPos: int, tuPos: int):
    """Display the map with position indicators"""
    print("\n" + "=" * 52)
    print("".join(currMap))
    print(f"Target Unit Position: {tuPos} | Control Unit Position: {cuPos}")
    print(f"Distance between units: {cuPos - tuPos}")
    print("=" * 52 + "\n")


def movePhase(
    cuMove: int,
    tuMove: int,
    currMap: list,
    cuPos: int,
    tuPos: int,
    cuPiece: str,
    tuPiece: str
):
    """Move phase handler"""
    
    print(f"\n--- MOVE PHASE ---")
    print(f"Control Unit can move up to {cuMove} spaces")
    print(f"Target Unit will automatically move {tuMove} spaces")
    
    displayMap(currMap, cuPos, tuPos)
    
    # Get player input for control unit movement
    while True:
        try:
            cuChoice = int(input(f"Move Control Unit forward (0-{cuMove}): "))
            if 0 <= cuChoice <= cuMove:
                break
            else:
                print(f"Please enter a value between 0 and {cuMove}")
        except ValueError:
            print("INPUT NOT AN INTEGER! Please try again.")
    
    # Clear old positions
    currMap[cuPos] = "o"
    currMap[tuPos] = "o"
    
    # Calculate new positions
    newCuPos = cuPos - cuChoice
    newTuPos = tuPos + tuMove
    
    # Check for collision/engagement
    if newTuPos >= newCuPos:
        print("\n!!! UNITS ARE NOW IN ENGAGEMENT RANGE !!!")
        newTuPos = newCuPos - 1
        if newTuPos < 0:
            newTuPos = 0
            newCuPos = 1
    
    # Update map
    currMap[newCuPos] = cuPiece
    currMap[newTuPos] = tuPiece
    
    print(f"\nControl Unit moved {cuChoice} spaces forward")
    print(f"Target Unit moved {tuMove} spaces forward")
    
    displayMap(currMap, newCuPos, newTuPos)
    
    return currMap, newCuPos, newTuPos


def isRangedWeapon(weapon: dict) -> bool:
    """Check if a weapon is ranged"""
    weaponRange = weapon["range"]
    if isinstance(weaponRange, int):
        return True
    elif isinstance(weaponRange, str) and weaponRange.lower() != "melee":
        try:
            int(weaponRange)
            return True
        except:
            return False
    return False


def getRangedWeapons(weapons: list) -> list:
    """Filter and return only ranged weapons"""
    rangedWeapons = []
    for weapon in weapons:
        if isRangedWeapon(weapon):
            rangedWeapons.append(weapon)
    return rangedWeapons


def selectWeapon(weapons: list, unitName: str) -> dict:
    """Allow player to select a weapon"""
    if len(weapons) == 0:
        return None
    elif len(weapons) == 1:
        print(f"{unitName} automatically uses: {weapons[0]['name']}")
        return weapons[0]
    else:
        print(f"\n{unitName} has multiple weapons:")
        for i, weapon in enumerate(weapons):
            print(f"{i+1}. {weapon['name']} (Range: {weapon['range']}, Attacks: {weapon['a']})")
        
        while True:
            try:
                choice = int(input(f"Select weapon (1-{len(weapons)}): "))
                if 1 <= choice <= len(weapons):
                    selectedWeapon = weapons[choice-1]
                    print(f"Selected: {selectedWeapon['name']}")
                    return selectedWeapon
                else:
                    print(f"Please enter a number between 1 and {len(weapons)}")
            except ValueError:
                print("Please enter a valid number")


def rollD6() -> int:
    """Roll a single D6"""
    return rolls.rollBox(1)[0]


def rollD3() -> int:
    """Roll a D3"""
    d6Result = rollD6()
    if d6Result in [1, 2]:
        return 1
    elif d6Result in [3, 4]:
        return 2
    else:
        return 3


def parseDiceNotation(value) -> int:
    """Parse dice notation and return the result"""
    if isinstance(value, int):
        return value
    
    valueStr = str(value).upper().replace(" ", "")
    pattern = r'^(\d*)D([36])([+\-]\d+)?$'
    match = re.match(pattern, valueStr)
    
    if not match:
        try:
            return int(value)
        except:
            print(f"Warning: Could not parse '{value}', defaulting to 1")
            return 1
    
    numDice = int(match.group(1)) if match.group(1) else 1
    diceType = int(match.group(2))
    modifier = int(match.group(3)) if match.group(3) else 0
    
    total = 0
    rollResults = []
    
    if diceType == 6:
        for _ in range(numDice):
            roll = rollD6()
            rollResults.append(roll)
            total += roll
    elif diceType == 3:
        for _ in range(numDice):
            roll = rollD3()
            rollResults.append(roll)
            total += roll
    
    finalTotal = total + modifier
    
    diceNotation = f"{numDice if numDice > 1 else ''}D{diceType}"
    if modifier > 0:
        diceNotation += f"+{modifier}"
    elif modifier < 0:
        diceNotation += f"{modifier}"
    
    print(f"Rolling {diceNotation}: {rollResults} = {total}", end="")
    if modifier != 0:
        print(f" {'+' if modifier > 0 else ''}{modifier} = {finalTotal}")
    else:
        print()
    
    return max(1, finalTotal)


def getAttackCount(weapon: dict, targetDistance: int, weaponRange: int, attackerModelCount: int, 
                   targetUnitCount: int, isInEngagementRange: bool) -> int:
    """
    Calculate final attack count after applying all attack-modifying abilities
    
    Attack calculation order:
    1. Parse base attacks per model (D6+1, etc.)
    2. Multiply by number of models in unit
    3. Apply BLAST (+1 per 5 target models)
    4. Apply RAPID FIRE (+X attacks within half range)
    """
    # Parse base attacks (handles D6, D3, etc.)
    baseAttacksPerModel  = parseDiceNotation(weapon["a"])
    weaponAbilities = weapon.get("weapon abilities", [])
    
    print(f"\nBase attacks per model: {baseAttacksPerModel}")
    print(f"Number of models shooting: {attackerModelCount}")
    
    # Apply BLAST (adds attacks based on target size)
    baseAttacks = baseAttacksPerModel * attackerModelCount
    print(f"Total base attacks: {baseAttacks} ({baseAttacksPerModel} x {attackerModelCount})")
    
    baseAttacks = wad.applyBlast(baseAttacks, targetUnitCount, isInEngagementRange, weaponAbilities)

    if baseAttacks == 0:
        return 0  # BLAST blocked by engagement range
    
    # Apply RAPID FIRE (adds attacks within half range)
    finalAttacks = wad.applyRapidFire(baseAttacks, targetDistance, weaponRange, weaponAbilities)
    
    return finalAttacks


def getDamageValue(damageValue) -> int:
    """Parse damage value"""
    return parseDiceNotation(damageValue)


def hitRollPhase(weapon: dict, weaponAbilities: list, attackCount: int, 
                 isStationary: bool, didAdvance: bool, targetVisible: bool = True,
                 targetUnitAbility: dict = None, isMeleeAttack: bool = False) -> tuple:
    """
    Perform hit rolls with all modifiers applied
    
    Returns: (normalHits, criticalHits, lethalHitCrits)
    - normalHits: regular successful hits
    - criticalHits: unmodified 6s (still need to wound)
    - lethalHitCrits: unmodified 6s with LETHAL HITS (skip wound rolls)
    """
    if attackCount == 0:
        return (0, 0, 0)
    
    bs = weapon["bs"]
    
    print(f"\n--- HIT ROLL PHASE ---")
    print(f"Making {attackCount} attacks with BS {bs}+")
    
    # Get all hit modifiers
    hitMods = wad.getHitModifiers(weaponAbilities, isStationary, didAdvance)

    # ✅ CHECK FOR DEFENSIVE ABILITIES (like Deft Parry)
    if targetUnitAbility:
        if targetUnitAbility.get("trigger") == "on_defense":
            condition = targetUnitAbility.get("condition", "")
            
            # Check if condition is met
            if condition == "isMeleeAttack" and isMeleeAttack:
                modifier_value = targetUnitAbility.get("value", 0)
                print(f"=--- Target ability [{targetUnitAbility['name']}] activated! ---=")
                print(f"=--- {targetUnitAbility['modifier'].capitalize()} {modifier_value} from Hit rolls ---=")
                
                if targetUnitAbility.get("modifier") == "subtract":
                    hitMods["modifier"] -= modifier_value
                    
            elif condition == "":  # Always active if no condition
                modifier_value = targetUnitAbility.get("value", 0)
                print(f"\n=--- Target ability [{targetUnitAbility['name']}] activated! ---=")
                print(f"=--- {targetUnitAbility['modifier'].capitalize()} {modifier_value} from Hit rolls ---=")
                
                if targetUnitAbility.get("modifier") == "subtract":
                    hitMods["modifier"] -= modifier_value
    
    # Check if unit can shoot at all
    if not hitMods["canShoot"]:
        return (0, 0, 0)
    
    # TORRENT: Auto-hit
    if hitMods["autoHit"]:
        print(f"All {attackCount} attacks automatically hit!")
        return (attackCount, 0, 0)  # All normal hits, no crits from auto-hits
    
    # INDIRECT FIRE penalties
    indirectPenalty = wad.getIndirectFirePenalty(targetVisible, weaponAbilities)
    totalModifier = hitMods["modifier"] + indirectPenalty["hitModifier"]
    
    if totalModifier != 0:
        print(f"Hit roll modifier: {'+' if totalModifier > 0 else ''}{totalModifier}")
    
    # Roll dice
    hitRolls = rolls.rollBox(attackCount)
    print(f"Hit rolls: {hitRolls}")
    
    normalHits = 0
    criticalHits = 0
    lethalHitCrits = 0
    
    for roll in hitRolls:
        # INDIRECT FIRE: rolls of 1-3 always fail when target not visible
        if indirectPenalty["minHitRoll"] > 1 and roll < indirectPenalty["minHitRoll"]:
            continue
        
        # Check if hit (with modifiers)
        isHit, isCritical = wad.applyHitModifier(roll, totalModifier, bs)
        
        if not isHit:
            continue
        
        if isCritical:
            # Check for LETHAL HITS
            if wad.isLethalHits(roll, weaponAbilities):
                lethalHitCrits += 1
            else:
                criticalHits += 1
        else:
            normalHits += 1
    
    totalHits = normalHits + criticalHits
    
    print(f"Results: {normalHits} normal hits, {criticalHits} critical hits", end="")
    
    if lethalHitCrits > 0:
        print(f", {lethalHitCrits} LETHAL HITS")
        print(f"=--- Weapon ability [LETHAL HITS] activated! ---=")
        print(f"=--- {lethalHitCrits} critical hits automatically wound! ---=")
    else:
        print()
    
    return (totalHits, lethalHitCrits)


def woundRollPhase(weapon: dict, weaponAbilities: list, successfulHits: int, 
                   targetToughness: int, targetKeywords: list, didCharge: bool = False,
                   canReroll: bool = False) -> tuple:
    """
    Perform wound rolls with all modifiers applied
    
    Returns: (normalWounds, devastatingDamage)
    - normalWounds: successful wounds that need saves
    - devastatingDamage: mortal damage from DEVASTATING WOUNDS (bypasses saves)
    """
    if successfulHits == 0:
        return (0, 0)
    
    strength = weapon["s"]
    
    print(f"\n--- WOUND ROLL PHASE ---")
    print(f"Rolling {successfulHits} wound rolls (S{strength} vs T{targetToughness})")
    
    # Calculate wound threshold
    if strength >= targetToughness * 2:
        woundThreshold = 2
    elif strength > targetToughness:
        woundThreshold = 3
    elif strength == targetToughness:
        woundThreshold = 4
    elif strength < targetToughness and strength >= targetToughness / 2:
        woundThreshold = 5
    else:
        woundThreshold = 6
    
    print(f"Wound threshold: {woundThreshold}+")
    
    # Get wound modifiers (LANCE, etc.)
    woundModifier = wad.getWoundModifiers(weaponAbilities, didCharge)
    
    if woundModifier != 0:
        print(f"Wound roll modifier: {'+' if woundModifier > 0 else ''}{woundModifier}")
    
    # Check for ANTI- abilities
    hasAnti, antiThreshold = wad.hasAntiAbility(weaponAbilities, targetKeywords)
    
    if hasAnti:
        antiKeyword = None
        for ability in weaponAbilities:
            ak, at = wad.parseAntiAbility(ability)
            if ak and at == antiThreshold:
                antiKeyword = ak
                break
        print(f"=--- Weapon ability [ANTI-{antiKeyword} {antiThreshold}+] is ACTIVE! ---=")
        print(f"=--- Wound rolls of {antiThreshold}+ count as CRITICAL WOUNDS! ---=")
    
    # Check for TWIN-LINKED
    hasTwinLinked = wad.canRerollWound(weaponAbilities)
    if hasTwinLinked:
        print("=--- Weapon ability [TWIN-LINKED] available! ---=")
        print("=--- Can re-roll wound rolls ---=")
    
    # Roll wounds
    woundRolls = rolls.rollBox(successfulHits)
    print(f"Wound rolls: {woundRolls}")
    
    # If TWIN-LINKED, offer to reroll
    if hasTwinLinked:
        rerollIndices = []
        for i, roll in enumerate(woundRolls):
            modifiedRoll = roll + woundModifier
            if modifiedRoll < woundThreshold:
                rerollIndices.append(i)
        
        if rerollIndices:
            print(f"\nFailed wound rolls at indices: {rerollIndices}")
            reroll = input("Re-roll failed wounds with TWIN-LINKED? (y/n): ").lower()
            
            if reroll == 'y':
                print("Re-rolling failed wounds...")
                rerollResults = rolls.rollBox(len(rerollIndices))
                print(f"Re-roll results: {rerollResults}")
                
                for i, newRoll in zip(rerollIndices, rerollResults):
                    woundRolls[i] = newRoll
    
    # Evaluate wounds
    normalWounds = 0
    criticalWounds = 0
    
    for roll in woundRolls:
        modifiedRoll = roll + woundModifier
        
        # Check if critical wound
        isCritical = wad.checkCriticalWound(roll, weaponAbilities, targetKeywords)
        
        if isCritical:
            criticalWounds += 1
            if roll != 6:  # If it's a crit from ANTI, not natural 6
                print(f"  → Roll of {roll} is a CRITICAL WOUND (ANTI ability)")
        elif modifiedRoll >= woundThreshold:
            normalWounds += 1
    
    print(f"Results: {normalWounds} normal wounds, {criticalWounds} critical wounds")
    
    # Check for DEVASTATING WOUNDS
    devastatingDamage = 0
    
    if wad.checkDevastatingWounds(weaponAbilities) and criticalWounds > 0:
        print(f"\n=--- Weapon ability [DEVASTATING WOUNDS] activated! ---=")
        print(f"=--- {criticalWounds} critical wounds deal mortal damage! ---=")
        
        for i in range(criticalWounds):
            damage = getDamageValue(weapon, 0, 0)  # No melta for devastating wounds
            devastatingDamage += damage
            print(f"  Critical wound {i+1}: {damage} mortal damage")
        
        print(f"Total mortal damage: {devastatingDamage}")
        criticalWounds = 0  # These are now mortal wounds, not normal wounds
    
    return (normalWounds + criticalWounds, devastatingDamage)

def hitRollPhase(weapon: dict, weaponAbilities: list, attackCount: int, 
                 isStationary: bool, didAdvance: bool, targetVisible: bool = True) -> tuple:
    """
    Perform hit rolls with all modifiers applied
    
    Returns: (normalHits, criticalHits, lethalHitCrits)
    - normalHits: regular successful hits
    - criticalHits: unmodified 6s (still need to wound)
    - lethalHitCrits: unmodified 6s with LETHAL HITS (skip wound rolls)
    """
    if attackCount == 0:
        return (0, 0, 0)
    
    bs = weapon["bs"]
    
    print(f"\n--- HIT ROLL PHASE ---")
    print(f"Making {attackCount} attacks with BS {bs}+")
    
    # Get all hit modifiers
    hitMods = wad.getHitModifiers(weaponAbilities, isStationary, didAdvance)
    
    # Check if unit can shoot at all
    if not hitMods["canShoot"]:
        return (0, 0, 0)
    
    # TORRENT: Auto-hit
    if hitMods["autoHit"]:
        print(f"All {attackCount} attacks automatically hit!")
        return (attackCount, 0, 0)  # All normal hits, no crits from auto-hits
    
    # INDIRECT FIRE penalties
    indirectPenalty = wad.getIndirectFirePenalty(targetVisible, weaponAbilities)
    totalModifier = hitMods["modifier"] + indirectPenalty["hitModifier"]
    
    if totalModifier != 0:
        print(f"Hit roll modifier: {'+' if totalModifier > 0 else ''}{totalModifier}")
    
    # Roll dice
    hitRolls = rolls.rollBox(attackCount)
    print(f"Hit rolls: {hitRolls}")
    
    normalHits = 0
    criticalHits = 0
    lethalHitCrits = 0
    
    for roll in hitRolls:
        # INDIRECT FIRE: rolls of 1-3 always fail when target not visible
        if indirectPenalty["minHitRoll"] > 1 and roll < indirectPenalty["minHitRoll"]:
            continue
        
        # Check if hit (with modifiers)
        isHit, isCritical = wad.applyHitModifier(roll, totalModifier, bs)
        
        if not isHit:
            continue
        
        if isCritical:
            # Check for LETHAL HITS
            if wad.isLethalHits(roll, weaponAbilities):
                lethalHitCrits += 1
            else:
                criticalHits += 1
        else:
            normalHits += 1
    
    totalHits = normalHits + criticalHits
    
    print(f"Results: {normalHits} normal hits, {criticalHits} critical hits", end="")
    
    if lethalHitCrits > 0:
        print(f", {lethalHitCrits} LETHAL HITS")
        print(f"=--- Weapon ability [LETHAL HITS] activated! ---=")
        print(f"=--- {lethalHitCrits} critical hits automatically wound! ---=")
    else:
        print()
    
    return (totalHits, lethalHitCrits)


def woundRollPhase(weapon: dict, weaponAbilities: list, successfulHits: int, 
                   targetToughness: int, targetKeywords: list, didCharge: bool = False,
                   canReroll: bool = False) -> tuple:
    """
    Perform wound rolls with all modifiers applied
    
    Returns: (normalWounds, devastatingDamage)
    - normalWounds: successful wounds that need saves
    - devastatingDamage: mortal damage from DEVASTATING WOUNDS (bypasses saves)
    """
    if successfulHits == 0:
        return (0, 0)
    
    strength = weapon["s"]
    
    print(f"\n--- WOUND ROLL PHASE ---")
    print(f"Rolling {successfulHits} wound rolls (S{strength} vs T{targetToughness})")
    
    # Calculate wound threshold
    if strength >= targetToughness * 2:
        woundThreshold = 2
    elif strength > targetToughness:
        woundThreshold = 3
    elif strength == targetToughness:
        woundThreshold = 4
    elif strength < targetToughness and strength >= targetToughness / 2:
        woundThreshold = 5
    else:
        woundThreshold = 6
    
    print(f"Wound threshold: {woundThreshold}+")
    
    # Get wound modifiers (LANCE, etc.)
    woundModifier = wad.getWoundModifiers(weaponAbilities, didCharge)
    
    if woundModifier != 0:
        print(f"Wound roll modifier: {'+' if woundModifier > 0 else ''}{woundModifier}")
    
    # Check for ANTI- abilities
    hasAnti, antiThreshold = wad.hasAntiAbility(weaponAbilities, targetKeywords)
    
    if hasAnti:
        antiKeyword = None
        for ability in weaponAbilities:
            ak, at = wad.parseAntiAbility(ability)
            if ak and at == antiThreshold:
                antiKeyword = ak
                break
        print(f"=--- Weapon ability [ANTI-{antiKeyword} {antiThreshold}+] is ACTIVE! ---=")
        print(f"=--- Wound rolls of {antiThreshold}+ count as CRITICAL WOUNDS! ---=")
    
    # Check for TWIN-LINKED
    hasTwinLinked = wad.canRerollWound(weaponAbilities)
    if hasTwinLinked:
        print("=--- Weapon ability [TWIN-LINKED] available! ---=")
        print("=--- Can re-roll wound rolls ---=")
    
    # Roll wounds
    woundRolls = rolls.rollBox(successfulHits)
    print(f"Wound rolls: {woundRolls}")
    
    # If TWIN-LINKED, offer to reroll
    if hasTwinLinked:
        rerollIndices = []
        for i, roll in enumerate(woundRolls):
            modifiedRoll = roll + woundModifier
            if modifiedRoll < woundThreshold:
                rerollIndices.append(i)
        
        if rerollIndices:
            print(f"\nFailed wound rolls at indices: {rerollIndices}")
            reroll = input("Re-roll failed wounds with TWIN-LINKED? (y/n): ").lower()
            
            if reroll == 'y':
                print("Re-rolling failed wounds...")
                rerollResults = rolls.rollBox(len(rerollIndices))
                print(f"Re-roll results: {rerollResults}")
                
                for i, newRoll in zip(rerollIndices, rerollResults):
                    woundRolls[i] = newRoll
    
    # Evaluate wounds
    normalWounds = 0
    criticalWounds = 0
    
    for roll in woundRolls:
        modifiedRoll = roll + woundModifier
        
        # Check if critical wound
        isCritical = wad.checkCriticalWound(roll, weaponAbilities, targetKeywords)
        
        if isCritical:
            criticalWounds += 1
            if roll != 6:  # If it's a crit from ANTI, not natural 6
                print(f"  → Roll of {roll} is a CRITICAL WOUND (ANTI ability)")
        elif modifiedRoll >= woundThreshold:
            normalWounds += 1
    
    print(f"Results: {normalWounds} normal wounds, {criticalWounds} critical wounds")
    
    # Check for DEVASTATING WOUNDS
    devastatingDamage = 0
    
    if wad.checkDevastatingWounds(weaponAbilities) and criticalWounds > 0:
        print(f"\n=--- Weapon ability [DEVASTATING WOUNDS] activated! ---=")
        print(f"=--- {criticalWounds} critical wounds deal mortal damage! ---=")
        
        for i in range(criticalWounds):
            damage = getDamageValue(weapon, 0, 0)  # No melta for devastating wounds
            devastatingDamage += damage
            print(f"  Critical wound {i+1}: {damage} mortal damage")
        
        print(f"Total mortal damage: {devastatingDamage}")
        criticalWounds = 0  # These are now mortal wounds, not normal wounds
    
    return (normalWounds + criticalWounds, devastatingDamage)


def getDamageValue(weapon: dict, targetDistance: int, weaponRange: int) -> int:
    """
    Parse damage value and apply MELTA if applicable
    """
    baseDamage = parseDiceNotation(weapon["d"])
    weaponAbilities = weapon.get("weapon abilities", [])
    
    # Apply MELTA bonus
    finalDamage = wad.applyMelta(baseDamage, targetDistance, weaponRange, weaponAbilities)
    
    return finalDamage


def saveRollPhase(weapon: dict, targetProfile: dict, normalWounds: int, 
                  targetHasCover: bool = False, targetDistance: int = 0, 
                  weaponRange: int = 0) -> int:
    """
    Perform save rolls
    
    Returns: failed saves (damage to allocate)
    """
    if normalWounds == 0:
        return 0
    
    weaponAbilities = weapon.get("weapon abilities", [])
    save = targetProfile["sv"]
    invSave = targetProfile.get("inv-sv", 7)
    ap = abs(weapon["ap"])
    
    print(f"\n--- SAVE ROLL PHASE ---")
    print(f"Target must make {normalWounds} save rolls")
    
    # Check IGNORES COVER
    effectiveCover = wad.targetHasCover(targetHasCover, weaponAbilities)
    
    if effectiveCover:
        save -= 1  # Cover gives +1 to save (lower is better)
        print(f"Target has Benefit of Cover (+1 to save)")
    
    # Calculate effective save
    modifiedSave = save + ap
    
    if invSave < modifiedSave:
        saveToUse = invSave
        print(f"Using Invulnerable Save: {saveToUse}+ (AP ignored)")
    else:
        saveToUse = modifiedSave
        print(f"Using Armor Save: {save}+ (modified to {saveToUse}+ by AP-{ap})")
    
    # Roll saves
    saveRolls = rolls.rollBox(normalWounds)
    print(f"Save rolls: {saveRolls}")
    
    failedSaves = 0
    for roll in saveRolls:
        if roll < saveToUse:
            failedSaves += 1
    
    print(f"Results: {failedSaves} failed saves")
    
    return failedSaves


def allocateDamage(weapon: dict, failedSaves: int, lethalHits: int, devastatingDamage: int, 
                   targetProfile: dict, targetModelCount: int, targetCurrentWounds: int, 
                   targetDistance: int, weaponRange: int) -> tuple:
    """
    Allocate damage to target
    
    Returns: (remaining models, current wounds on damaged model)
    """
    modelWounds = targetProfile["w"]
    
    print(f"\n--- DAMAGE ALLOCATION ---")
    print(f"Target has {targetModelCount} models with {modelWounds} wounds each")
    
    totalDamageInstances = failedSaves + lethalHits
    
    if totalDamageInstances > 0:
        print(f"Weapon damage: {weapon['d']} per failed save")
    
    currentModelWounds = targetCurrentWounds
    modelsRemaining = targetModelCount
    
    # Allocate normal damage
    for i in range(totalDamageInstances):
        damage = getDamageValue(weapon, targetDistance, weaponRange)
        
        damageDealt = min(damage, currentModelWounds)
        currentModelWounds -= damageDealt
        
        print(f"Damage instance {i+1}: {damage} damage rolled, {damageDealt} damage dealt", end="")
        
        if currentModelWounds <= 0:
            modelsRemaining -= 1
            print(f" - Model destroyed! ({modelsRemaining} remaining)")
            currentModelWounds = modelWounds
            
            if modelsRemaining <= 0:
                break
        else:
            print(f" - Model has {currentModelWounds}/{modelWounds} wounds remaining")
    
    # Allocate mortal damage (DEVASTATING WOUNDS)
    if devastatingDamage > 0:
        print(f"\nApplying {devastatingDamage} mortal damage")
        while devastatingDamage > 0 and modelsRemaining > 0:
            damageToModel = min(devastatingDamage, currentModelWounds)
            currentModelWounds -= damageToModel
            devastatingDamage -= damageToModel
            
            if currentModelWounds <= 0:
                modelsRemaining -= 1
                print(f"Model destroyed by mortal damage! ({modelsRemaining} remaining)")
                currentModelWounds = modelWounds
    
    print(f"\nFinal result: {modelsRemaining} models remaining")
    
    return (modelsRemaining, currentModelWounds if modelsRemaining > 0 else modelWounds)


def shootingPhase(attackerWeapons: list, attackerProfile: dict, 
                  targetProfile: dict, targetUnit: dict,  # ✅ ADD FULL TARGET UNIT
                  attackerModelCount: int, 
                  targetModelCount: int, targetCurrentWounds: int, distance: int, 
                  attackerName: str, targetName: str, 
                  targetKeywords: list, isStationary: bool = False, didAdvance: bool = False,
                  didCharge: bool = False, targetHasCover: bool = False) -> tuple:
    """
    Complete shooting phase with all weapon abilities
    
    New parameters:
    - isStationary: Did the unit remain stationary? (affects HEAVY)
    - didAdvance: Did the unit advance? (affects ASSAULT requirement)
    - didCharge: Did the unit charge? (affects LANCE)
    - targetHasCover: Does target have cover? (affected by IGNORES COVER)
    
    Returns: (remaining model count, current wounds, hazardous mortal wounds)
    """
    rangedWeapons = getRangedWeapons(attackerWeapons)
    
    if len(rangedWeapons) == 0:
        print(f"{attackerName} has no ranged weapons!")
        return (targetModelCount, targetProfile["w"], 0)
    
    isEngaged = distance <= 3
    
    # Check engagement range restrictions
    if isEngaged:
        print(f"Units are in engagement range (distance: {distance})")
        eligibleWeapons = [w for w in rangedWeapons if wad.isPistol(w.get("weapon abilities", []))]
        if len(eligibleWeapons) == 0:
            print(f"{attackerName} cannot shoot - no PISTOL weapons!")
            return (targetModelCount, targetProfile["w"], 0)
        rangedWeapons = eligibleWeapons
    
    # Select weapon
    selectedWeapon = selectWeapon(rangedWeapons, attackerName)
    if selectedWeapon is None:
        return (targetModelCount, targetProfile["w"], 0)
    
    weaponRange = selectedWeapon["range"]
    
    # Check range
    if distance > weaponRange:
        print(f"{selectedWeapon['name']} out of range! (Distance: {distance}, Range: {weaponRange})")
        return (targetModelCount, targetProfile["w"], 0)
    
    print(f"\n{'='*60}")
    print(f"{attackerName} fires {selectedWeapon['name']} at {targetName}!")
    print(f"Distance: {distance}\", Weapon Range: {weaponRange}\"")
    print(f"{'='*60}")
    
    weaponAbilities = selectedWeapon.get("weapon abilities", [])
    wad.displayActiveAbilities(weaponAbilities, targetKeywords)
    
    # PHASE 1: Calculate attack count (BLAST, RAPID FIRE apply here)
    attackCount = getAttackCount(selectedWeapon, distance, weaponRange, attackerModelCount, 
                                  targetModelCount, isEngaged)
    
    if attackCount == 0:
        print("\nCannot make attacks!")
        return (targetModelCount, targetProfile["w"], 0)
        
    if attackCount == 0:
        print("\nCannot make attacks!")
        return (targetModelCount, targetProfile["w"], 0)
    
    # ✅ Determine if this is a melee attack
    isMelee = selectedWeapon["range"] == "Melee" or (isinstance(selectedWeapon["range"], int) and selectedWeapon["range"] <= 2)
    
    # ✅ Get target's unit ability from full unit dict
    targetAbility = targetUnit.get("Ability", None)
    
    # PHASE 2: Hit rolls (HEAVY, TORRENT, LETHAL HITS apply here)
    normalHits, lethalHitCrits = hitRollPhase(
        selectedWeapon, weaponAbilities, attackCount, 
        isStationary, didAdvance,
        targetVisible=True,
        targetUnitAbility=targetAbility,
        isMeleeAttack=isMelee
    )
    
    if normalHits == 0 and lethalHitCrits == 0:
        print("\nAll attacks missed!")
        return (targetModelCount, targetProfile["w"], 0)
    
    # PHASE 3: Wound rolls (ANTI, LANCE, TWIN-LINKED, DEVASTATING WOUNDS apply here)
    normalWounds, devastatingDamage = woundRollPhase(
        selectedWeapon, weaponAbilities, normalHits, 
        targetProfile["t"], targetKeywords, didCharge
    )
    
    if normalWounds == 0 and lethalHitCrits == 0 and devastatingDamage == 0:
        print("\nAll wounds failed!")
        return (targetModelCount, targetProfile["w"], 0)
    
    # PHASE 4: Save rolls (IGNORES COVER applies here)
    failedSaves = saveRollPhase(
        selectedWeapon, targetProfile, normalWounds, 
        targetHasCover, distance, weaponRange
    )
    
    # PHASE 5: Damage allocation (MELTA applies here)
    remainingModels, currentWounds = allocateDamage(
        selectedWeapon, failedSaves, lethalHitCrits, devastatingDamage,
        targetProfile, targetModelCount, targetCurrentWounds,
        distance, weaponRange
    )
    
    # PHASE 6: Hazardous tests
    hazardousDamage = wad.performHazardousTests(weaponAbilities, attackCount)
    
    return (remainingModels, currentWounds, hazardousDamage)