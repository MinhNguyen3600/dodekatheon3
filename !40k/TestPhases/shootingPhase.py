"""
Shooting Phase implementation - Complete attack sequence
"""

import rolls as rolls
import weaponAbilityDict as wad
from .utilityFunctions import parseDiceNotation

def applyReorderReality(targetAbility: dict, distance: int, weaponAbilities: list) -> list:
    """
    Apply Vashtorr's "Reorder Reality" ability
    
    Official Rule: "Each time an enemy unit within 18" of this model targets this model, 
    subtract 1 from the Hit roll and, until the end of the phase, that enemy unit's 
    ranged weapons have the [HAZARDOUS] ability."
    
    Returns: Modified weapon abilities list with HAZARDOUS added if applicable
    """
    if not targetAbility or targetAbility.get("name") != "Reorder Reality":
        return weaponAbilities
    
    # Check if within 18"
    if distance > 18:
        return weaponAbilities
    
    # Check if effects include addHazardous
    effects = targetAbility.get("effects", [])
    for effect in effects:
        if effect.get("type") == "addHazardous":
            # Add HAZARDOUS to weapon abilities
            modifiedAbilities = weaponAbilities.copy()
            if "HAZARDOUS" not in modifiedAbilities:
                modifiedAbilities.append("HAZARDOUS")
                print(f"\n⚠️ [REORDER REALITY] activated!")
                print(f"   Weapon gains [HAZARDOUS] until end of phase!")
            return modifiedAbilities
    
    return weaponAbilities

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
        weaponRange = weapon.get("range")
        if weaponRange != "Melee" and weaponRange is not None:
            rangedWeapons.append(weapon)
    return rangedWeapons


def selectWeapon(weapons: list, unitName: str, distance: int, isInEngagement: bool) -> dict:
    """Allow player to select a weapon"""
    if len(weapons) == 0:
        return None
    elif len(weapons) == 1:
        print(f"{unitName} automatically uses: {weapons[0]['name']}")
        return weapons[0]
    else:
        if isInEngagement:
            print(f"\nUnits are in engagement range (distance: {distance})")
        
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
    baseAttacksPerModel = parseDiceNotation(weapon["a"])
    weaponAbilities = weapon.get("weapon abilities", [])
    
    print(f"\nBase attacks per model: {baseAttacksPerModel}")
    print(f"Number of models shooting: {attackerModelCount}")
    
    baseAttacks = baseAttacksPerModel * attackerModelCount
    print(f"Total base attacks: {baseAttacks} ({baseAttacksPerModel} x {attackerModelCount})")
    
    baseAttacks = wad.applyBlast(baseAttacks, targetUnitCount, isInEngagementRange, weaponAbilities)
    
    if baseAttacks == 0:
        return 0
    
    finalAttacks = wad.applyRapidFire(baseAttacks, targetDistance, weaponRange, weaponAbilities)
    
    return finalAttacks


def getDamageValue(weapon: dict, targetDistance: int, weaponRange: int) -> int:
    """Parse damage value and apply MELTA if applicable"""
    baseDamage = parseDiceNotation(weapon["d"])
    weaponAbilities = weapon.get("weapon abilities", [])
    
    finalDamage = wad.applyMelta(baseDamage, targetDistance, weaponRange, weaponAbilities)
    
    return finalDamage

"""
Shooting Phase implementation - Complete attack sequence
(Continued)
"""

def hitRollPhase(weapon: dict, weaponAbilities: list, attackCount: int, 
                 isStationary: bool, didAdvance: bool, targetVisible: bool = True,
                 targetUnitAbility: dict = None, isMeleeAttack: bool = False,
                 distance: int = 0) -> tuple:
    """
    Perform hit rolls with all modifiers applied
    
    Returns: (normalHits, lethalHitCrits)
    - normalHits: regular successful hits
    - lethalHitCrits: unmodified 6s with LETHAL HITS (skip wound rolls)
    """
    if attackCount == 0:
        return (0, 0)
    
    bs = weapon["bs"]
    
    print(f"\n--- HIT ROLL PHASE ---")
    print(f"Making {attackCount} attacks with BS {bs}+")
    
    # Get all hit modifiers
    hitMods = wad.getHitModifiers(weaponAbilities, isStationary, didAdvance)

    # ✅ CHECK FOR DEFENSIVE ABILITIES
    if targetUnitAbility:
        if targetUnitAbility.get("trigger") == "on_defense":
            condition = targetUnitAbility.get("condition", "")
            
            # ✅ Handle "Reorder Reality" (Vashtorr)
            if condition == "attackerWithin18" and distance <= 18:
                # Check effects array
                effects = targetUnitAbility.get("effects", [])
                for effect in effects:
                    if effect.get("type") == "hitModifier":
                        modifier_value = effect.get("value", 0)
                        print(f"\n⚠️ [REORDER REALITY] activated!")
                        print(f"   Subtract {abs(modifier_value)} from Hit rolls!")
                        hitMods["modifier"] += modifier_value  # Add negative value
            
            # Handle "Deft Parry" (Aleya) - melee only
            elif condition == "isMeleeAttack" and isMeleeAttack:
                modifier_value = targetUnitAbility.get("value", 0)
                print(f"=--- Target ability [{targetUnitAbility['name']}] activated! ---=")
                print(f"=--- Subtract {modifier_value} from Hit rolls ---=")
                hitMods["modifier"] -= modifier_value
            
            # Handle always-active abilities
            elif condition == "":
                modifier_value = targetUnitAbility.get("value", 0)
                print(f"\n=--- Target ability [{targetUnitAbility['name']}] activated! ---=")
                print(f"=--- Subtract {modifier_value} from Hit rolls ---=")
                hitMods["modifier"] -= modifier_value
    
    # Check if unit can shoot at all
    if not hitMods["canShoot"]:
        return (0, 0)
    
    # TORRENT: Auto-hit
    if hitMods["autoHit"]:
        print(f"All {attackCount} attacks automatically hit!")
        return (attackCount, 0)
    
    # INDIRECT FIRE penalties
    indirectPenalty = wad.getIndirectFirePenalty(targetVisible, weaponAbilities)
    totalModifier = hitMods["modifier"] + indirectPenalty["hitModifier"]
    
    if totalModifier != 0:
        print(f"Hit roll modifier: {'+' if totalModifier > 0 else ''}{totalModifier}")
    
    # Roll dice
    hitRolls = rolls.rollBox(attackCount)
    print(f"Hit rolls: {hitRolls}")
    
    normalHits = 0
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
                normalHits += 1  # Crits that aren't lethal still count as hits
        else:
            normalHits += 1
    
    print(f"Results: {normalHits} normal hits", end="")
    
    if lethalHitCrits > 0:
        print(f", {lethalHitCrits} LETHAL HITS")
        print(f"=--- Weapon ability [LETHAL HITS] activated! ---=")
        print(f"=--- {lethalHitCrits} critical hits automatically wound! ---=")
    else:
        print()
    
    return (normalHits, lethalHitCrits)


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
            if roll != 6:
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
            damage = parseDiceNotation(weapon["d"])
            devastatingDamage += damage
            print(f"  Critical wound {i+1}: {damage} mortal damage")
        
        print(f"Total mortal damage: {devastatingDamage}")
        criticalWounds = 0
    
    return (normalWounds + criticalWounds, devastatingDamage)


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
        save -= 1
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

def getRangedWeaponsInEngagement(weapons: list, attackerProfile: dict) -> list:
    """Filter weapons that can be used in engagement range"""
    eligibleWeapons = []
    
    for weapon in weapons:
        weaponRange = weapon.get("range")
        weaponAbilities = weapon.get("weapon abilities", [])
        
        # PISTOL weapons can always be used
        if "PISTOL" in weaponAbilities:
            eligibleWeapons.append(weapon)
    
    return eligibleWeapons

def resolveRangedAttacks(weapon: dict, weaponAbilities: list, attackCount: int,
                         attackerProfile: dict, targetProfile: dict, targetUnit: dict,
                         targetModelCount: int, targetCurrentWounds: int,
                         attackerName: str, targetName: str, targetKeywords: list,
                         isStationary: bool, targetHasCover: bool, distance: int) -> tuple:
    """
    Resolve ranged attacks
    
    Returns:
        tuple: (remaining models, current wounds, hazardous damage, combat_stats dict)
    """
    
    # Initialize combat stats
    combat_stats = {
        "total_hits": 0,
        "total_wounds": 0,
        "failed_saves": 0,
        "damage_dealt": 0,
        "models_destroyed": 0,
        "special_effects": []
    }
    
    if attackCount == 0:
        return (targetModelCount, targetCurrentWounds, 0, combat_stats)
    
    bs = weapon["bs"]
    
    # HIT ROLLS
    print(f"\n--- HIT ROLLS ---")
    print(f"Making {attackCount} attacks with BS {bs}+")
    
    # Check for TORRENT (auto-hit)
    if wad.hasTorrent(weaponAbilities):
        normalHits = attackCount
        lethalHitCrits = 0
        print(f"=--- Weapon ability [TORRENT] activated! ---=")
        print(f"All {attackCount} attacks automatically hit!")
        combat_stats["special_effects"].append("TORRENT: Auto-hit")
    else:
        # Calculate hit modifiers
        hitModifier = 0
        
        # HEAVY bonus if stationary
        if wad.hasHeavy(weaponAbilities) and isStationary:
            hitModifier += 1
            print(f"=--- Weapon ability [HEAVY] activated! ---=")
            print(f"Unit remained stationary: +1 to Hit rolls")
            combat_stats["special_effects"].append("HEAVY: +1 to hit (stationary)")
        
        # Check target's defensive abilities
        targetAbility = targetUnit.get("Ability", None)
        if targetAbility and targetAbility.get("trigger") == "on_defense":
            condition = targetAbility.get("condition", "")
            
            # Reorder Reality (Vashtorr)
            if condition == "attackerWithin18" and distance <= 18:
                effects = targetAbility.get("effects", [])
                for effect in effects:
                    if effect.get("type") == "hitModifier":
                        modifier_value = effect.get("value", 0)
                        print(f"\n⚠️ [REORDER REALITY] activated!")
                        print(f"   Subtract {abs(modifier_value)} from Hit rolls!")
                        hitModifier += modifier_value
                        combat_stats["special_effects"].append(f"REORDER REALITY: {modifier_value} to hit")
            
            # STEALTH
            elif condition == "hasStealthKeyword" or "STEALTH" in targetKeywords:
                hitModifier -= 1
                print(f"\n⚠️ Target has [STEALTH]!")
                print(f"   Subtract 1 from Hit rolls")
                combat_stats["special_effects"].append("STEALTH: -1 to hit")
        
        if hitModifier != 0:
            print(f"Hit roll modifier: {hitModifier:+d}")
        
        # Roll hits
        hitRolls = rolls.rollBox(attackCount)
        print(f"Hit rolls: {hitRolls}")
        
        normalHits = 0
        lethalHitCrits = 0
        
        for roll in hitRolls:
            modifiedRoll = roll + hitModifier
            
            # Unmodified 1 always fails
            if roll == 1:
                continue
            
            # Unmodified 6 is critical hit
            isCritical = (roll == 6)
            
            # Check if hit succeeds
            if modifiedRoll >= bs or isCritical:
                if isCritical and wad.isLethalHits(roll, weaponAbilities):
                    lethalHitCrits += 1
                else:
                    normalHits += 1
        
        print(f"Results: {normalHits} normal hits", end="")
        if lethalHitCrits > 0:
            print(f", {lethalHitCrits} LETHAL HITS")
            combat_stats["special_effects"].append(f"LETHAL HITS: {lethalHitCrits} auto-wounds")
        else:
            print()
    
    # ✅ TRACK TOTAL HITS
    combat_stats["total_hits"] = normalHits + lethalHitCrits
    
    if normalHits == 0 and lethalHitCrits == 0:
        print("\nAll attacks missed!")
        return (targetModelCount, targetCurrentWounds, 0, combat_stats)
    
    # WOUND ROLLS
    print(f"\n--- WOUND ROLLS ---")
    
    strength = weapon["s"]
    toughness = targetProfile["t"]
    
    print(f"Rolling {normalHits} wound rolls (S{strength} vs T{toughness})")
    
    # Calculate wound threshold
    if strength >= toughness * 2:
        woundThreshold = 2
    elif strength > toughness:
        woundThreshold = 3
    elif strength == toughness:
        woundThreshold = 4
    elif strength < toughness and strength >= toughness / 2:
        woundThreshold = 5
    else:
        woundThreshold = 6
    
    print(f"Wound threshold: {woundThreshold}+")
    
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
        combat_stats["special_effects"].append(f"ANTI-{antiKeyword} {antiThreshold}+")
    
    # Roll wounds
    woundRolls = rolls.rollBox(normalHits)
    print(f"Wound rolls: {woundRolls}")
    
    normalWounds = 0
    criticalWounds = 0
    
    for roll in woundRolls:
        # Check if critical wound
        isCritical = wad.checkCriticalWound(roll, weaponAbilities, targetKeywords)
        
        if isCritical:
            criticalWounds += 1
        elif roll >= woundThreshold:
            normalWounds += 1
    
    # ✅ TRACK TOTAL WOUNDS (including lethal hits)
    combat_stats["total_wounds"] = normalWounds + criticalWounds + lethalHitCrits
    
    print(f"Results: {normalWounds} normal wounds, {criticalWounds} critical wounds")
    
    # Handle DEVASTATING WOUNDS
    devastatingDamage = 0
    if wad.checkDevastatingWounds(weaponAbilities) and criticalWounds > 0:
        print(f"\n=--- Weapon ability [DEVASTATING WOUNDS] activated! ---=")
        for i in range(criticalWounds):
            damage = parseDiceNotation(weapon["d"])
            devastatingDamage += damage
        print(f"Total mortal damage: {devastatingDamage}")
        combat_stats["special_effects"].append(f"DEVASTATING WOUNDS: {devastatingDamage} mortal damage")
        criticalWounds = 0  # These become mortal wounds, no saves
    
    totalWounds = normalWounds + criticalWounds + lethalHitCrits  # ✅ INCLUDE LETHAL HITS
    
    if totalWounds == 0 and devastatingDamage == 0:
        print("\nAll wounds failed!")
        return (targetModelCount, targetCurrentWounds, 0, combat_stats)
    
    # SAVE ROLLS
    print(f"\n--- SAVE ROLLS ---")
    print(f"Target must make {totalWounds} save rolls")
    
    save = targetProfile["sv"]
    invSave = targetProfile.get("inv-sv", 7)
    ap = abs(weapon["ap"])
    
    # Check for IGNORES COVER
    ignoresCover = wad.hasIgnoresCover(weaponAbilities)
    if ignoresCover and targetHasCover:
        print(f"=--- Weapon ability [IGNORES COVER] activated! ---=")
        print(f"Target's cover is negated")
        targetHasCover = False
        combat_stats["special_effects"].append("IGNORES COVER")
    
    # Apply cover modifier
    coverModifier = 0
    if targetHasCover and not ignoresCover:
        coverModifier = 1
        print(f"Target has cover: +1 to armor saves")
        combat_stats["special_effects"].append("Target has cover: +1 save")
    
    modifiedSave = save + ap - coverModifier
    
    if invSave < modifiedSave:
        saveToUse = invSave
        print(f"Using Invulnerable Save: {saveToUse}+")
    else:
        saveToUse = modifiedSave
        if coverModifier > 0:
            print(f"Using Armor Save: {save}+ (modified to {saveToUse}+ by AP-{ap} and +1 cover)")
        else:
            print(f"Using Armor Save: {save}+ (modified to {saveToUse}+ by AP-{ap})")
    
    saveRolls = rolls.rollBox(totalWounds)
    print(f"Save rolls: {saveRolls}")
    
    failedSaves = sum(1 for roll in saveRolls if roll < saveToUse)
    
    # ✅ TRACK FAILED SAVES
    combat_stats["failed_saves"] = failedSaves
    
    print(f"Results: {failedSaves} failed saves")
    
    # DAMAGE ALLOCATION
    print(f"\n--- DAMAGE ALLOCATION ---")
    
    modelWounds = targetProfile["w"]
    currentModelWounds = targetCurrentWounds
    modelsRemaining = targetModelCount
    
    initialModels = targetModelCount
    initialWounds = targetCurrentWounds
    
    # ✅ CHECK FOR FEEL NO PAIN
    hasFNP, fnpThreshold = wad.checkFeelNoPain(targetUnit)
    
    if hasFNP:
        print(f"✓ Target has FEEL NO PAIN {fnpThreshold}+")
    
    totalDamageInstances = failedSaves
    
    # Check for MELTA bonus
    meltaBonus = wad.getMeltaBonus(weaponAbilities, distance, weapon.get("range"))
    if meltaBonus > 0:
        print(f"\n=--- Weapon ability [MELTA {meltaBonus}] activated! ---=")
        print(f"Target within half range: +{meltaBonus} damage")
        combat_stats["special_effects"].append(f"MELTA: +{meltaBonus} damage")
    
    # Allocate normal damage
    for i in range(totalDamageInstances):
        baseDamage = parseDiceNotation(weapon["d"])
        totalDamage = baseDamage + meltaBonus
        
        # ✅ APPLY FEEL NO PAIN
        if hasFNP:
            actualDamage = wad.applyFeelNoPain(totalDamage, fnpThreshold, targetName)
        else:
            actualDamage = totalDamage
        
        if actualDamage <= 0:
            print(f"Damage instance {i+1}: {totalDamage} damage rolled, all ignored by FNP!")
            continue
        
        damageDealt = min(actualDamage, currentModelWounds)
        currentModelWounds -= damageDealt
        
        print(f"Damage instance {i+1}: {totalDamage} → {actualDamage} after FNP → {damageDealt} dealt", end="")
        
        if currentModelWounds <= 0:
            modelsRemaining -= 1
            print(f" - Model destroyed! ({modelsRemaining} remaining)")
            currentModelWounds = modelWounds
            if modelsRemaining <= 0:
                break
        else:
            print(f" - Model has {currentModelWounds}/{modelWounds} wounds")
    
    # Allocate mortal damage from Devastating Wounds
    if devastatingDamage > 0:
        print(f"\nApplying {devastatingDamage} mortal damage")
        
        # ✅ FNP APPLIES TO MORTAL WOUNDS
        if hasFNP:
            devastatingDamage = wad.applyFeelNoPain(devastatingDamage, fnpThreshold, targetName)
            if devastatingDamage <= 0:
                print(f"All mortal wounds ignored by FNP!")
        
        while devastatingDamage > 0 and modelsRemaining > 0:
            damageToModel = min(devastatingDamage, currentModelWounds)
            currentModelWounds -= damageToModel
            devastatingDamage -= damageToModel
            
            if currentModelWounds <= 0:
                modelsRemaining -= 1
                print(f"Model destroyed by mortal damage! ({modelsRemaining} remaining)")
                currentModelWounds = modelWounds
    
    # ✅ CALCULATE ACTUAL DAMAGE DEALT
    if initialModels > modelsRemaining:
        models_lost = initialModels - modelsRemaining
        combat_stats["models_destroyed"] = models_lost
        if modelsRemaining > 0:
            combat_stats["damage_dealt"] = (models_lost * modelWounds) - (modelWounds - initialWounds) + (modelWounds - currentModelWounds)
        else:
            combat_stats["damage_dealt"] = (models_lost - 1) * modelWounds + initialWounds
    else:
        combat_stats["damage_dealt"] = initialWounds - currentModelWounds
    
    print(f"\nFinal result: {modelsRemaining} models remaining")
    
    # CHECK FOR HAZARDOUS
    hazardousDamage = 0
    if wad.hasHazardous(weaponAbilities):
        print(f"\n--- HAZARDOUS TEST ---")
        print(f"Rolling Hazardous test for {weapon['name']}...")
        hazardRoll = rolls.rollBox(1)[0]
        print(f"Hazardous roll: {hazardRoll}")
        
        if hazardRoll == 1:
            hazardousDamage = 3
            print(f"⚠️ HAZARDOUS TEST FAILED!")
            print(f"{attackerName} suffers 3 mortal wounds!")
            combat_stats["special_effects"].append("HAZARDOUS: 3 mortal wounds to shooter")
        else:
            print(f"✓ Hazardous test passed")
    
    # Check for Reorder Reality's HAZARDOUS effect
    targetAbility = targetUnit.get("Ability", None)
    if targetAbility and targetAbility.get("trigger") == "on_defense":
        condition = targetAbility.get("condition", "")
        if condition == "attackerWithin18" and distance <= 18:
            effects = targetAbility.get("effects", [])
            for effect in effects:
                if effect.get("type") == "weaponModifier" and effect.get("value") == "HAZARDOUS":
                    print(f"\n--- REORDER REALITY HAZARDOUS TEST ---")
                    print(f"Weapon gains HAZARDOUS from Reorder Reality...")
                    hazardRoll = rolls.rollBox(1)[0]
                    print(f"Hazardous roll: {hazardRoll}")
                    
                    if hazardRoll == 1:
                        hazardousDamage += 3
                        print(f"⚠️ HAZARDOUS TEST FAILED!")
                        print(f"{attackerName} suffers 3 mortal wounds!")
                        combat_stats["special_effects"].append("Reorder Reality HAZARDOUS: 3 mortal wounds")
                    else:
                        print(f"✓ Hazardous test passed")
    
    return (modelsRemaining, currentModelWounds if modelsRemaining > 0 else modelWounds, hazardousDamage, combat_stats)

def resolveWeaponAttacks(weapon: dict, attackerProfile: dict, attackerUnit: dict,
                        attackerKeywords: list, attackerModelCount: int, attackerCurrentWounds: int,
                        targetProfile: dict, targetUnit: dict, targetKeywords: list,
                        targetModelCount: int, targetCurrentWounds: int, targetStartingStrength: int,
                        distance: int, attackerName: str, targetName: str,
                        isStationary: bool, didAdvance: bool, didCharge: bool,
                        targetHasCover: bool, isWithinEngagement: bool) -> tuple:
    """
    Resolve attacks for a single weapon - COMPLETE IMPLEMENTATION
    
    Returns: (models, wounds, hazardous, stats) or None
    """
    
    weaponAbilities = weapon.get("weapon abilities", [])
    weaponRange = weapon.get("range")
    
    # Check range
    if isinstance(weaponRange, int) and distance > weaponRange:
        print(f"\n❌ Target out of range! (Distance: {distance}\", Weapon Range: {weaponRange}\")")
        return None
    
    # Display weapon info
    print(f"\n{attackerName} fires {weapon['name']} at {targetName}!")
    print(f"Distance: {distance}\", Weapon Range: {weaponRange}\"")
    
    wad.displayActiveAbilities(weaponAbilities, targetKeywords)
    
    # Calculate attacks
    baseAttacks = parseDiceNotation(weapon["a"])
    
    # Apply RAPID FIRE
    if wad.hasRapidFire(weaponAbilities):
        rapidBonus = wad.getRapidFireBonus(weaponAbilities, distance, weaponRange)
        if rapidBonus > 0:
            print(f"=--- [RAPID FIRE {rapidBonus}] +{rapidBonus} attacks (within half range) ---=")
            baseAttacks += rapidBonus
    
    # Apply BLAST
    if wad.hasBlast(weaponAbilities):
        if isWithinEngagement:
            print(f"❌ [BLAST] cannot be used (target in engagement range)")
            return None
        blastBonus = wad.getBlastBonus(targetModelCount)
        if blastBonus > 0:
            print(f"=--- [BLAST] +{blastBonus} attacks (target has {targetModelCount} models) ---=")
            baseAttacks += blastBonus
    
    totalAttacks = baseAttacks * attackerModelCount
    
    print(f"\nBase attacks: {baseAttacks} × {attackerModelCount} models = {totalAttacks} attacks")
    
    if totalAttacks == 0:
        return (targetModelCount, targetCurrentWounds, 0, {
            "weapon_name": weapon["name"],
            "total_hits": 0,
            "total_wounds": 0,
            "failed_saves": 0,
            "damage_dealt": 0,
            "models_destroyed": 0
        })
    
    # Initialize combat stats
    combat_stats = {
        "weapon_name": weapon["name"],
        "total_hits": 0,
        "total_wounds": 0,
        "failed_saves": 0,
        "damage_dealt": 0,
        "models_destroyed": 0,
        "special_effects": []
    }
    
    # === HIT ROLLS ===
    print(f"\n--- HIT ROLLS ---")
    bs = weapon["bs"]
    
    # Calculate all hit modifiers
    hitModifier = 0
    
    # DAMAGED modifier
    damagedMod = wad.getDamagedModifier(attackerProfile, attackerCurrentWounds, attackerKeywords)
    hitModifier += damagedMod
    
    # BIG GUNS NEVER TIRE modifier
    bigGunsMod = wad.getBigGunsNeverTireModifier(attackerKeywords, targetKeywords, 
                                                  isWithinEngagement, weaponAbilities)
    if bigGunsMod["modifier"] != 0:
        print(f"⚠️ [{bigGunsMod['reason']}]: {bigGunsMod['modifier']:+d} to Hit")
        hitModifier += bigGunsMod["modifier"]
        combat_stats["special_effects"].append(f"{bigGunsMod['reason']}: {bigGunsMod['modifier']:+d} to hit")
    
    # EXECUTIONER ability
    attackerAbility = attackerUnit.get("Ability", {})
    if attackerAbility.get("name") == "Executioner":
        execMod = wad.getExecutionerModifier(targetModelCount, targetStartingStrength,
                                            targetCurrentWounds, targetProfile["w"])
        hitModifier += execMod
    
    # HEAVY bonus
    if wad.hasHeavy(weaponAbilities) and isStationary:
        hitModifier += 1
        print(f"=--- [HEAVY] +1 to Hit (stationary) ---=")
        combat_stats["special_effects"].append("HEAVY: +1 to hit (stationary)")
    
    # Target defensive abilities
    targetAbility = targetUnit.get("Ability", {})
    if targetAbility and targetAbility.get("trigger") == "on_defense":
        condition = targetAbility.get("condition", "")
        
        # Reorder Reality
        if condition == "attackerWithin18" and distance <= 18:
            effects = targetAbility.get("effects", [])
            for effect in effects:
                if effect.get("type") == "hitModifier":
                    modifier_value = effect.get("value", 0)
                    print(f"\n⚠️ [REORDER REALITY] activated!")
                    print(f"   Subtract {abs(modifier_value)} from Hit rolls!")
                    hitModifier += modifier_value
                    combat_stats["special_effects"].append(f"REORDER REALITY: {modifier_value} to hit")
        
        # STEALTH
        elif "STEALTH" in targetKeywords:
            hitModifier -= 1
            print(f"\n⚠️ Target has [STEALTH]!")
            print(f"   Subtract 1 from Hit rolls")
            combat_stats["special_effects"].append("STEALTH: -1 to hit")
    
    if hitModifier != 0:
        print(f"Total Hit modifier: {hitModifier:+d}")
    
    # Check for TORRENT (auto-hit)
    if wad.hasTorrent(weaponAbilities):
        print(f"=--- [TORRENT] All attacks automatically hit! ---=")
        normalHits = totalAttacks
        lethalHits = 0
        combat_stats["special_effects"].append("TORRENT: Auto-hit")
    else:
        # Roll hits
        hitRolls = rolls.rollBox(totalAttacks)
        print(f"Hit rolls: {hitRolls}")
        
        normalHits = 0
        lethalHits = 0
        
        for roll in hitRolls:
            if roll == 1:
                continue
            
            modifiedRoll = roll + hitModifier
            isCritical = (roll == 6)
            
            if modifiedRoll >= bs or isCritical:
                if isCritical and wad.hasLethalHits(weaponAbilities):
                    lethalHits += 1
                else:
                    normalHits += 1
        
        print(f"Results: {normalHits} normal hits", end="")
        if lethalHits > 0:
            print(f", {lethalHits} LETHAL HITS")
            combat_stats["special_effects"].append(f"LETHAL HITS: {lethalHits} auto-wounds")
        else:
            print()
    
    combat_stats["total_hits"] = normalHits + lethalHits
    
    if normalHits == 0 and lethalHits == 0:
        print("\nAll attacks missed!")
        return (targetModelCount, targetCurrentWounds, 0, combat_stats)
    
    # === WOUND ROLLS ===
    print(f"\n--- WOUND ROLLS ---")
    
    strength = weapon["s"]
    toughness = targetProfile["t"]
    
    print(f"Rolling {normalHits} wound rolls (S{strength} vs T{toughness})")
    
    # Calculate wound threshold
    if strength >= toughness * 2:
        woundThreshold = 2
    elif strength > toughness:
        woundThreshold = 3
    elif strength == toughness:
        woundThreshold = 4
    elif strength < toughness and strength >= toughness / 2:
        woundThreshold = 5
    else:
        woundThreshold = 6
    
    print(f"Wound threshold: {woundThreshold}+")
    
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
        combat_stats["special_effects"].append(f"ANTI-{antiKeyword} {antiThreshold}+")
    
    # Roll wounds
    woundRolls = rolls.rollBox(normalHits)
    print(f"Wound rolls: {woundRolls}")
    
    normalWounds = 0
    criticalWounds = 0
    
    for roll in woundRolls:
        # Unmodified 1 always fails
        if roll == 1:
            continue
        
        # Check if critical wound
        isCritical = wad.checkCriticalWound(roll, weaponAbilities, targetKeywords)
        
        if isCritical:
            criticalWounds += 1
        elif roll >= woundThreshold:
            normalWounds += 1
    
    combat_stats["total_wounds"] = normalWounds + criticalWounds + lethalHits
    
    print(f"Results: {normalWounds} normal wounds, {criticalWounds} critical wounds")
    
    # Handle DEVASTATING WOUNDS
    devastatingDamage = 0
    if wad.checkDevastatingWounds(weaponAbilities) and criticalWounds > 0:
        print(f"\n=--- Weapon ability [DEVASTATING WOUNDS] activated! ---=")
        for i in range(criticalWounds):
            damage = parseDiceNotation(weapon["d"])
            devastatingDamage += damage
        print(f"Total mortal damage: {devastatingDamage}")
        combat_stats["special_effects"].append(f"DEVASTATING WOUNDS: {devastatingDamage} mortal damage")
        criticalWounds = 0
    
    totalWounds = normalWounds + criticalWounds + lethalHits
    
    if totalWounds == 0 and devastatingDamage == 0:
        print("\nAll wounds failed!")
        return (targetModelCount, targetCurrentWounds, 0, combat_stats)
    
    # === SAVE ROLLS ===
    print(f"\n--- SAVE ROLLS ---")
    print(f"Target must make {totalWounds} save rolls")
    
    save = targetProfile["sv"]
    invSave = targetProfile.get("inv-sv", 7)
    ap = abs(weapon["ap"])
    
    # Check for IGNORES COVER
    ignoresCover = wad.hasIgnoresCover(weaponAbilities)
    if ignoresCover and targetHasCover:
        print(f"=--- Weapon ability [IGNORES COVER] activated! ---=")
        print(f"Target's cover is negated")
        targetHasCover = False
        combat_stats["special_effects"].append("IGNORES COVER")
    
    # Apply cover modifier
    coverModifier = 0
    if targetHasCover and not ignoresCover:
        coverModifier = 1
        print(f"Target has cover: +1 to armor saves")
        combat_stats["special_effects"].append("Target has cover: +1 save")
    
    modifiedSave = save + ap - coverModifier
    
    if invSave < modifiedSave:
        saveToUse = invSave
        print(f"Using Invulnerable Save: {saveToUse}+")
    else:
        saveToUse = modifiedSave
        if coverModifier > 0:
            print(f"Using Armor Save: {save}+ (modified to {saveToUse}+ by AP-{ap} and +1 cover)")
        else:
            print(f"Using Armor Save: {save}+ (modified to {saveToUse}+ by AP-{ap})")
    
    saveRolls = rolls.rollBox(totalWounds)
    print(f"Save rolls: {saveRolls}")
    
    failedSaves = sum(1 for roll in saveRolls if roll < saveToUse)
    
    combat_stats["failed_saves"] = failedSaves
    
    print(f"Results: {failedSaves} failed saves")
    
    # === DAMAGE ALLOCATION ===
    print(f"\n--- DAMAGE ALLOCATION ---")
    
    modelWounds = targetProfile["w"]
    currentModelWounds = targetCurrentWounds
    modelsRemaining = targetModelCount
    
    initialModels = targetModelCount
    initialWounds = targetCurrentWounds
    
    # Check for Feel No Pain
    hasFNP, fnpThreshold = wad.checkFeelNoPain(targetUnit)
    
    if hasFNP:
        print(f"✓ Target has FEEL NO PAIN {fnpThreshold}+")
    
    # Check for MELTA bonus
    meltaBonus = wad.getMeltaBonus(weaponAbilities, distance, weaponRange)
    if meltaBonus > 0:
        print(f"\n=--- Weapon ability [MELTA {meltaBonus}] activated! ---=")
        print(f"Target within half range: +{meltaBonus} damage")
        combat_stats["special_effects"].append(f"MELTA: +{meltaBonus} damage")
    
    # Allocate normal damage
    for i in range(failedSaves):
        baseDamage = parseDiceNotation(weapon["d"])
        totalDamage = baseDamage + meltaBonus
        
        # Apply Feel No Pain
        if hasFNP:
            actualDamage = wad.applyFeelNoPain(totalDamage, fnpThreshold, targetName)
        else:
            actualDamage = totalDamage
        
        if actualDamage <= 0:
            print(f"Damage instance {i+1}: {totalDamage} damage rolled, all ignored by FNP!")
            continue
        
        damageDealt = min(actualDamage, currentModelWounds)
        currentModelWounds -= damageDealt
        
        print(f"Damage instance {i+1}: {totalDamage} → {actualDamage} after FNP → {damageDealt} dealt", end="")
        
        if currentModelWounds <= 0:
            modelsRemaining -= 1
            print(f" - Model destroyed! ({modelsRemaining} remaining)")
            currentModelWounds = modelWounds
            if modelsRemaining <= 0:
                break
        else:
            print(f" - Model has {currentModelWounds}/{modelWounds} wounds")
    
    # Allocate mortal damage from Devastating Wounds
    if devastatingDamage > 0:
        print(f"\nApplying {devastatingDamage} mortal damage")
        
        # FNP applies to mortal wounds
        if hasFNP:
            devastatingDamage = wad.applyFeelNoPain(devastatingDamage, fnpThreshold, targetName)
            if devastatingDamage <= 0:
                print(f"All mortal wounds ignored by FNP!")
        
        while devastatingDamage > 0 and modelsRemaining > 0:
            damageToModel = min(devastatingDamage, currentModelWounds)
            currentModelWounds -= damageToModel
            devastatingDamage -= damageToModel
            
            if currentModelWounds <= 0:
                modelsRemaining -= 1
                print(f"Model destroyed by mortal damage! ({modelsRemaining} remaining)")
                currentModelWounds = modelWounds
    
    # Calculate actual damage dealt
    if initialModels > modelsRemaining:
        models_lost = initialModels - modelsRemaining
        combat_stats["models_destroyed"] = models_lost
        if modelsRemaining > 0:
            combat_stats["damage_dealt"] = (models_lost * modelWounds) - (modelWounds - initialWounds) + (modelWounds - currentModelWounds)
        else:
            combat_stats["damage_dealt"] = (models_lost - 1) * modelWounds + initialWounds
    else:
        combat_stats["damage_dealt"] = initialWounds - currentModelWounds
    
    print(f"\nFinal result: {modelsRemaining} models remaining")
    
    # Check for HAZARDOUS
    hazardousDamage = 0
    if wad.hasHazardous(weaponAbilities):
        print(f"\n--- HAZARDOUS TEST ---")
        print(f"Rolling Hazardous test for {weapon['name']}...")
        hazardRoll = rolls.rollBox(1)[0]
        print(f"Hazardous roll: {hazardRoll}")
        
        if hazardRoll == 1:
            hazardousDamage = 3
            print(f"⚠️ HAZARDOUS TEST FAILED!")
            print(f"{attackerName} suffers 3 mortal wounds!")
            combat_stats["special_effects"].append("HAZARDOUS: 3 mortal wounds to shooter")
        else:
            print(f"✓ Hazardous test passed")
    
    # Check for Reorder Reality's HAZARDOUS effect
    if targetAbility and targetAbility.get("trigger") == "on_defense":
        condition = targetAbility.get("condition", "")
        if condition == "attackerWithin18" and distance <= 18:
            effects = targetAbility.get("effects", [])
            for effect in effects:
                if effect.get("type") == "addHazardous":
                    print(f"\n--- REORDER REALITY HAZARDOUS TEST ---")
                    print(f"Weapon gains HAZARDOUS from Reorder Reality...")
                    hazardRoll = rolls.rollBox(1)[0]
                    print(f"Hazardous roll: {hazardRoll}")
                    
                    if hazardRoll == 1:
                        hazardousDamage += 3
                        print(f"⚠️ HAZARDOUS TEST FAILED!")
                        print(f"{attackerName} suffers 3 mortal wounds!")
                        combat_stats["special_effects"].append("Reorder Reality HAZARDOUS: 3 mortal wounds")
                    else:
                        print(f"✓ Hazardous test passed")
    
    return (modelsRemaining, currentModelWounds if modelsRemaining > 0 else modelWounds, hazardousDamage, combat_stats)

def shootPhase(attackerWeapons: list, attackerProfile: dict, targetProfile: dict,
               targetUnit: dict, attackerModelCount: int, targetModelCount: int,
               targetCurrentWounds: int, distance: int, attackerName: str,
               targetName: str, targetKeywords: list, attackerUnit: dict = None,
               attackerKeywords: list = None, targetStartingStrength: int = None,
               attackerCurrentWounds: int = None, isStationary: bool = False,
               didAdvance: bool = False, didCharge: bool = False,
               targetHasCover: bool = False,
               game_state=None, ability_logger=None) -> tuple:
    """
    Execute the shooting phase for a unit
    
    NEW: Supports VEHICLE multi-weapon shooting and MONSTER/VEHICLE abilities
    
    Returns:
        tuple: (remaining target models, current target wounds, hazardous damage, combat_stats dict)
        or None if unit cannot shoot
    """
    
    # Initialize combat stats tracker
    combat_stats = {
        "weapon_name": "",
        "total_hits": 0,
        "total_wounds": 0,
        "failed_saves": 0,
        "damage_dealt": 0,
        "models_destroyed": 0,
        "special_effects": []
    }
    
    # Safety: ensure attackerUnit and keywords are provided
    if attackerUnit is None:
        attackerUnit = {"Keyword": attackerKeywords or []}
    if attackerKeywords is None:
        attackerKeywords = attackerUnit.get("Keyword", [])
    
    if targetStartingStrength is None:
        targetStartingStrength = targetUnit.get("Model Count", targetModelCount)
    
    if attackerCurrentWounds is None:
        attackerCurrentWounds = attackerProfile.get("w", 1)
    
    # Check if within engagement range
    isWithinEngagement = distance <= 1
    
    # ✅ CHECK BIG GUNS NEVER TIRE
    canShootInEngagement = wad.canShootInEngagement(attackerKeywords, [])
    
    if isWithinEngagement and not canShootInEngagement:
        # Normal infantry cannot shoot in engagement unless using PISTOL
        pistolWeapons = [w for w in attackerWeapons if "PISTOL" in w.get("weapon abilities", [])]
        
        if len(pistolWeapons) == 0:
            print(f"\n⚠️ {attackerName} cannot shoot (in Engagement Range without PISTOL or MONSTER/VEHICLE)")
            return None
    
    # Check if unit can shoot after advancing/charging
    if didAdvance or didCharge:
        hasAssaultWeapon = any(
            "ASSAULT" in weapon.get("weapon abilities", [])
            for weapon in attackerWeapons
            if weapon.get("range") != "Melee"
        )
        
        if not hasAssaultWeapon:
            print(f"\n⚠️ {attackerName} cannot shoot (Advanced/Charged without ASSAULT weapons)")
            return None
    
    # ✅ CHECK IF VEHICLE - FIRE ALL WEAPONS
    isVehicle = wad.isVehicle(attackerKeywords)
    
    if isVehicle:
        print(f"\n{'='*60}")
        print(f"🚗 {attackerName} is a VEHICLE - fires ALL ranged weapons!")
        print(f"{'='*60}")
        
        # Get all ranged weapons
        rangedWeapons = wad.getAllRangedWeapons(attackerWeapons)
        
        if len(rangedWeapons) == 0:
            print(f"\n⚠️ {attackerName} has no ranged weapons!")
            return None
        
        # Track total damage across all weapons
        totalModelsDestroyed = 0
        totalDamageDealt = 0
        totalHazardous = 0
        
        # Fire each weapon sequentially
        for weaponIndex, weapon in enumerate(rangedWeapons):
            print(f"\n{'='*60}")
            print(f"WEAPON {weaponIndex + 1}/{len(rangedWeapons)}: {weapon['name']}")
            print(f"{'='*60}")
            
            # Resolve this weapon's attacks
            result = resolveWeaponAttacks(
                weapon=weapon,
                attackerProfile=attackerProfile,
                attackerUnit=attackerUnit,
                attackerKeywords=attackerKeywords,
                attackerModelCount=attackerModelCount,
                attackerCurrentWounds=attackerCurrentWounds,
                targetProfile=targetProfile,
                targetUnit=targetUnit,
                targetKeywords=targetKeywords,
                targetModelCount=targetModelCount,
                targetCurrentWounds=targetCurrentWounds,
                targetStartingStrength=targetStartingStrength,
                distance=distance,
                attackerName=attackerName,
                targetName=targetName,
                isStationary=isStationary,
                didAdvance=didAdvance,
                didCharge=didCharge,
                targetHasCover=targetHasCover,
                isWithinEngagement=isWithinEngagement
            )
            
            if result:
                targetModelCount, targetCurrentWounds, hazDamage, weapon_stats = result
                totalHazardous += hazDamage
                
                # Accumulate stats
                combat_stats["total_hits"] += weapon_stats.get("total_hits", 0)
                combat_stats["total_wounds"] += weapon_stats.get("total_wounds", 0)
                combat_stats["failed_saves"] += weapon_stats.get("failed_saves", 0)
                combat_stats["damage_dealt"] += weapon_stats.get("damage_dealt", 0)
                combat_stats["models_destroyed"] += weapon_stats.get("models_destroyed", 0)
                combat_stats["special_effects"].extend(weapon_stats.get("special_effects", []))
            
            # Stop if target destroyed
            if targetModelCount <= 0:
                print(f"\n💀 {targetName} DESTROYED!")
                break
        
        combat_stats["weapon_name"] = f"All weapons ({len(rangedWeapons)} total)"
        
        return (targetModelCount, targetCurrentWounds, totalHazardous, combat_stats)
    
    else:
        # ✅ NON-VEHICLE: Select single weapon
        if isWithinEngagement:
            eligibleWeapons = getRangedWeaponsInEngagement(attackerWeapons, attackerProfile)
        else:
            eligibleWeapons = getRangedWeapons(attackerWeapons)
        
        if len(eligibleWeapons) == 0:
            print(f"\n⚠️ {attackerName} has no eligible ranged weapons!")
            return None
        
        selectedWeapon = selectWeapon(eligibleWeapons, attackerName, distance, isWithinEngagement)
        
        if selectedWeapon is None:
            return None
        
        combat_stats["weapon_name"] = selectedWeapon["name"]
        
        # Resolve single weapon attacks
        result = resolveWeaponAttacks(
            weapon=selectedWeapon,
            attackerProfile=attackerProfile,
            attackerUnit=attackerUnit,
            attackerKeywords=attackerKeywords,
            attackerModelCount=attackerModelCount,
            attackerCurrentWounds=attackerCurrentWounds,
            targetProfile=targetProfile,
            targetUnit=targetUnit,
            targetKeywords=targetKeywords,
            targetModelCount=targetModelCount,
            targetCurrentWounds=targetCurrentWounds,
            targetStartingStrength=targetStartingStrength,
            distance=distance,
            attackerName=attackerName,
            targetName=targetName,
            isStationary=isStationary,
            didAdvance=didAdvance,
            didCharge=didCharge,
            targetHasCover=targetHasCover,
            isWithinEngagement=isWithinEngagement
        )
        
        if result:
            targetModelCount, targetCurrentWounds, hazDamage, weapon_stats = result
            combat_stats.update(weapon_stats)
            return (targetModelCount, targetCurrentWounds, hazDamage, combat_stats)
        
        return (targetModelCount, targetCurrentWounds, 0, combat_stats)

