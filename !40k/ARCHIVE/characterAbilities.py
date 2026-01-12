"""
characterAbilities.py - Complete Character Ability System
Create this as a NEW FILE in project root
"""

import rolls
from TestPhases.utilityFunctions import parseDiceNotation

# ==================== FINEST HOUR ====================

def canActivateFinestHour(unit: dict, game_state: dict) -> bool:
    """
    Check if Finest Hour can be activated
    
    Returns: True if ability available
    """
    ability = unit.get("Ability", {})
    
    if ability.get("name") != "Finest Hour":
        return False
    
    # Check if already used this battle
    unitName = unit["Name"]
    finestHourKey = f"{unitName}_finest_hour_used"
    
    if game_state.get(finestHourKey, False):
        return False
    
    return True


def activateFinestHour(unit: dict, game_state: dict) -> dict:
    """
    Activate Finest Hour ability
    
    Effects:
    - +3 Attacks on melee weapons
    - Melee weapons gain DEVASTATING WOUNDS
    - Lasts until end of Fight phase
    
    Returns: Modified game_state
    """
    unitName = unit["Name"]
    
    print(f"\n{'='*60}")
    print(f"⚡ FINEST HOUR - {unitName}")
    print(f"{'='*60}")
    print(f"Once per battle ability activated!")
    print(f"Effects:")
    print(f"  • +3 Attacks on all melee weapons")
    print(f"  • Melee weapons gain [DEVASTATING WOUNDS]")
    print(f"  • Lasts until end of Fight phase")
    print(f"{'='*60}\n")
    
    # Mark as used
    finestHourKey = f"{unitName}_finest_hour_used"
    game_state[finestHourKey] = True
    
    # Mark as active this phase
    finestHourActiveKey = f"{unitName}_finest_hour_active"
    game_state[finestHourActiveKey] = True
    
    return game_state


def applyFinestHourBonus(weapon: dict, unit: dict, game_state: dict) -> dict:
    """
    Apply Finest Hour bonuses to a melee weapon
    
    Returns: Modified weapon dict
    """
    unitName = unit["Name"]
    finestHourActiveKey = f"{unitName}_finest_hour_active"
    
    if not game_state.get(finestHourActiveKey, False):
        return weapon
    
    # Check if weapon is melee
    if weapon.get("range") != "Melee":
        return weapon
    
    # Create modified copy
    modifiedWeapon = weapon.copy()
    
    # +3 Attacks (handle both int and dice notation)
    attacksValue = weapon.get("a")
    if isinstance(attacksValue, int):
        modifiedWeapon["a"] = attacksValue + 3
    else:
        # If it's dice notation, parse it
        baseAttacks = parseDiceNotation(str(attacksValue))
        modifiedWeapon["a"] = baseAttacks + 3
    
    print(f"  [FINEST HOUR] {weapon['name']}: Attacks {weapon['a']} → {modifiedWeapon['a']}")
    
    # Add DEVASTATING WOUNDS
    weaponAbilities = list(modifiedWeapon.get("weapon abilities", []))
    if "DEVASTATING WOUNDS" not in weaponAbilities:
        weaponAbilities.append("DEVASTATING WOUNDS")
        modifiedWeapon["weapon abilities"] = weaponAbilities
        print(f"  [FINEST HOUR] {weapon['name']}: Gained [DEVASTATING WOUNDS]")
    
    return modifiedWeapon


def deactivateFinestHour(unit: dict, game_state: dict) -> dict:
    """
    Deactivate Finest Hour at end of Fight phase
    
    Returns: Modified game_state
    """
    unitName = unit["Name"]
    finestHourActiveKey = f"{unitName}_finest_hour_active"
    
    if game_state.get(finestHourActiveKey, False):
        print(f"\n⚡ [FINEST HOUR] Effect ends for {unitName}")
        game_state[finestHourActiveKey] = False
    
    return game_state


# ==================== HONOR OF ULTRAMAR ====================

def canTriggerHonorOfUltramar(unit: dict, destroyed_by_melee: bool, 
                               has_fought_this_phase: bool) -> bool:
    """
    Check if Honor of Ultramar can trigger
    
    Conditions:
    - Destroyed by melee attack
    - Has not fought this phase
    
    Returns: True if ability can trigger
    """
    ability = unit.get("Ability", {})
    
    if ability.get("name") != "Honor of Ultramar":
        return False
    
    if not destroyed_by_melee:
        return False
    
    if has_fought_this_phase:
        return False
    
    return True


def activateHonorOfUltramar(unit: dict, game_state: dict) -> tuple:
    """
    Activate Honor of Ultramar ability
    
    Process:
    1. Roll D6, on 2+ unit survives temporarily
    2. Unit fights back
    3. If killed enemy models → regain D3 wounds, survive
    4. Otherwise → removed from play
    
    Returns: (survives_temporarily, regained_wounds)
    """
    unitName = unit["Name"]
    
    print(f"\n{'='*60}")
    print(f"⚔️ HONOR OF ULTRAMAR - {unitName}")
    print(f"{'='*60}")
    print(f"{unitName} was destroyed by a melee attack!")
    print(f"Has not fought this phase...")
    print(f"\nRolling survival check...")
    
    survivalRoll = rolls.rollBox(1)[0]
    print(f"Survival roll: {survivalRoll}")
    
    if survivalRoll >= 2:
        print(f"\n✓ SUCCESS! {unitName} survives temporarily!")
        print(f"  • {unitName} will fight after the attacking unit")
        print(f"  • Must kill enemy models to survive permanently")
        print(f"{'='*60}\n")
        return (True, 0)
    else:
        print(f"\n✗ FAILED! {unitName} is removed from play")
        print(f"{'='*60}\n")
        return (False, 0)


def resolveHonorOfUltramar(unit: dict, models_killed: int, game_state: dict) -> tuple:
    """
    Resolve Honor of Ultramar after fighting back
    
    Args:
        unit: Titus unit dict
        models_killed: Number of enemy models killed
        game_state: Current game state
    
    Returns: (survives_permanently, wounds_regained)
    """
    unitName = unit["Name"]
    
    print(f"\n{'='*60}")
    print(f"⚔️ HONOR OF ULTRAMAR - Resolution")
    print(f"{'='*60}")
    print(f"Enemy models killed: {models_killed}")
    
    if models_killed > 0:
        # Regain D3 wounds
        woundsRegained = parseDiceNotation("D3")
        print(f"\n✓ {unitName} killed enemy models!")
        print(f"  • Rolling D3 to regain wounds: {woundsRegained}")
        print(f"  • {unitName} is NOT DESTROYED!")
        print(f"{'='*60}\n")
        return (True, woundsRegained)
    else:
        print(f"\n✗ {unitName} did not kill any enemy models")
        print(f"  • {unitName} is removed from play")
        print(f"{'='*60}\n")
        return (False, 0)

# ==================== MOMENT SHACKLE (TRAJANN) ====================

def canActivateMomentShackle(unit: dict, game_state: dict) -> bool:
    """Check if Moment Shackle can be activated"""
    ability = unit.get("Ability", {})
    
    if ability.get("name") != "Moment Shackle":
        return False
    
    unitName = unit["Name"]
    momentShackleKey = f"{unitName}_moment_shackle_used"
    
    if game_state.get(momentShackleKey, False):
        return False
    
    return True


def activateMomentShackle(unit: dict, game_state: dict) -> dict:
    """
    Activate Moment Shackle - player chooses one option
    
    Returns: Modified game_state with choice recorded
    """
    unitName = unit["Name"]
    
    print(f"\n{'='*60}")
    print(f"⚡ MOMENT SHACKLE - {unitName}")
    print(f"{'='*60}")
    print(f"Once per battle ability - Choose one option:")
    print(f"  1. Attacks Overdrive: Watcher's Axe has 12 Attacks")
    print(f"  2. Invulnerable Aegis: Model gains 2+ invulnerable save")
    print(f"{'='*60}")
    
    while True:
        choice = input("Select option (1 or 2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    # Mark as used
    momentShackleKey = f"{unitName}_moment_shackle_used"
    game_state[momentShackleKey] = True
    
    # Mark which option is active
    momentShackleActiveKey = f"{unitName}_moment_shackle_active"
    momentShackleChoiceKey = f"{unitName}_moment_shackle_choice"
    
    game_state[momentShackleActiveKey] = True
    game_state[momentShackleChoiceKey] = "attacks" if choice == "1" else "invuln"
    
    if choice == "1":
        print(f"\n⚔️ ATTACKS OVERDRIVE ACTIVATED!")
        print(f"   Watcher's Axe: 6 → 12 Attacks")
    else:
        print(f"\n🛡️ INVULNERABLE AEGIS ACTIVATED!")
        print(f"   Invulnerable Save: 4+ → 2+")
    
    print(f"   Duration: Until end of Fight phase")
    print(f"{'='*60}\n")
    
    return game_state


def applyMomentShackleWeaponBonus(weapon: dict, unit: dict, game_state: dict) -> dict:
    """Apply Moment Shackle weapon bonus if active and attacks option chosen"""
    unitName = unit["Name"]
    momentShackleActiveKey = f"{unitName}_moment_shackle_active"
    momentShackleChoiceKey = f"{unitName}_moment_shackle_choice"
    
    if not game_state.get(momentShackleActiveKey, False):
        return weapon
    
    if game_state.get(momentShackleChoiceKey) != "attacks":
        return weapon
    
    # Only apply to Watcher's Axe
    if weapon.get("name") != "Watcher's Axe":
        return weapon
    
    modifiedWeapon = weapon.copy()
    modifiedWeapon["a"] = 12
    
    print(f"  [MOMENT SHACKLE] Watcher's Axe: Attacks 6 → 12")
    
    return modifiedWeapon


def getMomentShackleInvulnBonus(unit: dict, game_state: dict) -> int:
    """Get Moment Shackle invuln save bonus if active"""
    unitName = unit["Name"]
    momentShackleActiveKey = f"{unitName}_moment_shackle_active"
    momentShackleChoiceKey = f"{unitName}_moment_shackle_choice"
    
    if not game_state.get(momentShackleActiveKey, False):
        return 0  # No bonus
    
    if game_state.get(momentShackleChoiceKey) != "invuln":
        return 0
    
    # Return 2+ invuln
    return 2


def deactivateMomentShackle(unit: dict, game_state: dict) -> dict:
    """Deactivate Moment Shackle at end of Fight phase"""
    unitName = unit["Name"]
    momentShackleActiveKey = f"{unitName}_moment_shackle_active"
    
    if game_state.get(momentShackleActiveKey, False):
        print(f"\n⚡ [MOMENT SHACKLE] Effect ends for {unitName}")
        game_state[momentShackleActiveKey] = False
    
    return game_state


# ==================== MARTIAL KA'TAH ====================

def canSelectKatahStance(unit: dict) -> bool:
    """Check if unit has Martial Ka'tah faction ability"""
    factionAbility = unit.get("Faction Ability", "")
    return factionAbility == "Martial Ka'tah"


def selectKatahStance(unit: dict, game_state: dict) -> dict:
    """
    Prompt player to select Ka'tah Stance
    Returns: Modified game_state with stance recorded
    """
    unitName = unit["Name"]
    
    print(f"\n{'='*60}")
    print(f"⚔️ MARTIAL KA'TAH - {unitName}")
    print(f"{'='*60}")
    print(f"Select Ka'tah Stance:")
    print(f"  1. Dacatarai Stance: Melee weapons gain [SUSTAINED HITS 1]")
    print(f"  2. Rendax Stance: Melee weapons gain [LETHAL HITS]")
    print(f"{'='*60}")
    
    while True:
        choice = input("Select stance (1 or 2): ").strip()
        if choice in ["1", "2"]:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    katahKey = f"{unitName}_katah_stance"
    game_state[katahKey] = "dacatarai" if choice == "1" else "rendax"
    
    if choice == "1":
        print(f"\n⚡ DACATARAI STANCE SELECTED!")
        print(f"   Effect: Melee weapons gain [SUSTAINED HITS 1]")
    else:
        print(f"\n⚡ RENDAX STANCE SELECTED!")
        print(f"   Effect: Melee weapons gain [LETHAL HITS]")
    
    print(f"{'='*60}\n")
    
    return game_state


def applyKatahStance(weapon: dict, unit: dict, game_state: dict) -> dict:
    """Apply active Ka'tah Stance to melee weapon"""
    unitName = unit["Name"]
    katahKey = f"{unitName}_katah_stance"
    
    stance = game_state.get(katahKey)
    
    if not stance:
        return weapon
    
    # Only apply to melee weapons
    if weapon.get("range") != "Melee":
        return weapon
    
    modifiedWeapon = weapon.copy()
    weaponAbilities = list(modifiedWeapon.get("weapon abilities", []))
    
    if stance == "dacatarai":
        if "SUSTAINED HITS 1" not in weaponAbilities:
            weaponAbilities.append("SUSTAINED HITS 1")
            print(f"  [DACATARAI STANCE] {weapon['name']}: Gained [SUSTAINED HITS 1]")
    elif stance == "rendax":
        if "LETHAL HITS" not in weaponAbilities:
            weaponAbilities.append("LETHAL HITS")
            print(f"  [RENDAX STANCE] {weapon['name']}: Gained [LETHAL HITS]")
    
    modifiedWeapon["weapon abilities"] = weaponAbilities
    
    return modifiedWeapon


def clearKatahStance(unit: dict, game_state: dict) -> dict:
    """Clear Ka'tah Stance after unit finishes fighting"""
    unitName = unit["Name"]
    katahKey = f"{unitName}_katah_stance"
    
    if katahKey in game_state:
        del game_state[katahKey]
    
    return game_state


# ==================== HELPER FUNCTIONS ====================

def checkFinestHourActivation(unit: dict, game_state: dict) -> dict:
    """
    Prompt player to activate Finest Hour if available
    Call this at START OF FIGHT PHASE
    """
    if canActivateFinestHour(unit, game_state):
        unitName = unit["Name"]
        activate = input(f"\n{unitName} can use FINEST HOUR! Activate? (y/n): ").lower()
        
        if activate == 'y':
            game_state = activateFinestHour(unit, game_state)
    
    return game_state



