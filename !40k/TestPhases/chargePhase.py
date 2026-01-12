"""
Charge Phase implementation - Declaring charges and moving into combat
"""

from .utilityFunctions import rollD6


def crgPhase(game_state, attackerWeapons: list, attackerName: str, 
                defenderName: str, distance: int, didAdvance: bool, 
                didFallBack: bool, isWithinEngagement: bool) -> dict:
    """
    Execute the charge phase
    
    Args:
        game_state: Current game state dictionary
        attackerWeapons: List of attacker's weapons
        attackerName: Name of attacking unit
        defenderName: Name of defending unit
        distance: Current distance between units
        didAdvance: Did attacker advance this turn?
        didFallBack: Did attacker fall back this turn?
        isWithinEngagement: Is attacker already in engagement range?
    
    Returns:
        Updated game_state with charge results
    """
    
    print(f"\n{'='*60}")
    print(f"⚔️ {attackerName.upper()} CHARGE PHASE")
    print(f"{'='*60}")
    
    # Initialize charge state
    game_state["charge_successful"] = False
    game_state["fights_first"] = False
    
    # Check if unit has melee weapons
    hasMeleeWeapons = any(
        w.get("range") == "Melee" or (isinstance(w.get("range"), int) and w.get("range") <= 2)
        for w in attackerWeapons
    )
    
    if not hasMeleeWeapons:
        print(f"❌ {attackerName} has no melee weapons - cannot charge")
        return game_state
    
    # Check eligibility
    print(f"\n--- CHARGE ELIGIBILITY CHECK ---")
    print(f"Distance to {defenderName}: {distance}\"")
    
    if not isChargeEligible(distance, didAdvance, didFallBack, isWithinEngagement, attackerName):
        return game_state
    
    # Declare charge
    print(f"\n✓ {attackerName} declares a charge against {defenderName}!")
    
    # Make charge roll
    chargeRoll = makeChargeRoll()
    
    # Check if charge is successful
    if chargeRoll < distance:
        print(f"\n❌ CHARGE FAILED!")
        print(f"   Need {distance}\" to reach target, rolled {chargeRoll}\"")
        return game_state
    
    # Charge successful
    print(f"\n✅ CHARGE SUCCESSFUL!")
    print(f"   {attackerName} moves {distance}\" into combat!")
    
    game_state["charge_successful"] = True
    game_state["fights_first"] = True
    game_state["charged_this_turn"] = True
    
    print(f"\n⚡ {attackerName} gains FIGHTS FIRST until end of turn!")
    
    return game_state


def isChargeEligible(distance: int, didAdvance: bool, didFallBack: bool, 
                     isWithinEngagement: bool, unitName: str) -> bool:
    """
    Check if a unit is eligible to charge
    
    Official Rules:
    - Within 12" of enemy units
    - Did not Advance or Fall Back this turn
    - Not within Engagement Range of enemy models
    - Not an AIRCRAFT (we don't handle this in our simplified system)
    
    Returns: True if eligible to charge
    """
    
    # Check distance (must be within 12")
    if distance > 12:
        print(f"❌ {unitName} cannot charge - target is {distance}\" away (max 12\")")
        return False
    
    # Check if already in engagement range
    if isWithinEngagement:
        print(f"❌ {unitName} cannot charge - already in Engagement Range")
        return False
    
    # Check if Advanced this turn
    if didAdvance:
        print(f"❌ {unitName} cannot charge - Advanced this turn")
        return False
    
    # Check if Fell Back this turn
    if didFallBack:
        print(f"❌ {unitName} cannot charge - Fell Back this turn")
        return False
    
    print(f"✓ {unitName} is eligible to charge")
    return True


def makeChargeRoll() -> int:
    """
    Make a charge roll (2D6)
    
    Official Rule: "You then make a Charge roll for the charging unit by rolling 2D6."
    
    Returns: Total of 2D6
    """
    die1 = rollD6()
    die2 = rollD6()
    total = die1 + die2
    
    print(f"\n--- CHARGE ROLL ---")
    print(f"Rolling 2D6: [{die1}, {die2}] = {total}\"")
    
    return total


def canDeclareCharge(distance: int, unitWeapons: list) -> bool:
    """
    Helper function to check if a unit can even attempt to charge
    
    Returns: True if unit has melee weapons and is within 12"
    """
    # Must be within 12"
    if distance > 12:
        return False
    
    # Must have melee weapons
    hasMeleeWeapons = any(
        w.get("range") == "Melee" or (isinstance(w.get("range"), int) and w.get("range") <= 2)
        for w in unitWeapons
    )
    
    return hasMeleeWeapons