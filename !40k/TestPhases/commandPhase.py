"""
Command Phase implementation - Faction abilities and battle-shock
"""

from .utilityFunctions import rollD3


def cmdPhase(game_state):
    """
    Execute the command phase with proper ability timing.
    
    Args:
        game_state: Dictionary containing unit and game data
    
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
    
    # Base effect: Heal damaged models
    if current_count > 0 and current_wounds < max_wounds:
        healing = rollD3()
        new_wounds = min(current_wounds + healing, max_wounds)
        game_state["attacker_current_wounds"] = new_wounds
        
        print(f"  ✓ Healed {healing} wounds ({current_wounds} → {new_wounds})")
    
    # Special condition: Return destroyed models
    models_destroyed = max_count - current_count
    
    if models_destroyed > 0 and current_count > 0 and max_count > 1:
        game_state["attacker_count"] = current_count + 1
        game_state["attacker_current_wounds"] = 1
        
        print(f"  ✓ Returned 1 destroyed model to the unit!")
        print(f"    Models: {current_count} → {current_count + 1}")
    elif models_destroyed == 0 and current_count > 0 and current_wounds == max_wounds:
        print(f"  No damage taken - Reanimation has no effect")
    elif current_count == 0:
        print(f"  Unit completely destroyed - cannot reanimate")
    
    return game_state