"""
testMain.py - Complete 40K Game Loop with DUAL UNIT CONTROL
Player controls BOTH units throughout all phases
"""

import TestPhases.datasheets as datasheets 
import TestPhases.utilityFunctions as utilityFunctions 
import TestPhases.commandPhase as commandPhase 
import TestPhases.movementPhase as movementPhase 
import TestPhases.shootingPhase as shootingPhase 
import TestPhases.chargePhase as chargePhase 
import TestPhases.fightPhase as fightPhase

import testUtils as util
import testGameLog as gameLog
import abilitySystem as abilitySys

# ============================================
# CONFIGURATION
# ============================================
print("="*60)
print("🎮 WARHAMMER 40,000 SIMULATOR")
print("="*60)
print("\nSelect Unit 1:")
print("1. Nightbringer")
print("2. Lion el'Jonson")
print("3. Trajann Valoris")
print("4. Custodian Guard")
print("5. Vashtorr")
print("6. Angron")

unit1_choice = input("\nUnit 1 choice (1-5): ")
unit1_map = {
    "1": datasheets.nightbringer,
    "2": datasheets.lion,
    "3": datasheets.trajann,
    "4": datasheets.cust_guard,
    "5": datasheets.vashtorr,
    "6": datasheets.angron
}
controlUnit = unit1_map.get(unit1_choice, datasheets.nightbringer)

print("\nSelect Unit 2:")
print("1. Nightbringer")
print("2. Lion el'Jonson")
print("3. Trajann Valoris")
print("4. Custodian Guard")
print("5. Vashtorr")
print("6. Angron")

unit2_choice = input("\nUnit 2 choice (1-5): ")
unit2_map = {
    "1": datasheets.nightbringer,
    "2": datasheets.lion,
    "3": datasheets.trajann,
    "4": datasheets.cust_guard,
    "5": datasheets.vashtorr,
    "6": datasheets.angron
}
targetUnit = unit2_map.get(unit2_choice, datasheets.lion)

# ============================================
# INITIALIZE GAME STATE
# ============================================

cuName, cuPiece, cuProfile, cuWeapons, cuCount, cuKeywords, \
tuName, tuPiece, tuProfile, tuWeapons, tuCount, tuKeywords = utilityFunctions.dataLoad(
    controlUnit,
    targetUnit
)

gameMap, cuPosition, tuPosition = movementPhase.mapInit(cuPiece, tuPiece)

# Initialize DETAILED game logger
logger = gameLog.GameLogger(cuName, tuName)

# Initialize ability processor
ability_processor = abilitySys.AbilityProcessor({}, logger=logger)


print(f"\nUnit 1: {cuName} (Move: {cuProfile['m']}\")")
print(f"Unit 2: {tuName} (Move: {tuProfile['m']}\")")

game_state = {
    "attacker_unit": controlUnit,
    "defender_unit": targetUnit,
    "attacker_count": cuCount,
    "defender_count": tuCount,
    "attacker_current_wounds": cuProfile["w"],
    "defender_current_wounds": tuProfile["w"],
    "oath_target": None,
    "turn": 1,
    "attacker_position": cuPosition,
    "defender_position": tuPosition,
    
    # Generic ability tracking (replaces unit-specific keys)
    "ability_uses": {},  # Track all ability uses
    "active_effects": {}  # Track active temporary effects
}

# Set ability processor game state
ability_processor.game_state = game_state

# ============================================
# HELPER FUNCTIONS
# ============================================

def apply_mortal_wounds(game_state, is_attacker: bool, mortal_damage: int):
    """Apply mortal wounds with detailed logging"""
    if mortal_damage <= 0:
        return game_state
    
    if is_attacker:
        unit = game_state["attacker_unit"]
        count_key = "attacker_count"
        wounds_key = "attacker_current_wounds"
        name = unit["Name"]
    else:
        unit = game_state["defender_unit"]
        count_key = "defender_count"
        wounds_key = "defender_current_wounds"
        name = unit["Name"]
    
    full_wounds = unit["Profile"]["w"]
    current_count = game_state[count_key]
    current_wounds = game_state[wounds_key]
    
    logger.log_special_event("Mortal Wounds", {
        "target": name,
        "damage": mortal_damage,
        "models_before": current_count,
        "wounds_before": current_wounds
    })
    
    print(f"\n{'='*60}")
    print(f"💀 {name} suffers {mortal_damage} MORTAL WOUNDS!")
    print(f"{'='*60}")
    
    models_lost = 0
    while mortal_damage > 0 and current_count > 0:
        damage_to_apply = min(mortal_damage, current_wounds)
        current_wounds -= damage_to_apply
        mortal_damage -= damage_to_apply
        
        if current_wounds <= 0:
            current_count -= 1
            models_lost += 1
            print(f"💀 Model destroyed by mortal wounds! ({current_count} models remaining)")
            if current_count > 0:
                current_wounds = full_wounds
            else:
                current_wounds = 0
    
    game_state[count_key] = max(current_count, 0)
    game_state[wounds_key] = max(current_wounds, 0)
    
    logger.log_special_event("Mortal Wounds Result", {
        "models_destroyed": models_lost,
        "models_remaining": game_state[count_key],
        "wounds_remaining": game_state[wounds_key]
    })
    
    return game_state

def display_unit_status(game_state):
    """Display current status"""
    attacker = game_state["attacker_unit"]
    defender = game_state["defender_unit"]
    
    print(f"\n{'='*60}")
    print("UNIT STATUS")
    print(f"{'='*60}")
    
    a_count = game_state["attacker_count"]
    a_wounds = game_state["attacker_current_wounds"]
    a_max_wounds = attacker["Profile"]["w"]
    print(f"🔵 {attacker['Name']}: {a_count} models")
    if a_count > 0:
        print(f"   Current wounds on damaged model: {a_wounds}/{a_max_wounds}")
    
    d_count = game_state["defender_count"]
    d_wounds = game_state["defender_current_wounds"]
    d_max_wounds = defender["Profile"]["w"]
    print(f"🔴 {defender['Name']}: {d_count} models")
    if d_count > 0:
        print(f"   Current wounds on damaged model: {d_wounds}/{d_max_wounds}")
    
    print(f"{'='*60}\n")

def check_victory(game_state):
    """Check victory condition"""
    a_count = game_state["attacker_count"]
    d_count = game_state["defender_count"]
    
    if a_count <= 0 and d_count <= 0:
        return (True, "MUTUAL DESTRUCTION")
    elif a_count <= 0:
        return (True, game_state["defender_unit"]["Name"])
    elif d_count <= 0:
        return (True, game_state["attacker_unit"]["Name"])
    
    return (False, None)

def end_game(game_state, logger, winner):
    """Unified game ending"""
    util.clear()
    print(f"\n{'='*60}")
    print(f"🏆 VICTORY: {winner}!")
    print(f"{'='*60}")
    
    logger.log_game_end(
        winner=winner,
        total_turns=game_state['turn'],
        reason="Unit destroyed" if winner != "MUTUAL DESTRUCTION" else "Both units destroyed"
    )
    logger.write_to_file()
    
    print(f"\n🎮 GAME OVER")
    print(f"Total turns played: {game_state['turn']}")
    print("\nThanks for playing!")
    input("\n>>> Press Enter to exit...")

# ============================================
# MAIN GAME LOOP
# ============================================

print(f"\n{'='*60}")
print("🎮 GAME START")
print(f"{'='*60}")

logger.start_game(game_state)

input("Press Enter to begin...")

game_ended = False

while not game_ended:
    util.clear()
    
    turn = game_state["turn"]
    logger.start_turn(turn, game_state)

    print(f"\n{'='*70}")
    print(f"⚔️  TURN {turn}  ⚔️")
    print(f"{'='*70}")
    
    display_unit_status(game_state)
    
    # ===========================
    # 1. COMMAND PHASE
    # ===========================
    print(f"\n{'='*60}")
    print("📋 COMMAND PHASE")
    print(f"{'='*60}")
    
    # Process command phase abilities using ability system
    game_state = abilitySys.process_command_phase_abilities(
        controlUnit, targetUnit, game_state
    )
    
    cuCount = game_state["attacker_count"]
    tuCount = game_state["defender_count"]

    logger.log_command_phase(
        oath_declared=(game_state.get("oath_target") == tuName),
        oath_target=game_state.get("oath_target")
    )
    
    input("\n>>> Press Enter to continue to Movement Phase...")
    
    game_over, winner = check_victory(game_state)
    if game_over:
        end_game(game_state, logger, winner)
        break
    
    # ===========================
    # 2. MOVEMENT PHASE
    # ===========================
    util.clear()
    print(f"\n{'='*60}")
    print("🏃 MOVEMENT PHASE")
    print(f"{'='*60}")

    distance = abs(cuPosition - tuPosition)

    # DUAL CONTROL: Unit 1 moves first
    print(f"\n--- {cuName.upper()} MOVEMENT ---")
    print(f"Current distance to {tuName}: {distance}\"")
    
    cuStationary, cuAdvanced = False, False
    
    if cuCount > 0:
        print(f"\nMovement Options for {cuName}:")
        print("1. Remain Stationary")
        print("2. Normal Move")
        print("3. Advance")
        
        while True:
            try:
                cu_move_choice = int(input(f"Choose movement type for {cuName} (1-3): "))
                if 1 <= cu_move_choice <= 3:
                    break
            except ValueError:
                pass
            print("Please enter 1, 2, or 3")
        
        if cu_move_choice == 1:
            cuStationary = True
            print(f"✓ {cuName} remains STATIONARY")
        elif cu_move_choice == 3:
            cuAdvanced = True
            advance_roll = movementPhase.rollD6()
            max_move = cuProfile['m'] + advance_roll
            print(f"✓ {cuName} ADVANCES! ({cuProfile['m']}\" + {advance_roll}\" = {max_move}\")")
            
            while True:
                try:
                    move_dist = int(input(f"Move {cuName} forward (0-{max_move}): "))
                    if 0 <= move_dist <= max_move:
                        cuPosition = max(0, cuPosition - move_dist)
                        break
                except ValueError:
                    pass
        else:
            # Normal move
            while True:
                try:
                    move_dist = int(input(f"Move {cuName} forward (0-{cuProfile['m']}): "))
                    if 0 <= move_dist <= cuProfile['m']:
                        cuPosition = max(0, cuPosition - move_dist)
                        if move_dist == 0:
                            cuStationary = True
                        break
                except ValueError:
                    pass
    
    # DUAL CONTROL: Unit 2 moves second
    print(f"\n--- {tuName.upper()} MOVEMENT ---")
    
    tuStationary, tuAdvanced = False, False
    
    if tuCount > 0:
        print(f"\nMovement Options for {tuName}:")
        print("1. Remain Stationary")
        print("2. Normal Move")
        print("3. Advance")
        
        while True:
            try:
                tu_move_choice = int(input(f"Choose movement type for {tuName} (1-3): "))
                if 1 <= tu_move_choice <= 3:
                    break
            except ValueError:
                pass
            print("Please enter 1, 2, or 3")
        
        if tu_move_choice == 1:
            tuStationary = True
            print(f"✓ {tuName} remains STATIONARY")
        elif tu_move_choice == 3:
            tuAdvanced = True
            advance_roll = movementPhase.rollD6()
            max_move = tuProfile['m'] + advance_roll
            print(f"✓ {tuName} ADVANCES! ({tuProfile['m']}\" + {advance_roll}\" = {max_move}\")")
            
            while True:
                try:
                    move_dist = int(input(f"Move {tuName} forward (0-{max_move}): "))
                    if 0 <= move_dist <= max_move:
                        tuPosition = min(29, tuPosition + move_dist)
                        break
                except ValueError:
                    pass
        else:
            # Normal move
            while True:
                try:
                    move_dist = int(input(f"Move {tuName} forward (0-{tuProfile['m']}): "))
                    if 0 <= move_dist <= tuProfile['m']:
                        tuPosition = min(29, tuPosition + move_dist)
                        if move_dist == 0:
                            tuStationary = True
                        break
                except ValueError:
                    pass

    # Update positions and distance
    distance = abs(cuPosition - tuPosition)
    game_state["attacker_position"] = cuPosition
    game_state["defender_position"] = tuPosition

    logger.log_movement(distance, {
        f"{cuName}_stationary": cuStationary,
        f"{cuName}_advanced": cuAdvanced,
        f"{tuName}_stationary": tuStationary,
        f"{tuName}_advanced": tuAdvanced
    }, {})

    print(f"\nFinal distance: {distance}\"")

    input("\n>>> Press Enter to continue to Shooting Phase...")
    
    # ===========================
    # 3. SHOOTING PHASE - Unit 1
    # ===========================
    util.clear()
    print(f"\n{'='*60}")
    print(f"🔫 {cuName.upper()} SHOOTING PHASE")
    print(f"{'='*60}")
    print(f"Distance to target: {distance}\"")

    target_has_cover = input(f"Does {tuName} have cover? (y/n): ").lower() == 'y'

    tuCount_before = tuCount

    # Use shooting phase with ability system
    result = shootingPhase.shootPhase(
        attackerWeapons=cuWeapons,
        attackerProfile=cuProfile,
        targetProfile=tuProfile,
        targetUnit=targetUnit,
        attackerModelCount=cuCount,
        targetModelCount=tuCount,
        targetCurrentWounds=game_state["defender_current_wounds"],
        distance=distance,
        attackerName=cuName,
        targetName=tuName,
        targetKeywords=tuKeywords,
        attackerUnit=controlUnit,
        attackerKeywords=cuKeywords,
        targetStartingStrength=targetUnit["Model Count"],
        attackerCurrentWounds=game_state["attacker_current_wounds"],
        isStationary=cuStationary,
        didAdvance=cuAdvanced,
        didCharge=False,
        targetHasCover=target_has_cover,
        game_state=game_state,  # Ensure game_state is passed
        ability_logger=logger   # ADD: Pass logger
    )

    if result:
        tuCount, tuCurrentWounds, hazardous, combat_stats = result
        game_state["defender_count"] = tuCount
        game_state["defender_current_wounds"] = tuCurrentWounds
        
        # ✅ FIX: Get the actual weapon that was used for proper stat logging
        selected_weapon = None
        for weapon in cuWeapons:
            if weapon.get("name") == combat_stats.get("weapon_name"):
                selected_weapon = weapon
                break
        
        logger.log_shooting(
            shooter=cuName,
            target=tuName,
            weapon_name=combat_stats.get("weapon_name", ""),
            weapon_stats=selected_weapon,  # ✅ Pass actual weapon dict
            hits=combat_stats.get("total_hits", 0),
            wounds=combat_stats.get("total_wounds", 0),
            saves_failed=combat_stats.get("failed_saves", 0),
            damage_dealt=combat_stats.get("damage_dealt", 0),
            models_destroyed=combat_stats.get("models_destroyed", 0),
            hazardous_damage=hazardous
        )
        
        if hazardous > 0:
            game_state = apply_mortal_wounds(game_state, True, hazardous)
            cuCount = game_state["attacker_count"]

    game_over, winner = check_victory(game_state)
    if game_over:
        logger.end_turn(game_state)
        end_game(game_state, logger, winner)
        break

    input("\n>>> Press Enter to continue to Unit 2's Shooting Phase...")

    # ===========================
    # 4. SHOOTING PHASE - Unit 2
    # ===========================
    util.clear()
    print(f"\n{'='*60}")
    print(f"🔫 {tuName.upper()} SHOOTING PHASE")
    print(f"{'='*60}")
    print(f"Distance to target: {distance}\"")

    attacker_has_cover = input(f"Does {cuName} have cover? (y/n): ").lower() == 'y'

    cuCount_before = cuCount

    result = shootingPhase.shootPhase(
        attackerWeapons=tuWeapons,
        attackerProfile=tuProfile,
        targetProfile=cuProfile,
        targetUnit=controlUnit,
        attackerModelCount=tuCount,
        targetModelCount=cuCount,
        targetCurrentWounds=game_state["attacker_current_wounds"],
        distance=distance,
        attackerName=tuName,
        targetName=cuName,
        targetKeywords=cuKeywords,
        attackerUnit=targetUnit,
        attackerKeywords=tuKeywords,
        targetStartingStrength=controlUnit["Model Count"],
        attackerCurrentWounds=game_state["defender_current_wounds"],
        isStationary=tuStationary,
        didAdvance=tuAdvanced,
        didCharge=False,
        targetHasCover=attacker_has_cover,
        game_state=game_state,  # Ensure game_state is passed
        ability_logger=logger   # ADD: Pass logger
    )

    if result:
        cuCount, cuCurrentWounds, hazardous, combat_stats = result
        game_state["attacker_count"] = cuCount
        game_state["attacker_current_wounds"] = cuCurrentWounds
        
        # ✅ FIX: Get the actual weapon that was used for proper stat logging
        selected_weapon = None
        for weapon in tuWeapons:
            if weapon.get("name") == combat_stats.get("weapon_name"):
                selected_weapon = weapon
                break
        
        logger.log_shooting(
            shooter=tuName,
            target=cuName,
            weapon_name=combat_stats.get("weapon_name", ""),
            weapon_stats=selected_weapon,  # ✅ Pass actual weapon dict
            hits=combat_stats.get("total_hits", 0),
            wounds=combat_stats.get("total_wounds", 0),
            saves_failed=combat_stats.get("failed_saves", 0),
            damage_dealt=combat_stats.get("damage_dealt", 0),
            models_destroyed=combat_stats.get("models_destroyed", 0),
            hazardous_damage=hazardous
        )
        
        if hazardous > 0:
            game_state = apply_mortal_wounds(game_state, False, hazardous)
            tuCount = game_state["defender_count"]

    game_over, winner = check_victory(game_state)
    if game_over:
        logger.end_turn(game_state)
        end_game(game_state, logger, winner)
        break
    
    # ===========================
    # 5. CHARGE PHASE
    # ===========================
    util.clear()
    print(f"\n{'='*60}")
    print(f"⚔️ CHARGE PHASE")
    print(f"{'='*60}")
    
    # DUAL CONTROL: Unit 1 charges
    print(f"\n--- {cuName.upper()} ---")
    
    if chargePhase.canDeclareCharge(distance, cuWeapons) and not cuAdvanced:
        wants_charge = input(f"Does {cuName} declare a charge? (y/n): ").lower() == 'y'
        
        if wants_charge:
            game_state = chargePhase.crgPhase(
                game_state, cuWeapons, cuName, tuName,
                distance, cuAdvanced, False, distance <= 1
            )
            
            if game_state.get("charge_successful"):
                distance = 1
                game_state["cu_charged"] = True
    
    # DUAL CONTROL: Unit 2 charges
    print(f"\n--- {tuName.upper()} ---")
    
    if chargePhase.canDeclareCharge(distance, tuWeapons) and not tuAdvanced:
        wants_charge = input(f"Does {tuName} declare a charge? (y/n): ").lower() == 'y'
        
        if wants_charge:
            temp_state = chargePhase.crgPhase(
                {}, tuWeapons, tuName, cuName,
                distance, tuAdvanced, False, distance <= 1
            )
            
            if temp_state.get("charge_successful"):
                distance = 1
                game_state["tu_charged"] = True

    input("\n>>> Press Enter to continue to Fight Phase...")
    
    # ===========================
    # 6. FIGHT PHASE
    # ===========================
    util.clear()
    print(f"\n{'='*60}")
    print(f"⚔️ FIGHT PHASE")
    print(f"{'='*60}")

    cu_charged = game_state.get("cu_charged", False)
    tu_charged = game_state.get("tu_charged", False)

    cu_can_fight = distance <= 1 or cu_charged
    tu_can_fight = distance <= 1 or tu_charged

    if not cu_can_fight and not tu_can_fight:
        print(f"\nNo units are eligible to fight")
    else:
        # Determine fight order
        cu_fights_first = cu_charged or controlUnit.get("Fights First", False)
        tu_fights_first = tu_charged or targetUnit.get("Fights First", False)
        
        fight_order = []
        if cu_fights_first and cu_can_fight:
            fight_order.append(("cu", True))
        if tu_fights_first and tu_can_fight:
            fight_order.append(("tu", True))
        
        # Add remaining fights
        if not cu_fights_first and cu_can_fight:
            fight_order.append(("cu", False))
        if not tu_fights_first and tu_can_fight:
            fight_order.append(("tu", False))
        
        # Execute fights in order
        for unit_type, fights_first in fight_order:
            if game_ended:
                break
            
            if unit_type == "cu":
                print(f"\n{'='*60}")
                print(f"⚔️ {cuName.upper()} FIGHTS")
                if fights_first:
                    print("⚡ FIGHTS FIRST")
                print(f"{'='*60}")
                
                result = fightPhase.ftPhase(
                    cuWeapons, cuProfile, controlUnit,
                    tuProfile, targetUnit,
                    cuCount, tuCount,
                    game_state["defender_current_wounds"],
                    distance, cuName, tuName, tuKeywords,
                    fights_first, cu_charged, game_state,
                    ability_logger=logger   # ADD: Pass logger
                )
                
                if result:
                    tuCount, tuCurrentWounds, combat_stats = result
                    game_state["defender_count"] = tuCount
                    game_state["defender_current_wounds"] = tuCurrentWounds
                    
                    # ✅ FIX: Get the actual weapon that was used
                    selected_weapon = None
                    for weapon in cuWeapons:
                        if weapon.get("name") == combat_stats.get("weapon_name"):
                            selected_weapon = weapon
                            break
                    
                    logger.log_fight(
                        fighter=cuName,
                        target=tuName,
                        weapon_name=combat_stats.get("weapon_name", ""),
                        weapon_stats=selected_weapon,  # ✅ Pass actual weapon dict
                        hits=combat_stats.get("total_hits", 0),
                        wounds=combat_stats.get("total_wounds", 0),
                        saves_failed=combat_stats.get("failed_saves", 0),
                        damage_dealt=combat_stats.get("damage_dealt", 0),
                        models_destroyed=combat_stats.get("models_destroyed", 0),
                        fights_first=fights_first
                    )
            
            else:  # tu
                print(f"\n{'='*60}")
                print(f"⚔️ {tuName.upper()} FIGHTS")
                if fights_first:
                    print("⚡ FIGHTS FIRST")
                print(f"{'='*60}")
                
                result = fightPhase.ftPhase(
                    tuWeapons, tuProfile, targetUnit,
                    cuProfile, controlUnit,
                    tuCount, cuCount,
                    game_state["attacker_current_wounds"],
                    distance, tuName, cuName, cuKeywords,
                    fights_first, tu_charged, game_state,
                    ability_logger=logger   # ADD: Pass logger
                )
                
                if result:
                    cuCount, cuCurrentWounds, combat_stats = result
                    game_state["attacker_count"] = cuCount
                    game_state["attacker_current_wounds"] = cuCurrentWounds
                    
                    # ✅ FIX: Get the actual weapon that was used
                    selected_weapon = None
                    for weapon in tuWeapons:
                        if weapon.get("name") == combat_stats.get("weapon_name"):
                            selected_weapon = weapon
                            break
                    
                    logger.log_fight(
                        fighter=tuName,
                        target=cuName,
                        weapon_name=combat_stats.get("weapon_name", ""),
                        weapon_stats=selected_weapon,  # ✅ Pass actual weapon dict
                        hits=combat_stats.get("total_hits", 0),
                        wounds=combat_stats.get("total_wounds", 0),
                        saves_failed=combat_stats.get("failed_saves", 0),
                        damage_dealt=combat_stats.get("damage_dealt", 0),
                        models_destroyed=combat_stats.get("models_destroyed", 0),
                        fights_first=fights_first
                    )
            
            game_over, winner = check_victory(game_state)
            if game_over:
                logger.end_turn(game_state)
                end_game(game_state, logger, winner)
                game_ended = True
                break

    if game_ended:
        break

    # Clear charge flags
    game_state["cu_charged"] = False
    game_state["tu_charged"] = False

    # ===========================
    # END OF TURN
    # ===========================
    print(f"\n{'='*60}")
    print(f"END OF TURN {turn}")
    print(f"{'='*60}")
    
    display_unit_status(game_state)
    
    logger.end_turn(game_state)
    
    game_state["turn"] = turn + 1
    
    if turn >= 10:
        if cuCount > tuCount:
            winner = cuName
        elif tuCount > cuCount:
            winner = tuName
        else:
            winner = "DRAW"
        
        end_game(game_state, logger, winner)
        break
    
    input("\n>>> Press Enter to begin next turn...")