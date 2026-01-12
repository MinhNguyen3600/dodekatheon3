"""
Fight Phase implementation - Melee combat with Pile In, attacks, and Consolidate
FULLY MODULAR - Uses abilitySystem.py for ALL abilities
NO unit-specific code
"""

import rolls as rolls
import weaponAbilityDict as wad
import abilitySystem as abilitySys
from .utilityFunctions import parseDiceNotation


def ftPhase(attackerWeapons: list, attackerProfile: dict, attackerUnit: dict,
           targetProfile: dict, targetUnit: dict, attackerModelCount: int,
           targetModelCount: int, targetCurrentWounds: int, distance: int,
           attackerName: str, targetName: str, targetKeywords: list,
           fightsFirst: bool = False, chargedThisTurn: bool = False,
           game_state: dict = None, ability_logger = None) -> tuple:
    """
    Execute the fight phase for a unit
    Returns: (remaining target models, current target wounds, combat_stats dict)
    
    This function uses ONLY the ability system - no hardcoded ability checks
    """
    
    print(f"\n{'='*60}")
    print(f"⚔️ {attackerName.upper()} FIGHTS")
    print(f"{'='*60}")
    
    # Check eligibility
    isWithinEngagement = distance <= 1
    
    if not isWithinEngagement and not chargedThisTurn:
        print(f"❌ {attackerName} cannot fight - not in Engagement Range and did not charge")
        return (targetModelCount, targetCurrentWounds, {"weapon_name": "None"})
    
    if fightsFirst:
        print(f"⚡ {attackerName} has FIGHTS FIRST!")
    
    # Initialize ability processor
    if game_state is None:
        game_state = {}
    
    processor = abilitySys.AbilityProcessor(game_state, logger=ability_logger)
    
    # ✅ GENERIC: Process abilities that trigger before fighting
    context = {
        "unit_name": attackerName,
        "target_name": targetName,
        "distance": distance,
        "did_charge": chargedThisTurn,
        "is_melee": True,
        "attacker_model_count": attackerModelCount,
        "target_model_count": targetModelCount,
        "target_keywords": targetKeywords
    }
    
    # Check for abilities that trigger at start of fight/before fight
    for trigger in ["start_of_fight", "before_fight"]:
        unit_ability = attackerUnit.get("Ability", {})
        
        if processor.check_trigger(unit_ability, trigger, **context):
            # Check if player choice is required
            if unit_ability.get("player_choice", False):
                if processor.prompt_player_activation(unit_ability, attackerName):
                    effects = processor.apply_effects(unit_ability, **context)
                    processor.mark_ability_used(unit_ability, attackerName)
                    
                    # Handle special effects (like stance selection)
                    for effect in effects.get("special_effects", []):
                        if isinstance(effect, tuple) and effect[0] == "CHOOSE_STANCE":
                            game_state = handle_stance_choice(attackerUnit, game_state, effect[1])
            else:
                # Auto-activate ability
                effects = processor.apply_effects(unit_ability, **context)
                processor.mark_ability_used(unit_ability, attackerName)

    # Get melee weapons
    meleeWeapons = getMeleeWeapons(attackerWeapons)
    
    if len(meleeWeapons) == 0:
        print(f"❌ {attackerName} has no melee weapons!")
        return (targetModelCount, targetCurrentWounds, {"weapon_name": "None"})
    
    # ✅ GENERIC: Apply weapon modifications from active abilities
    if game_state is not None:
        modifiedWeapons = []
        for weapon in meleeWeapons:
            modifiedWeapon = apply_ability_weapon_modifications(
                weapon, attackerUnit, game_state
            )
            modifiedWeapons.append(modifiedWeapon)
        meleeWeapons = modifiedWeapons
    
    # STEP 1: PILE IN
    print(f"\n--- STEP 1: PILE IN ---")
    if distance > 1:
        print(f"{attackerName} piles in 3\" toward {targetName}")
        print(f"Units are now in Engagement Range!")
    else:
        print(f"{attackerName} is already in base-to-base contact")
    
    # STEP 2: MAKE MELEE ATTACKS
    print(f"\n--- STEP 2: MAKE MELEE ATTACKS ---")
    
    # Select weapon
    selectedWeapon = selectMeleeWeapon(meleeWeapons, attackerName)
    
    if selectedWeapon is None:
        return (targetModelCount, targetCurrentWounds, {"weapon_name": "None"})
    
    weaponAbilities = selectedWeapon.get("weapon abilities", [])
    
    # Display weapon and abilities
    print(f"\n{attackerName} attacks with {selectedWeapon['name']}")
    wad.displayActiveAbilities(weaponAbilities, targetKeywords)
    
    # Calculate attacks (multiply by model count)
    baseAttacksPerModel = parseDiceNotation(selectedWeapon["a"])
    totalAttacks = baseAttacksPerModel * attackerModelCount
    
    print(f"\nAttacks: {baseAttacksPerModel} per model × {attackerModelCount} models = {totalAttacks} attacks")
    
    # Make attacks (same sequence as shooting)
    remainingModels, currentWounds, combat_stats = resolveMeleeAttacks(
        selectedWeapon,
        weaponAbilities,
        totalAttacks,
        attackerProfile,
        attackerUnit,
        targetProfile,
        targetUnit,
        targetModelCount,
        targetCurrentWounds,
        attackerName,
        targetName,
        targetKeywords,
        chargedThisTurn,
        distance,
        game_state
    )
    
    # STEP 3: CONSOLIDATE
    print(f"\n--- STEP 3: CONSOLIDATE ---")
    if remainingModels > 0:
        print(f"{attackerName} consolidates - remains in Engagement Range")
    else:
        print(f"{targetName} has been destroyed - no consolidation needed")
    
    # Add weapon name to stats
    combat_stats["weapon_name"] = selectedWeapon["name"]
    
    # ✅ GENERIC: Deactivate temporary abilities
    deactivate_fight_phase_abilities(attackerUnit, game_state)
    
    return (remainingModels, currentWounds, combat_stats)


def getMeleeWeapons(weapons: list) -> list:
    """
    Filter and return only melee weapons
    
    Official Rule: Melee weapons have range "Melee" or very short range (2" or less)
    """
    meleeWeapons = []
    for weapon in weapons:
        weaponRange = weapon.get("range")
        if weaponRange == "Melee":
            meleeWeapons.append(weapon)
        elif isinstance(weaponRange, int) and weaponRange <= 2:
            meleeWeapons.append(weapon)
    
    return meleeWeapons


def selectMeleeWeapon(weapons: list, unitName: str) -> dict:
    """Allow player to select a melee weapon"""
    if len(weapons) == 0:
        return None
    elif len(weapons) == 1:
        print(f"{unitName} automatically uses: {weapons[0]['name']}")
        return weapons[0]
    else:
        print(f"\n{unitName} has multiple melee weapons:")
        for i, weapon in enumerate(weapons):
            print(f"{i+1}. {weapon['name']} (Attacks: {weapon['a']}, S: {weapon['s']}, AP: {weapon['ap']}, D: {weapon['d']})")
        
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


def apply_ability_weapon_modifications(weapon: dict, unit: dict, game_state: dict) -> dict:
    """
    ✅ GENERIC: Apply weapon modifications from active abilities
    
    Checks game_state for active ability effects and applies them to weapons
    NO hardcoded ability names
    """
    # Only modify melee weapons
    if weapon.get("range") != "Melee":
        return weapon
    
    modifiedWeapon = weapon.copy()
    unitName = unit["Name"]
    
    # Check for active effects in game_state
    # Pattern: {unitName}_{abilityName}_active
    active_effects = []
    for key, value in game_state.items():
        if key.startswith(f"{unitName}_") and key.endswith("_active") and value:
            active_effects.append(key)
    
    # If there are active effects, check the unit's ability for modifications
    if active_effects:
        unit_ability = unit.get("Ability", {})
        if unit_ability:
            effects = unit_ability.get("effects", [])
            
            for effect in effects:
                effect_type = effect.get("type")
                
                # Modify Attacks
                if effect_type == "modifyAttacks":
                    target = effect.get("target", "")
                    if "meleeWeapons" in target or target == "":
                        operation = effect.get("operation", "add")
                        value = effect.get("value", 0)
                        
                        # Check if effect applies to this weapon
                        weapon_name_filter = effect.get("weapon")
                        if weapon_name_filter and weapon_name_filter != weapon.get("name"):
                            continue
                        
                        if operation == "set":
                            modifiedWeapon["a"] = value
                            print(f"  [ABILITY] {weapon['name']}: Attacks → {value}")
                        else:
                            current_a = weapon.get("a")
                            if isinstance(current_a, int):
                                modifiedWeapon["a"] = current_a + value
                            else:
                                base = parseDiceNotation(str(current_a))
                                modifiedWeapon["a"] = base + value
                            print(f"  [ABILITY] {weapon['name']}: Attacks {weapon['a']} → {modifiedWeapon['a']}")
                
                # Add Weapon Ability
                elif effect_type == "addWeaponAbility":
                    target = effect.get("target", "")
                    if "meleeWeapons" in target or target == "":
                        ability_to_add = effect.get("ability")
                        if ability_to_add:
                            weaponAbilities = list(modifiedWeapon.get("weapon abilities", []))
                            if ability_to_add not in weaponAbilities:
                                weaponAbilities.append(ability_to_add)
                                modifiedWeapon["weapon abilities"] = weaponAbilities
                                print(f"  [ABILITY] {weapon['name']}: Gained [{ability_to_add}]")
    
    # Check for faction ability effects (like Martial Ka'tah stances)
    faction_ability = unit.get("Faction Ability", "")
    if faction_ability:
        # Check for active stance in game_state
        stance_key = f"{unitName}_selected_stance"
        if stance_key in game_state:
            stance_effects = game_state[stance_key]
            
            # Apply stance effects
            if isinstance(stance_effects, dict):
                ability_to_add = stance_effects.get("ability")
                if ability_to_add:
                    weaponAbilities = list(modifiedWeapon.get("weapon abilities", []))
                    if ability_to_add not in weaponAbilities:
                        weaponAbilities.append(ability_to_add)
                        modifiedWeapon["weapon abilities"] = weaponAbilities
                        print(f"  [{stance_effects.get('name', 'STANCE')}] {weapon['name']}: Gained [{ability_to_add}]")
    
    return modifiedWeapon


def handle_stance_choice(unit: dict, game_state: dict, stance_effect: dict) -> dict:
    """
    ✅ GENERIC: Handle stance/choice selection from abilities
    
    NO hardcoded ability names
    """
    unitName = unit["Name"]
    options = stance_effect.get("options", {})
    
    if not options:
        return game_state
    
    print(f"\n{'='*60}")
    print(f"⚡ SELECT OPTION - {unitName}")
    print(f"{'='*60}")
    
    option_list = list(options.items())
    for i, (key, option_data) in enumerate(option_list, 1):
        name = option_data.get("name", key)
        description = option_data.get("description", "")
        print(f"  {i}. {name}")
        if description:
            print(f"     {description}")
    
    print(f"{'='*60}")
    
    while True:
        try:
            choice = int(input(f"Select option (1-{len(option_list)}): "))
            if 1 <= choice <= len(option_list):
                break
        except ValueError:
            pass
        print(f"Invalid choice. Please enter 1-{len(option_list)}")
    
    selected_key, selected_option = option_list[choice - 1]
    
    # Store selected option in game_state
    stance_key = f"{unitName}_selected_stance"
    game_state[stance_key] = selected_option
    
    print(f"\n⚡ {selected_option.get('name', selected_key).upper()} SELECTED!")
    
    return game_state


def deactivate_fight_phase_abilities(unit: dict, game_state: dict) -> dict:
    """
    ✅ GENERIC: Deactivate abilities that last until end of fight phase
    
    NO hardcoded ability names
    """
    unitName = unit["Name"]
    
    # Check unit ability for duration
    unit_ability = unit.get("Ability", {})
    if unit_ability:
        duration = unit_ability.get("duration", "")
        ability_name = unit_ability.get("name", "")
        
        if duration in ["this_phase", "until_end_of_phase"]:
            active_key = f"{unitName}_{ability_name}_active"
            if game_state.get(active_key, False):
                print(f"\n⚡ [{ability_name.upper()}] Effect ends for {unitName}")
                game_state[active_key] = False
    
    # Clear stance selections
    stance_key = f"{unitName}_selected_stance"
    if stance_key in game_state:
        del game_state[stance_key]
    
    return game_state


def resolveMeleeAttacks(weapon: dict, weaponAbilities: list, attackCount: int,
                       attackerProfile: dict, attackerUnit: dict, targetProfile: dict, 
                       targetUnit: dict, targetModelCount: int, targetCurrentWounds: int,
                       attackerName: str, targetName: str, targetKeywords: list,
                       didCharge: bool, distance: int = 0, game_state: dict = None) -> tuple:
    """
    ✅ GENERIC: Resolve melee attacks using ability system
    Returns: (remaining models, current wounds, combat_stats dict)
    
    NO unit-specific checks
    """
    
    # Initialize combat stats tracker
    combat_stats = {
        "total_hits": 0,
        "total_wounds": 0,
        "failed_saves": 0,
        "damage_dealt": 0,
        "models_destroyed": 0
    }
    
    if attackCount == 0:
        return (targetModelCount, targetCurrentWounds, combat_stats)
    
    ws = weapon["ws"]
    
    # === HIT ROLLS ===
    print(f"\n--- HIT ROLLS ---")
    print(f"Making {attackCount} attacks with WS {ws}+")
    
    # ✅ GENERIC: Get hit modifiers from abilities
    if game_state is None:
        game_state = {}
    
    processor = abilitySys.AbilityProcessor(game_state)
    
    context = {
        "unit_name": attackerName,
        "target_name": targetName,
        "distance": distance,
        "is_melee": True,
        "target_keywords": targetKeywords
    }
    
    # Get hit modifiers from attacker abilities
    hit_modifier = abilitySys.get_hit_modifiers(
        attackerUnit, targetUnit, weapon, game_state, **context
    )
    
    if hit_modifier != 0:
        print(f"Hit roll modifier: {hit_modifier:+d}")
    
    # Roll hits
    hitRolls = rolls.rollBox(attackCount)
    print(f"Hit rolls: {hitRolls}")
    
    normalHits = 0
    lethalHitCrits = 0
    
    for roll in hitRolls:
        modifiedRoll = roll + hit_modifier
        if roll == 1:
            continue
        isCritical = (roll == 6)
        if modifiedRoll >= ws or isCritical:
            if isCritical and wad.isLethalHits(roll, weaponAbilities):
                lethalHitCrits += 1
            else:
                normalHits += 1
    
    combat_stats["total_hits"] = normalHits + lethalHitCrits
    
    print(f"Results: {normalHits} normal hits", end="")
    if lethalHitCrits > 0:
        print(f", {lethalHitCrits} LETHAL HITS")
    else:
        print()
    
    if normalHits == 0 and lethalHitCrits == 0:
        print("\nAll attacks missed!")
        return (targetModelCount, targetCurrentWounds, combat_stats)
    
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
    
    # Get wound modifiers (LANCE, etc.)
    woundModifier = wad.getWoundModifiers(weaponAbilities, didCharge)
    
    # ✅ GENERIC: Add wound modifiers from abilities
    ability_wound_mod = abilitySys.get_wound_modifiers(
        attackerUnit, weapon, game_state, **context
    )
    woundModifier += ability_wound_mod
    
    if woundModifier != 0:
        print(f"Wound roll modifier: {woundModifier:+d}")
    
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
    
    # Roll wounds
    woundRolls = rolls.rollBox(normalHits)
    print(f"Wound rolls: {woundRolls}")
    
    # ✅ GENERIC: Check for wound rerolls from abilities
    attacker_ability = attackerUnit.get("Ability", {})
    if attacker_ability:
        if processor.check_trigger(attacker_ability, "on_wound_roll", **context):
            effects = processor.apply_effects(attacker_ability, **context)
            rerolls = effects.get("rerolls", {})
            
            if "wounds" in rerolls:
                reroll_type = rerolls["wounds"]
                
                if reroll_type == "1s":
                    reroll_indices = [i for i, roll in enumerate(woundRolls) if roll == 1]
                elif reroll_type == "failed":
                    reroll_indices = [i for i, roll in enumerate(woundRolls) 
                                     if (roll + woundModifier) < woundThreshold]
                elif reroll_type == "all":
                    reroll_indices = list(range(len(woundRolls)))
                else:
                    reroll_indices = []
                
                if reroll_indices:
                    ability_name = attacker_ability.get("name", "ABILITY")
                    print(f"\n⚔️ [{ability_name}] Re-rolling {len(reroll_indices)} wound roll(s)")
                    
                    reroll_choice = input(f"Re-roll wounds? (y/n): ").lower()
                    if reroll_choice == 'y':
                        reroll_results = rolls.rollBox(len(reroll_indices))
                        print(f"Re-roll results: {reroll_results}")
                        
                        for i, new_roll in zip(reroll_indices, reroll_results):
                            woundRolls[i] = new_roll
    
    normalWounds = 0
    criticalWounds = 0
    
    for roll in woundRolls:
        modifiedRoll = roll + woundModifier
        isCritical = wad.checkCriticalWound(roll, weaponAbilities, targetKeywords)
        if isCritical:
            criticalWounds += 1
        elif modifiedRoll >= woundThreshold:
            normalWounds += 1
    
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
        criticalWounds = 0
    
    totalWounds = normalWounds + criticalWounds + lethalHitCrits
    
    if totalWounds == 0 and devastatingDamage == 0:
        print("\nAll wounds failed!")
        return (targetModelCount, targetCurrentWounds, combat_stats)
    
    # === SAVE ROLLS ===
    print(f"\n--- SAVE ROLLS ---")
    print(f"Target must make {totalWounds} save rolls")
    
    save = targetProfile["sv"]
    invSave = targetProfile.get("inv-sv", 7)
    
    # ✅ GENERIC: Check for invuln modifiers from abilities
    target_ability = targetUnit.get("Ability", {})
    if target_ability:
        target_context = {"unit_name": targetName, "is_melee": True}
        if processor.check_trigger(target_ability, "on_save_roll", **target_context):
            effects = processor.apply_effects(target_ability, **target_context)
            
            for effect in effects.get("special_effects", []):
                if isinstance(effect, tuple) and effect[0] == "CHANGE_INVULN":
                    new_invuln = effect[1]
                    if new_invuln < invSave:
                        invSave = new_invuln
                        ability_name = target_ability.get("name", "ABILITY")
                        print(f"[{ability_name}] Using {new_invuln}+ invulnerable save")
    
    ap = abs(weapon["ap"])
    modifiedSave = save + ap
    
    if invSave < modifiedSave:
        saveToUse = invSave
        print(f"Using Invulnerable Save: {saveToUse}+")
    else:
        saveToUse = modifiedSave
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
    
    totalDamageInstances = failedSaves
    
    # Allocate normal damage
    for i in range(totalDamageInstances):
        damage = parseDiceNotation(weapon["d"])
        
        # Apply Feel No Pain
        if hasFNP:
            actualDamage = wad.applyFeelNoPain(damage, fnpThreshold, targetName)
        else:
            actualDamage = damage
        
        if actualDamage <= 0:
            print(f"Damage instance {i+1}: {damage} damage rolled, all ignored by FNP!")
            continue
        
        damageDealt = min(actualDamage, currentModelWounds)
        currentModelWounds -= damageDealt
        
        print(f"Damage instance {i+1}: {damage} → {actualDamage} after FNP → {damageDealt} dealt", end="")
        
        if currentModelWounds <= 0:
            modelsRemaining -= 1
            print(f" - Model destroyed! ({modelsRemaining} remaining)")
            currentModelWounds = modelWounds
            if modelsRemaining <= 0:
                break
        else:
            print(f" - Model has {currentModelWounds}/{modelWounds} wounds")
    
    # Allocate mortal damage
    if devastatingDamage > 0:
        print(f"\nApplying {devastatingDamage} mortal damage")
        
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
        combat_stats["damage_dealt"] = (models_lost - 1) * modelWounds + (modelWounds - currentModelWounds) if modelsRemaining > 0 else models_lost * modelWounds
    else:
        combat_stats["damage_dealt"] = initialWounds - currentModelWounds
    
    print(f"\nFinal result: {modelsRemaining} models remaining")
    
    return (modelsRemaining, currentModelWounds if modelsRemaining > 0 else modelWounds, combat_stats)