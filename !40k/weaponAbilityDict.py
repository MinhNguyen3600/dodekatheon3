"""
weaponAbilityDict.py - Core Rules Weapon Abilities Only

This file contains ONLY weapon abilities defined in the 40K core rules.
NO unit-specific abilities should be here - those belong in datasheets.py using ability templates.

All functions use definitions from abilitySystem where possible.
"""

import rolls as rolls
import re

# ==================== WEAPON ABILITY PARSERS ====================

def parseAntiAbility(ability: str) -> tuple:
    """
    Parse ANTI- ability string
    Returns: (keyword, threshold) or (None, None) if not an ANTI ability
    Example: "ANTI-VEHICLE 4+" returns ("VEHICLE", 4)
    """
    pattern = r'^ANTI-(\w+)\s+(\d+)\+$'
    match = re.match(pattern, ability.upper())
    
    if match:
        keyword = match.group(1)
        threshold = int(match.group(2))
        return (keyword, threshold)
    
    return (None, None)

def parseRapidFire(ability: str) -> int:
    """
    Parse RAPID FIRE X ability
    Returns: X value, or 0 if not a RAPID FIRE ability
    Example: "RAPID FIRE 5" returns 5
    """
    pattern = r'^RAPID FIRE\s+(\d+)$'
    match = re.match(pattern, ability.upper())
    
    if match:
        return int(match.group(1))
    
    return 0

def parseMelta(ability: str) -> int:
    """
    Parse MELTA X ability
    Returns: X value, or 0 if not a MELTA ability
    Example: "MELTA 2" returns 2
    """
    pattern = r'^MELTA\s+(\d+)$'
    match = re.match(pattern, ability.upper())
    
    if match:
        return int(match.group(1))
    
    return 0

def parseSustainedHits(ability: str) -> int:
    """
    Parse SUSTAINED HITS X ability
    Returns: X value, or 0 if not a SUSTAINED HITS ability
    Example: "SUSTAINED HITS 1" returns 1
    """
    pattern = r'^SUSTAINED HITS\s+(\d+)$'
    match = re.match(pattern, ability.upper())
    
    if match:
        return int(match.group(1))
    
    return 0

# ==================== KEYWORD CHECKERS ====================

def isMonsterOrVehicle(keywords: list) -> bool:
    """Check if unit has MONSTER or VEHICLE keyword"""
    upperKeywords = [k.upper() for k in keywords]
    return "MONSTER" in upperKeywords or "VEHICLE" in upperKeywords

def isMonster(keywords: list) -> bool:
    """Check if unit has MONSTER keyword"""
    upperKeywords = [k.upper() for k in keywords]
    return "MONSTER" in upperKeywords

def isVehicle(keywords: list) -> bool:
    """Check if unit has VEHICLE keyword"""
    upperKeywords = [k.upper() for k in keywords]
    return "VEHICLE" in upperKeywords

# ==================== WEAPON ABILITY PRESENCE CHECKERS ====================

def hasRapidFire(weaponAbilities: list) -> bool:
    """Check if weapon has RAPID FIRE ability"""
    for ability in weaponAbilities:
        if ability.upper().startswith("RAPID FIRE"):
            return True
    return False

def hasBlast(weaponAbilities: list) -> bool:
    """Check if weapon has BLAST ability"""
    return "BLAST" in weaponAbilities

def hasMelta(weaponAbilities: list) -> bool:
    """Check if weapon has MELTA ability"""
    for ability in weaponAbilities:
        if ability.upper().startswith("MELTA"):
            return True
    return False

def hasHeavy(weaponAbilities: list) -> bool:
    """Check if weapon has HEAVY ability"""
    return "HEAVY" in weaponAbilities

def hasTorrent(weaponAbilities: list) -> bool:
    """Check if weapon has TORRENT ability (auto-hit)"""
    return "TORRENT" in weaponAbilities

def hasIgnoresCover(weaponAbilities: list) -> bool:
    """Check if weapon has IGNORES COVER ability"""
    return "IGNORES COVER" in weaponAbilities

def hasHazardous(weaponAbilities: list) -> bool:
    """Check if weapon has HAZARDOUS ability"""
    return "HAZARDOUS" in weaponAbilities

def hasAssault(weaponAbilities: list) -> bool:
    """Check if weapon has ASSAULT ability"""
    return "ASSAULT" in weaponAbilities

def hasPistol(weaponAbilities: list) -> bool:
    """Check if weapon has PISTOL ability"""
    return "PISTOL" in weaponAbilities

def hasIndirectFire(weaponAbilities: list) -> bool:
    """Check if weapon has INDIRECT FIRE ability"""
    return "INDIRECT FIRE" in weaponAbilities

def hasTwinLinked(weaponAbilities: list) -> bool:
    """Check if weapon has TWIN-LINKED ability (reroll wounds)"""
    return "TWIN-LINKED" in weaponAbilities

def hasLance(weaponAbilities: list) -> bool:
    """Check if weapon has LANCE ability (+1 to wound after charging)"""
    return "LANCE" in weaponAbilities

def hasSustainedHits(weaponAbilities: list) -> bool:
    """Check if weapon has SUSTAINED HITS ability"""
    for ability in weaponAbilities:
        if ability.upper().startswith("SUSTAINED HITS"):
            return True
    return False

def hasLethalHits(weaponAbilities: list) -> bool:
    """Check if weapon has LETHAL HITS ability"""
    return "LETHAL HITS" in weaponAbilities

def hasDevastatingWounds(weaponAbilities: list) -> bool:
    """Check if weapon has DEVASTATING WOUNDS ability"""
    return "DEVASTATING WOUNDS" in weaponAbilities

def hasPrecision(weaponAbilities: list) -> bool:
    """Check if weapon has PRECISION ability"""
    return "PRECISION" in weaponAbilities

def hasAntiAbility(weaponAbilities: list, targetKeywords: list) -> tuple:
    """
    Check if weapon has ANTI- ability that applies to target
    Returns: (hasAnti, threshold) where threshold is the crit wound value
    """
    for ability in weaponAbilities:
        antiKeyword, antiThreshold = parseAntiAbility(ability)
        
        if antiKeyword and antiThreshold:
            # Check if target has the matching keyword
            for keyword in targetKeywords:
                if keyword.upper() == antiKeyword:
                    return (True, antiThreshold)
    
    return (False, 6)  # Default to only natural 6s are crits

def hasExtraAttacks(weaponAbilities: list) -> bool:
    """Check if weapon has EXTRA ATTACKS ability"""
    return "EXTRA ATTACKS" in weaponAbilities

# ==================== WEAPON ABILITY VALUE GETTERS ====================

def getRapidFireBonus(weaponAbilities: list, distance: int, weaponRange: int) -> int:
    """
    Calculate RAPID FIRE bonus attacks if within half range
    Returns: bonus attacks (0 if not within half range or no RAPID FIRE)
    """
    for ability in weaponAbilities:
        rapidFireValue = parseRapidFire(ability)
        if rapidFireValue > 0:
            if isinstance(weaponRange, int) and distance <= weaponRange / 2:
                return rapidFireValue
    return 0

def getBlastBonus(targetModelCount: int) -> int:
    """
    Calculate BLAST bonus attacks based on target unit size
    Official Rule: Add 1 attack per 5 models (rounding down)
    Returns: bonus attacks
    """
    return targetModelCount // 5

def getMeltaBonus(weaponAbilities: list, distance: int, weaponRange) -> int:
    """
    Calculate MELTA bonus damage if within half range
    Returns: bonus damage (0 if not within half range or no MELTA)
    """
    for ability in weaponAbilities:
        meltaValue = parseMelta(ability)
        if meltaValue > 0:
            if isinstance(weaponRange, int) and distance <= weaponRange / 2:
                return meltaValue
    return 0

def getSustainedHitsValue(weaponAbilities: list) -> int:
    """
    Get SUSTAINED HITS X value
    Returns: X value, or 0 if no SUSTAINED HITS
    """
    for ability in weaponAbilities:
        sustainedValue = parseSustainedHits(ability)
        if sustainedValue > 0:
            return sustainedValue
    return 0

def getExtraAttacksWeapons(weapons: list) -> dict:
    """
    Separate melee weapons into Extra Attacks and normal weapons
    
    Returns: {
        "extra_attacks": list of weapons with EXTRA ATTACKS,
        "normal": list of weapons without EXTRA ATTACKS
    }
    """
    extraAttacks = []
    normal = []
    
    for weapon in weapons:
        if weapon.get("range") == "Melee":
            if hasExtraAttacks(weapon.get("weapon abilities", [])):
                extraAttacks.append(weapon)
            else:
                normal.append(weapon)
    
    return {
        "extra_attacks": extraAttacks,
        "normal": normal
    }

# ==================== ATTACK COUNT MODIFIERS (BEFORE HIT ROLLS) ====================

def applyBlast(baseAttacks: int, targetUnitCount: int, isInEngagementRange: bool, weaponAbilities: list) -> int:
    """
    BLAST: Add 1 attack per 5 models in target unit (rounding down)
    Cannot be used if any friendly unit is in engagement range of target
    
    Official Rule: "Add 1 to the Attacks characteristic for every five models in the target unit (rounding down).
    Can never be used against a target that is within Engagement Range of any units from the attacking model's army."
    """
    if "BLAST" not in weaponAbilities:
        return baseAttacks
    
    if isInEngagementRange:
        print("=--- Weapon ability [BLAST] is not eligible to be activated! ---=")
        print("=-------- REASON: Target unit within engagement range! ---------=")
        return 0  # Cannot shoot at all
    
    bonusAttacks = targetUnitCount // 5
    
    if bonusAttacks > 0:
        print(f"=--- Weapon ability [BLAST] activated! ---=")
        print(f"=--- +{bonusAttacks} attacks (target has {targetUnitCount} models) ---=")
        return baseAttacks + bonusAttacks
    
    return baseAttacks

def applyRapidFire(baseAttacks: int, targetDistance: int, weaponRange: int, weaponAbilities: list) -> int:
    """
    RAPID FIRE X: Increase Attacks by X when targeting units within half range
    
    Official Rule: "Each time such a weapon targets a unit within half that weapon's range, 
    the Attacks characteristic of that weapon is increased by the amount denoted by 'x'."
    """
    for ability in weaponAbilities:
        rapidFireValue = parseRapidFire(ability)
        
        if rapidFireValue > 0:
            if targetDistance <= weaponRange / 2:
                print(f"=--- Weapon Ability [RAPID FIRE {rapidFireValue}] activated! ---=")
                print(f"=--- Attacks increased from {baseAttacks} to {baseAttacks + rapidFireValue} ---=")
                return baseAttacks + rapidFireValue
    
    return baseAttacks

def applySustainedHits(criticalHits: int, weaponAbilities: list) -> int:
    """
    SUSTAINED HITS X: Each critical hit generates X additional hits
    
    Official Rule: "Each time an attack is made with such a weapon, if a Critical Hit is rolled, 
    that attack scores a number of additional hits on the target equal to the value denoted by 'x'."
    
    Returns: additional hits generated
    """
    for ability in weaponAbilities:
        sustainedValue = parseSustainedHits(ability)
        
        if sustainedValue > 0 and criticalHits > 0:
            additionalHits = criticalHits * sustainedValue
            print(f"=--- Weapon ability [SUSTAINED HITS {sustainedValue}] activated! ---=")
            print(f"=--- {criticalHits} critical hits generate {additionalHits} additional hits! ---=")
            return additionalHits
    
    return 0

def canModifyExtraAttacksCount(weapon: dict, abilityName: str = "") -> bool:
    """
    Check if attack count can be modified for an Extra Attacks weapon
    
    Official Rule: "The number of attacks made with an Extra Attacks weapon cannot be 
    modified by other rules, unless that weapon's name is explicitly specified in that rule."
    
    Returns: True if attacks can be modified, False if blocked
    """
    if not hasExtraAttacks(weapon.get("weapon abilities", [])):
        return True  # Not an Extra Attacks weapon, always modifiable
    
    # Check if ability explicitly names this weapon
    weaponName = weapon.get("name", "")
    if weaponName.lower() in abilityName.lower():
        return True  # Explicitly named, modification allowed
    
    return False  # Extra Attacks weapon, modification blocked

# ==================== HIT ROLL MODIFIERS ====================

def getHitModifiers(weaponAbilities: list, isStationary: bool, didAdvance: bool) -> dict:
    """
    Calculate all hit roll modifiers
    Returns: {
        "modifier": int (total modifier to hit rolls),
        "canShoot": bool (whether unit can shoot at all),
        "autoHit": bool (TORRENT makes attacks auto-hit)
    }
    """
    result = {
        "modifier": 0,
        "canShoot": True,
        "autoHit": False
    }
    
    # HEAVY: +1 to hit if stationary
    if "HEAVY" in weaponAbilities:
        if isStationary:
            result["modifier"] += 1
            print("=--- Weapon ability [HEAVY] activated! ---=")
            print("=--- +1 to Hit rolls (unit stationary) ---=")
        else:
            print("=--- Weapon ability [HEAVY] is not eligible! ---=")
            print("=--- REASON: Unit is not stationary this turn! ---=")
    
    # ASSAULT: Can shoot after advancing
    if didAdvance:
        if "ASSAULT" in weaponAbilities:
            print("=--- Weapon ability [ASSAULT] activated! ---=")
            print("=--- Can shoot despite advancing ---=")
        else:
            result["canShoot"] = False
            print("=--- Cannot shoot - unit Advanced (no ASSAULT weapon) ---=")
    
    # TORRENT: Auto-hit
    if "TORRENT" in weaponAbilities:
        result["autoHit"] = True
        print("=--- Weapon ability [TORRENT] activated! ---=")
        print("=--- All attacks automatically hit! ---=")
    
    return result

def applyHitModifier(roll: int, modifier: int, ballistic_skill: int) -> tuple:
    """
    Apply hit modifiers to a single roll
    Returns: (isHit, isCritical)
    
    Important: Modifiers don't change whether a roll is "critical" (unmodified 6)
    """
    # Unmodified 1 always fails
    if roll == 1:
        return (False, False)
    
    # Unmodified 6 is always a critical hit
    if roll == 6:
        return (True, True)
    
    # Apply modifier and check against BS
    modifiedRoll = roll + modifier
    isHit = modifiedRoll >= ballistic_skill
    
    return (isHit, False)  # Not a critical since it wasn't unmodified 6

def isLethalHits(hitRoll: int, weaponAbilities: list) -> bool:
    """
    LETHAL HITS: Critical hits (unmodified 6s) automatically wound
    
    Official Rule: "Each time an attack is made with such a weapon, 
    a Critical Hit automatically wounds the target."
    """
    if hasLethalHits(weaponAbilities) and hitRoll == 6:
        return True
    return False

# ==================== WOUND ROLL MODIFIERS ====================

def getWoundModifiers(weaponAbilities: list, didCharge: bool) -> int:
    """
    Calculate wound roll modifiers
    Returns: total modifier to wound rolls
    """
    modifier = 0
    
    # LANCE: +1 to wound if charged this turn
    if hasLance(weaponAbilities) and didCharge:
        modifier += 1
        print("=--- Weapon ability [LANCE] activated! ---=")
        print("=--- +1 to Wound rolls (unit charged this turn) ---=")
    
    return modifier

def checkCriticalWound(woundRoll: int, weaponAbilities: list, targetKeywords: list) -> bool:
    """
    Check if a wound roll is a critical wound
    Returns: True if critical wound
    
    Critical wounds occur on:
    - Unmodified 6
    - ANTI-KEYWORD X+ against matching keyword
    """
    # Unmodified 6 is always critical
    if woundRoll == 6:
        return True
    
    # Check ANTI- abilities
    hasAnti, antiThreshold = hasAntiAbility(weaponAbilities, targetKeywords)
    
    if hasAnti and woundRoll >= antiThreshold:
        return True
    
    return False

def checkDevastatingWounds(weaponAbilities: list) -> bool:
    """
    DEVASTATING WOUNDS: Critical wounds deal mortal damage
    
    Official Rule: "Each time an attack is made with such a weapon, if that attack scores a Critical Wound, 
    no saving throw of any kind can be made against that attack. 
    It inflicts a number of mortal wounds on the target equal to the Damage characteristic of that attack."
    """
    return hasDevastatingWounds(weaponAbilities)

def canRerollWound(weaponAbilities: list) -> bool:
    """
    TWIN-LINKED: Can re-roll wound rolls
    
    Official Rule: "Each time an attack is made with such a weapon, 
    you can re-roll that attack's Wound roll."
    """
    return "TWIN-LINKED" in weaponAbilities

# ==================== DAMAGE MODIFIERS ====================

def applyMelta(baseDamage: int, targetDistance: int, weaponRange: int, weaponAbilities: list) -> int:
    """
    MELTA X: Increase damage by X when targeting units within half range
    
    Official Rule: "Each time an attack made with such a weapon targets a unit within half that weapon's range, 
    that attack's Damage characteristic is increased by the amount denoted by 'x'."
    """
    for ability in weaponAbilities:
        meltaValue = parseMelta(ability)
        
        if meltaValue > 0:
            if targetDistance <= weaponRange / 2:
                print(f"  → [MELTA {meltaValue}] +{meltaValue} damage (within half range)")
                return baseDamage + meltaValue
    
    return baseDamage

# ==================== SAVE ROLL MODIFIERS ====================

def targetHasCover(targetHasCover: bool, weaponAbilities: list) -> bool:
    """
    IGNORES COVER: Target cannot benefit from cover
    
    Official Rule: "Each time an attack is made with such a weapon, 
    the target cannot have the Benefit of Cover against that attack."
    """
    if "IGNORES COVER" in weaponAbilities:
        print("=--- Weapon ability [IGNORES COVER] activated! ---=")
        print("=--- Target loses Benefit of Cover ---=")
        return False
    
    return targetHasCover

def applyBenefitOfCover(save: int, hasCover: bool) -> int:
    """
    Apply Benefit of Cover bonus to save
    
    Official Rule: Benefit of Cover improves save by 1 (to a maximum of 4+)
    
    Returns: modified save characteristic
    """
    if not hasCover:
        return save
    
    # Cover gives +1 to save (lower number is better)
    modifiedSave = save - 1
    
    # Cover cannot improve save beyond 4+
    modifiedSave = max(modifiedSave, 4)
    
    return modifiedSave

def checkFeelNoPain(targetUnit: dict) -> tuple:
    """
    Check if target has Feel No Pain ability
    
    Official Rule: "Each time a model with this ability suffers damage and so would lose a wound, 
    roll one D6: if the result is greater than or equal to 'x', that wound is ignored."
    
    Returns: (hasFNP, threshold)
    Example: "FEEL NO PAIN 5+" returns (True, 5)
    """
    # Check for direct FNP field
    fnp = targetUnit.get("Feel No Pain", None)
    if fnp:
        if isinstance(fnp, int):
            return (True, fnp)
        elif isinstance(fnp, str):
            pattern = r'(\d+)\+'
            match = re.search(pattern, fnp)
            if match:
                threshold = int(match.group(1))
                return (True, threshold)
    
    # Check in ability dict
    unitAbility = targetUnit.get("Ability", {})
    if isinstance(unitAbility, dict):
        abilityName = unitAbility.get("name", "")
        if "FEEL NO PAIN" in abilityName.upper():
            pattern = r'(\d+)\+'
            match = re.search(pattern, abilityName)
            if match:
                threshold = int(match.group(1))
                return (True, threshold)
    
    # Check keywords
    keywords = targetUnit.get("Keyword", [])
    for keyword in keywords:
        if "FEEL NO PAIN" in keyword.upper():
            pattern = r'(\d+)\+'
            match = re.search(pattern, keyword)
            if match:
                threshold = int(match.group(1))
                return (True, threshold)
    
    return (False, 7)

def applyFeelNoPain(damageToAllocate: int, fnpThreshold: int, modelName: str) -> int:
    """
    Apply Feel No Pain rolls to damage
    
    Args:
        damageToAllocate: Total wounds to allocate
        fnpThreshold: FNP threshold (e.g., 5 for "5+")
        modelName: Name of model for display
    
    Returns: actual damage taken after FNP saves
    """
    if fnpThreshold >= 7 or damageToAllocate <= 0:
        return damageToAllocate
    
    print(f"\n{'='*60}")
    print(f"💊 FEEL NO PAIN {fnpThreshold}+ - {modelName}")
    print(f"{'='*60}")
    print(f"Rolling to ignore {damageToAllocate} wound(s)...")
    
    fnpRolls = rolls.rollBox(damageToAllocate)
    print(f"Feel No Pain rolls: {fnpRolls}")
    
    woundsIgnored = sum(1 for roll in fnpRolls if roll >= fnpThreshold)
    actualDamage = damageToAllocate - woundsIgnored
    
    print(f"Wounds ignored: {woundsIgnored}")
    print(f"Actual damage taken: {actualDamage}")
    print(f"{'='*60}\n")
    
    return actualDamage

# ==================== SPECIAL WEAPON TYPES ====================

def isPistol(weaponAbilities: list) -> bool:
    """
    PISTOL: Can be used in engagement range
    
    Official Rule: "If a unit contains any models equipped with Pistols, that unit is eligible to shoot 
    in its controlling player's Shooting phase even while it is within Engagement Range of one or more enemy units."
    """
    return "PISTOL" in weaponAbilities

def isIndirectFire(weaponAbilities: list) -> bool:
    """
    INDIRECT FIRE: Can target units not visible to attacker
    
    Official Rule: "Attacks can be made with them even if the target is not visible to the attacking model."
    """
    return "INDIRECT FIRE" in weaponAbilities

def getIndirectFirePenalty(targetVisible: bool, weaponAbilities: list) -> dict:
    """
    INDIRECT FIRE: Penalties when target not visible
    
    Returns: {
        "hitModifier": int,
        "targetHasCover": bool,
        "minHitRoll": int (minimum roll needed, 1-3 always fails)
    }
    """
    if "INDIRECT FIRE" in weaponAbilities and not targetVisible:
        print("=--- Weapon ability [INDIRECT FIRE] targeting non-visible unit ---=")
        print("=--- -1 to Hit, rolls of 1-3 fail, target has cover ---=")
        return {
            "hitModifier": -1,
            "targetHasCover": True,
            "minHitRoll": 4  # 1-3 always fails
        }
    
    return {
        "hitModifier": 0,
        "targetHasCover": False,
        "minHitRoll": 1
    }

# ==================== POST-SHOOTING HAZARDS ====================

def performHazardousTests(weaponAbilities: list, shotsResolved: int) -> int:
    """
    HAZARDOUS: After shooting, roll D6 for each hazardous weapon used. On 1, suffer 3 mortal wounds.
    
    Official Rule: "After that unit has resolved all of its attacks, for each Hazardous weapon that targets were 
    selected for when resolving those attacks, that unit must take one Hazardous test. To do so, roll one D6: on a 1, 
    that test is failed. For each failed test... that unit suffers 3 mortal wounds."
    
    Returns: mortal wounds suffered
    """
    if "HAZARDOUS" not in weaponAbilities or shotsResolved == 0:
        return 0
    
    print("\n=--- HAZARDOUS TEST ---=")
    testRoll = rolls.rollBox(1)[0]
    print(f"Rolling Hazardous test: {testRoll}")
    
    if testRoll == 1:
        print("=--- HAZARDOUS TEST FAILED! ---=")
        print("=--- Shooting unit suffers 3 mortal wounds! ---=")
        return 3
    else:
        print("=--- Hazardous test passed ---=")
        return 0

# ==================== ABILITY DISPLAY ====================

def displayActiveAbilities(weaponAbilities: list, targetKeywords: list = None):
    """
    Display which weapon abilities are present on the weapon
    """
    if not weaponAbilities:
        return
    
    print(f"\nWeapon abilities: {', '.join(weaponAbilities)}")
    
    # Check for ANTI- abilities and show if they apply
    if targetKeywords:
        for ability in weaponAbilities:
            antiKeyword, antiThreshold = parseAntiAbility(ability)
            if antiKeyword:
                if antiKeyword in [k.upper() for k in targetKeywords]:
                    print(f"  → [ANTI-{antiKeyword} {antiThreshold}+] is ACTIVE against this target!")
                else:
                    print(f"  → [ANTI-{antiKeyword} {antiThreshold}+] is inactive (target lacks {antiKeyword} keyword)")

# ==================== VEHICLE/MONSTER ABILITIES ====================

def getDamagedModifier(unitProfile: dict, currentWounds: int, unitKeywords: list) -> int:
    """
    DAMAGED: VEHICLE units suffer -1 to hit when below damage threshold
    
    Official Rule: "While this model has [X] wounds remaining, 
    each time this model makes an attack, subtract 1 from the Hit roll."
    
    Returns: -1 if damaged, 0 otherwise
    """
    if not isVehicle(unitKeywords):
        return 0
    
    damagedThreshold = unitProfile.get("damaged_threshold", 0)
    
    if damagedThreshold == 0:
        return 0  # No DAMAGED profile
    
    if currentWounds <= damagedThreshold and currentWounds > 0:
        print(f"\n⚠️ [DAMAGED] Vehicle has {currentWounds} wounds remaining!")
        print(f"   Effect: -1 to all Hit rolls")
        return -1
    
    return 0

def canShootInEngagement(unitKeywords: list, weaponAbilities: list) -> bool:
    """
    BIG GUNS NEVER TIRE: Check if unit can shoot while in engagement range
    
    Returns: True if MONSTER/VEHICLE or has PISTOL
    """
    if isMonsterOrVehicle(unitKeywords):
        return True
    
    if "PISTOL" in weaponAbilities:
        return True
    
    return False

def getBigGunsNeverTireModifier(attackerKeywords: list, targetKeywords: list, 
                                 isInEngagement: bool, weaponAbilities: list) -> dict:
    """
    BIG GUNS NEVER TIRE: Get hit modifiers for shooting in/at engagement
    
    Official Rule: "MONSTERS and VEHICLES can shoot, and be shot at, 
    even while they are within Engagement Range of enemy units. 
    Each time a ranged attack is made by or against such a unit, 
    subtract 1 from that attack's Hit roll (unless shooting with a Pistol)."
    
    Returns: {
        "modifier": int,
        "reason": str
    }
    """
    result = {"modifier": 0, "reason": ""}
    
    if not isInEngagement:
        return result
    
    # Skip modifier if using PISTOL
    if "PISTOL" in weaponAbilities:
        return result
    
    # Attacker is MONSTER/VEHICLE shooting in engagement
    if isMonsterOrVehicle(attackerKeywords):
        result["modifier"] = -1
        result["reason"] = "Shooting in Engagement Range (BIG GUNS NEVER TIRE)"
        return result
    
    # Target is MONSTER/VEHICLE being shot at in engagement
    if isMonsterOrVehicle(targetKeywords):
        result["modifier"] = -1
        result["reason"] = "Targeting MONSTER/VEHICLE in Engagement Range"
        return result
    
    return result

def getAllRangedWeapons(weapons: list) -> list:
    """
    Get all ranged weapons from a unit's weapon list
    Used for VEHICLES that fire all weapons simultaneously
    
    Returns: List of ranged weapons (excludes melee)
    """
    rangedWeapons = []
    
    for weapon in weapons:
        weaponRange = weapon.get("range")
        if weaponRange != "Melee" and weaponRange is not None:
            rangedWeapons.append(weapon)
    
    return rangedWeapons

# ==================== BELOW HALF-STRENGTH CHECKER ====================

def isBelowHalfStrength(currentModelCount: int, startingStrength: int, 
                       currentWounds: int, maxWounds: int) -> bool:
    """
    Check if a unit is Below Half-strength
    
    Official Rule:
    - If Starting Strength = 1: Below Half-strength when remaining wounds < half of Wounds characteristic
    - Otherwise: Below Half-strength when model count < half of Starting Strength
    
    Returns: True if Below Half-strength
    """
    if startingStrength == 1:
        return currentWounds < (maxWounds / 2)
    else:
        return currentModelCount < (startingStrength / 2)

def getExecutionerModifier(targetModelCount: int, targetStartingStrength: int,
                           targetCurrentWounds: int, targetMaxWounds: int) -> int:
    """
    EXECUTIONER: +1 to hit when targeting Below Half-strength units
    
    Returns: +1 if target is Below Half-strength, 0 otherwise
    """
    if isBelowHalfStrength(targetModelCount, targetStartingStrength, 
                          targetCurrentWounds, targetMaxWounds):
        print(f"\n⚡ [EXECUTIONER] Target is Below Half-strength!")
        print(f"   Effect: +1 to all Hit rolls")
        return 1
    
    return 0

