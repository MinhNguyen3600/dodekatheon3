"""
abilitySystem.py - Modular Ability Processing Engine

This system processes all unit, weapon, and faction abilities using a declarative template system.
ALL ability-specific logic should be defined in datasheets.py, characterAbilities.py, or weaponAbilityDict.py
using these templates - NO ability-specific code should exist in phase files.
"""

import rolls
from TestPhases.utilityFunctions import parseDiceNotation

# ============================================
# ABILITY SCHEMA DEFINITIONS
# ============================================

"""
ABILITY TEMPLATE STRUCTURE:

{
    "name": str,                    # Ability name
    "trigger": str,                 # When it activates (see VALID_TRIGGERS)
    "condition": str,               # What must be true (see CONDITIONS)
    "effects": list[dict],          # What it does (see EFFECT_TYPES)
    "duration": str,                # How long it lasts (see DURATIONS)
    "uses": int,                    # Optional: limited uses (1 = once per battle)
    "player_choice": bool,          # Optional: requires player input
    "description": str              # Human-readable description
}

VALID TRIGGERS:
- "always"                  : Active at all times
- "start_of_command"        : Command phase start
- "end_of_command"          : Command phase end
- "start_of_movement"       : Movement phase start
- "start_of_shooting"       : Shooting phase start
- "on_attack"               : When making attacks
- "on_defense"              : When being attacked
- "on_hit_roll"             : Modifies hit rolls
- "on_wound_roll"           : Modifies wound rolls
- "on_save_roll"            : Modifies save rolls
- "on_damage"               : When taking damage
- "start_of_fight"          : Fight phase start
- "before_fight"            : Before making fight attacks
- "on_destruction"          : When unit is destroyed
- "on_destruction_melee"    : When destroyed by melee
- "after_shooting"          : After shooting attacks complete
- "after_fighting"          : After fight attacks complete
- "start_of_battle_round"   : Start of battle round (both players)

CONDITIONS:
- "always"                          : No condition
- "isStationary"                    : Unit remained stationary
- "didAdvance"                      : Unit advanced
- "didCharge"                       : Unit charged
- "isOathTarget"                    : Target is oath target
- "attackerWithin"                  : Attacker within a specified distance from unit
- "targetBelowStartingStrength"     : Target is below starting strength
- "targetBelowHalfStrength"         : Target is below half strength
- "unitBelowStartingStrength"       : Unit is below starting strength
- "unitBelowHalfStrength"           : Unit is below half strength
- "hasNotFoughtThisPhase"           : Unit hasn't fought yet
- "notUsedThisBattle"               : Ability not used yet
- "isMeleeAttack"                   : Attack is melee
- "targetHasKeyword:X"              : Target has keyword X
- "distance <= X"                   : Within distance X
- "weaponRange / 2"                 : Within half weapon range
- "hasResourcePattern:X"            : Check if resource pool contains pattern
  - Patterns: "double:N+", "triple:N+", "quad:N+"
  - Examples: "double:5+", "triple:2+", "pair:any"

EFFECT TYPES:
- "modifyHit"           : Modify hit rolls (+/- value)
- "modifyWound"         : Modify wound rolls (+/- value)
- "modifySave"          : Modify save rolls (+/- value)
- "modifyDamage"        : Modify damage (+/- value)
- "modifyAttacks"       : Modify attack count (+/- value)
- "addWeaponAbility"    : Add weapon ability (LETHAL HITS, etc.)
- "rerollHits"          : Re-roll hit rolls (value: "1s", "failed", "all")
- "rerollWounds"        : Re-roll wound rolls (value: "1s", "failed", "all")
- "rerollSaves"         : Re-roll save rolls (value: "1s", "failed", "all")
- "rerollDamage"        : Re-roll damage rolls (value: "1s", "failed", "all")
- "autoHit"             : Attacks automatically hit
- "autoWound"           : Attacks automatically wound
- "mortalWounds"        : Deal mortal wounds (value: dice notation)
- "healWounds"          : Heal wounds (value: dice notation)
- "returnModel"         : Return destroyed model
- "changeInvuln"        : Change invuln save (value: new save)
- "fightBack"           : Fight after being destroyed
- "shootAgain"          : Shoot again immediately
- "chooseStance"        : Select from multiple options
- "rollResourcePool"    : Roll dice and store as resource pool
  - count: number of dice (int)
  - dice_type: "D6" or "D3"
  - store_as: key to store pool (str)
- "selectResourceOptions": Select from options that cost resources
  - resource_pool: which pool to use (str)
  - max_selections: how many can be picked (int)
  - once_per_round: can each be used once per round (bool)
  - options: dict of sub-abilities with costs

DURATIONS:
- "permanent"           : Lasts entire battle
- "this_turn"           : Until end of turn
- "this_phase"          : Until end of phase
- "until_end_of_phase"  : Same as this_phase
- "next_attack"         : Only next attack
- "instant"             : Resolves immediately
- "this_battle_round"   : Until end of battle round (all player turns)

VALUE SPECIFICATIONS:
Numeric values can be specified in several formats:
- Integers: 1, 2, 3, -1, -2 (for modifiers)
- Dice notation: "D3", "D6", "2D6", "D6+1", "D6+3", "2D6+3"
- Fractions: Use "half", "HALF", or numeric 0.5 for halving
- Operations:
  * Addition: value: 3 or value: "+3"
  * Subtraction: value: -2 or value: "-2"
  * Multiplication: value: "*2" (doubles)
  * Division: value: "half" or value: "/2"
  * Set to specific: value: 12 with operation: "set"

    Examples:
    - {"type": "modifyHit", "value": 1}          → +1 to hit
    - {"type": "modifyWound", "value": -1}       → -1 to wound
    - {"type": "modifyDamage", "value": "half"}  → Halve damage
    - {"type": "mortalWounds", "value": "D3"}    → Deal D3 mortal wounds
    - {"type": "modifyAttacks", "value": 3}      → +3 attacks
    - {"type": "modifyAttacks", "value": 12, "operation": "set"} → Set attacks to 12

"""

# ============================================
# ABILITY PROCESSOR
# ============================================

class AbilityProcessor:
    """
    Central processor for all abilities.
    Handles triggering, condition checking, and effect application.
    """
    
    def __init__(self, game_state: dict, logger=None):
        self.game_state = game_state
        self.active_abilities = {}  # Track active temporary abilities
        self.logger = logger  # ADD: Logger reference
        
    def check_trigger(self, ability: dict, trigger_context: str, **kwargs) -> bool:
        """
        Check if an ability should trigger
        
        Args:
            ability: Ability definition dict
            trigger_context: Current trigger (e.g., "start_of_command")
            **kwargs: Additional context (unit, target, distance, etc.)
        
        Returns:
            True if ability should trigger
        """
        if not ability or not ability.get("trigger"):
            return False

        ability_name = ability.get("name", "Unknown Ability")
        unit_name = kwargs.get("unit_name", "Unknown Unit")
        
        
        # Check if trigger matches
        ability_trigger = ability.get("trigger")
        trigger_met = (ability_trigger == trigger_context or ability_trigger == "always")
        
        if not trigger_met:
            return False
        
        # Check uses (if limited)
        uses = ability.get("uses")
        if uses is not None:
            unit_name = kwargs.get("unit_name")
            ability_name = ability.get("name")
            use_key = f"{unit_name}_{ability_name}_used"
            
            if self.game_state.get(use_key, 0) >= uses:
                # ADD: Log limited use exhausted
                if self.logger:
                    self.logger.log_ability_used_limited(
                        ability_name, unit_name,
                        0, uses
                    )
                return False
        
        # Check condition
        condition = ability.get("condition", "always")
        condition_met = self.check_condition(condition, **kwargs)

        #   ADD: Log trigger/condition check
        if self.logger and (trigger_met or condition_met):
            self.logger.log_ability_trigger_check(
                ability_name, unit_name,
                ability_trigger, condition,
                trigger_met, condition_met
            )

        return condition_met
    
    def check_condition(self, condition: str, **kwargs) -> bool:
        """
        Evaluate ability condition
        
        Args:
            condition: Condition string
            **kwargs: Context variables
        
        Returns:
            True if condition is met
        """
        if condition == "always":
            return True
        
        # Simple conditions
        if condition == "isStationary":
            return kwargs.get("is_stationary", False)
        
        if condition == "didAdvance":
            return kwargs.get("did_advance", False)
        
        if condition == "didCharge":
            return kwargs.get("did_charge", False)
        
        if condition == "isOathTarget":
            target_name = kwargs.get("target_name")
            oath_target = self.game_state.get("oath_target")
            return target_name == oath_target
        
        if condition == "targetBelowHalfStrength":
            target_count = kwargs.get("target_model_count", 0)
            target_starting = kwargs.get("target_starting_strength", 1)
            target_wounds = kwargs.get("target_current_wounds", 1)
            target_max = kwargs.get("target_max_wounds", 1)
            
            if target_starting == 1:
                return target_wounds < (target_max / 2)
            else:
                return target_count < (target_starting / 2)
        
        if condition == "targetBelowStartingStrength":
            target_count = kwargs.get("target_model_count", 0)
            target_starting = kwargs.get("target_starting_strength", 1)
            target_wounds = kwargs.get("target_current_wounds", 1)
            target_max = kwargs.get("target_max_wounds", 1)
            
            if target_starting == 1:
                return target_wounds < target_max
            else:
                return target_count < target_starting
        
        if condition == "unitBelowHalfStrength":
            unit_count = kwargs.get("attacker_model_count", 0)
            unit_starting = kwargs.get("attacker_starting_strength", 1)
            unit_wounds = kwargs.get("attacker_current_wounds", 1)
            unit_max = kwargs.get("attacker_max_wounds", 1)
            
            if unit_starting == 1:
                return unit_wounds < (unit_max / 2)
            else:
                return unit_count < (unit_starting / 2)
        
        if condition == "unitBelowStartingStrength":
            unit_count = kwargs.get("attacker_model_count", 0)
            unit_starting = kwargs.get("attacker_starting_strength", 1)
            unit_wounds = kwargs.get("attacker_current_wounds", 1)
            unit_max = kwargs.get("attacker_max_wounds", 1)
            
            if unit_starting == 1:
                return unit_wounds < unit_max
            else:
                return unit_count < unit_starting
        
        if condition == "hasNotFoughtThisPhase":
            unit_name = kwargs.get("unit_name")
            fought_key = f"{unit_name}_has_fought"
            return not self.game_state.get(fought_key, False)
        
        if condition == "notUsedThisBattle":
            unit_name = kwargs.get("unit_name")
            ability_name = kwargs.get("ability_name")
            use_key = f"{unit_name}_{ability_name}_used"
            return not self.game_state.get(use_key, False)
        
        if condition == "isMeleeAttack":
            return kwargs.get("is_melee", False)
        
        # Distance conditions
        if condition.startswith("attackerWithin"):
            import re
            # Handle both "attackerWithin18" (legacy) and "attackerWithin:18" (new format)
            match = re.search(r'attackerWithin:?(\d+)', condition)
            if match:
                threshold = int(match.group(1))
                distance = kwargs.get("distance", 999)
                return distance <= threshold
        
        if condition.startswith("distance"):
            # Handle "distance <= X" or "distance > X"
            import re
            match = re.search(r'distance\s*([<>=]+)\s*(\d+)', condition)
            if match:
                operator = match.group(1)
                threshold = int(match.group(2))
                distance = kwargs.get("distance", 999)
                
                if operator == "<=":
                    return distance <= threshold
                elif operator == "<":
                    return distance < threshold
                elif operator == ">=":
                    return distance >= threshold
                elif operator == ">":
                    return distance > threshold
                elif operator == "==":
                    return distance == threshold
        
        # Keyword conditions
        if condition.startswith("targetHasKeyword"):
            keyword = condition.split(":")[1] if ":" in condition else None
            if keyword:
                target_keywords = kwargs.get("target_keywords", [])
                return keyword.upper() in [k.upper() for k in target_keywords]
        
        # ✅ FIX: Add hasResourcePattern condition
        if condition.startswith("hasResourcePattern"):
            pattern = condition.split(":")[1] if ":" in condition else None
            if pattern:
                pool_key = kwargs.get("resource_pool", "resource_pool")
                dice_pool = self.game_state.get(pool_key, [])
                result = self.check_dice_pattern(dice_pool, pattern)
                return result["matches"]
        
        # Weapon range conditions
        if "weaponRange" in condition:
            weapon_range = kwargs.get("weapon_range", 0)
            distance = kwargs.get("distance", 999)
            
            if "weaponRange / 2" in condition or "weaponRange/2" in condition:
                return distance <= (weapon_range / 2)
        
        # Default: unknown condition fails
        return False
    
    def roll_resource_pool(self, count: int, dice_type: str) -> list:
        """
        Roll multiple dice and return results
        
        Args:
            count: Number of dice to roll
            dice_type: "D6" or "D3"
        
        Returns:
            List of dice results
        """
        results = []
        for _ in range(count):
            if dice_type == "D6":
                results.append(rolls.rollD6())
            elif dice_type == "D3":
                results.append(rolls.rollD3())
        
        return sorted(results)  # Sort for easier pattern matching

    def check_dice_pattern(self, dice_pool: list, pattern: str) -> dict:
        """
        Check if dice pool contains required pattern
        
        Args:
            dice_pool: List of dice results
            pattern: Pattern string (e.g., "double:5+", "triple:3+")
        
        Returns:
            Dict with {"matches": bool, "matching_dice": list}
        """
        from collections import Counter
        
        # Parse pattern: "double:5+" or "triple:2+" or "quad:4+"
        parts = pattern.split(":")
        pattern_type = parts[0]  # "double", "triple", "quad"
        value_requirement = parts[1] if len(parts) > 1 else "any"  # "5+", "2+", "any"
        
        # Count occurrences
        counts = Counter(dice_pool)
        
        # Determine required count
        required_count = {
            "double": 2,
            "pair": 2,
            "triple": 3,
            "quad": 4
        }.get(pattern_type, 2)
        
        # Check for matches
        for value, count in counts.items():
            if count >= required_count:
                # Check value requirement
                if value_requirement == "any":
                    return {"matches": True, "matching_dice": [value] * required_count}
                elif "+" in value_requirement:
                    min_value = int(value_requirement.replace("+", ""))
                    if value >= min_value:
                        return {"matches": True, "matching_dice": [value] * required_count}
        
        return {"matches": False, "matching_dice": []}

    def prompt_resource_selection(self, dice_pool: list, options: dict, 
                                max_selections: int, unit_name: str) -> list:
        """
        Let player select which resource-based options to activate
        
        Args:
            dice_pool: Available dice
            options: Dict of available options with costs
            max_selections: Maximum number to select
            unit_name: Name of unit activating
        
        Returns:
            List of selected option keys and consumed dice
        """
        print(f"\n{'='*60}")
        print(f"🎲 {unit_name.upper()} - RESOURCE SELECTION")
        print(f"{'='*60}")
        print(f"Dice Pool: {dice_pool}")
        print(f"You can activate up to {max_selections} options:")
        print(f"{'='*60}")
        
        # Display available options
        available_options = []
        for i, (key, option) in enumerate(options.items(), 1):
            requires = option.get("requires", {})
            pattern = requires.get("type", "unknown")
            value = requires.get("value", "any")
            
            print(f"{i}. {option.get('name', key)}")
            print(f"   Requires: {pattern.upper()} of {value}+")
            
            # ✅ FIX: Check for alt_requires (OR condition)
            alt_requires = option.get("alt_requires")
            if alt_requires:
                alt_pattern = alt_requires.get("type", "unknown")
                alt_value = alt_requires.get("value", "any")
                print(f"   OR: {alt_pattern.upper()} of {alt_value}+")
            
            print(f"   {option.get('description', '')}")
            
            # Check if can be activated (primary requirement)
            pattern_str = f"{pattern}:{value}+"
            result = self.check_dice_pattern(dice_pool, pattern_str)
            
            # ✅ FIX: Check alt_requires if primary fails
            if not result["matches"] and alt_requires:
                alt_pattern_str = f"{alt_requires.get('type')}:{alt_requires.get('value')}+"
                result = self.check_dice_pattern(dice_pool, alt_pattern_str)
            
            if result["matches"]:
                available_options.append((key, option, result["matching_dice"]))
                print(f"   ✓ CAN ACTIVATE")
            else:
                print(f"   ✗ Cannot activate")
            print()
        
        if not available_options:
            print("No options can be activated with current dice!")
            return []
        
        print(f"{'='*60}")
        
        # Let player select
        selections = []
        remaining_dice = dice_pool.copy()
        
        for selection_num in range(max_selections):
            if not available_options:
                break
            
            print(f"\nRemaining dice: {remaining_dice}")
            print(f"Selection {selection_num + 1}/{max_selections}")
            print("Enter option number (or 0 to finish):")
            
            while True:
                try:
                    choice = int(input("> "))
                    if choice == 0:
                        return selections
                    if 1 <= choice <= len(available_options):
                        break
                except ValueError:
                    pass
                print(f"Please enter 0-{len(available_options)}")
            
            # Get selected option
            selected_key, selected_option, matching_dice = available_options[choice - 1]
            
            # Remove used dice
            for die in matching_dice:
                if die in remaining_dice:
                    remaining_dice.remove(die)
            
            selections.append({
                "key": selected_key,
                "option": selected_option,
                "dice_used": matching_dice
            })
            
            print(f"✓ Activated: {selected_option.get('name')}")
            print(f"   Used dice: {matching_dice}")
            
            # Recalculate available options with remaining dice
            available_options = []
            for key, option in options.items():
                if any(s["key"] == key for s in selections):
                    continue  # Already selected
                
                requires = option.get("requires", {})
                pattern = requires.get("type", "unknown")
                value = requires.get("value", "any")
                pattern_str = f"{pattern}:{value}+"
                
                result = self.check_dice_pattern(remaining_dice, pattern_str)
                
                # ✅ FIX: Check alt_requires
                if not result["matches"]:
                    alt_requires = option.get("alt_requires")
                    if alt_requires:
                        alt_pattern_str = f"{alt_requires.get('type')}:{alt_requires.get('value')}+"
                        result = self.check_dice_pattern(remaining_dice, alt_pattern_str)
                
                if result["matches"]:
                    available_options.append((key, option, result["matching_dice"]))
        
        return selections
    
    def apply_effects(self, ability: dict, **kwargs) -> dict:
        """
        Apply ability effects
        
        Args:
            ability: Ability definition dict
            **kwargs: Context for effect application
        
        Returns:
            Dict with applied effects (modifiers, changes, etc.)
        """
        effects = ability.get("effects", [])
        results = {
            "hit_modifier": 0,
            "wound_modifier": 0,
            "save_modifier": 0,
            "damage_modifier": 0,
            "attacks_modifier": 0,
            "added_abilities": [],
            "rerolls": {},
            "special_effects": [],
            "mortal_damage": 0
        }
        
        for effect in effects:
            effect_type = effect.get("type")
            
            if effect_type == "modifyHit":
                results["hit_modifier"] += effect.get("value", 0)
            
            elif effect_type == "modifyWound":
                results["wound_modifier"] += effect.get("value", 0)
            
            elif effect_type == "modifySave":
                results["save_modifier"] += effect.get("value", 0)
            
            elif effect_type == "modifyDamage":
                results["damage_modifier"] += effect.get("value", 0)
            
            elif effect_type == "modifyAttacks":
                results["attacks_modifier"] += effect.get("value", 0)
            
            elif effect_type == "addWeaponAbility":
                ability_to_add = effect.get("ability")
                if ability_to_add:
                    results["added_abilities"].append(ability_to_add)
            
            elif effect_type in ["rerollHits", "rerollWounds", "rerollSaves", "rerollDamage"]:
                reroll_type = effect_type.replace("reroll", "").lower()
                results["rerolls"][reroll_type] = effect.get("value", "1s")
            
            elif effect_type == "autoHit":
                results["special_effects"].append("AUTO_HIT")
            
            elif effect_type == "autoWound":
                results["special_effects"].append("AUTO_WOUND")
            
            elif effect_type == "mortalWounds":
                damage = parseDiceNotation(effect.get("value", "0"))
                results["mortal_damage"] += damage
            
            elif effect_type == "healWounds":
                heal_value = effect.get("value", "D3")
                healing = parseDiceNotation(heal_value)
                results["special_effects"].append(("HEAL", healing))
            
            elif effect_type == "returnModel":
                results["special_effects"].append(("RETURN_MODEL", effect.get("wounds", 1)))
            
            elif effect_type == "changeInvuln":
                results["special_effects"].append(("CHANGE_INVULN", effect.get("value", 4)))
            
            elif effect_type == "fightBack":
                results["special_effects"].append("FIGHT_BACK")
            
            elif effect_type == "shootAgain":
                results["special_effects"].append("SHOOT_AGAIN")
            
            elif effect_type == "chooseStance":
                results["special_effects"].append(("CHOOSE_STANCE", effect))

            elif effect_type == "rollResourcePool":
                count = effect.get("count", 1)
                dice_type = effect.get("dice_type", "D6")
                store_as = effect.get("store_as", "resource_pool")
                
                pool = self.roll_resource_pool(count, dice_type)
                self.game_state[store_as] = pool
                
                print(f"\n🎲 Rolled {count}{dice_type}: {pool}")
                results["special_effects"].append(("RESOURCE_POOL", store_as, pool))

            elif effect_type == "selectResourceOptions":
                pool_key = effect.get("resource_pool", "resource_pool")
                dice_pool = self.game_state.get(pool_key, [])
                options = effect.get("options", {})
                max_selections = effect.get("max_selections", 1)
                unit_name = kwargs.get("unit_name", "Unit")
                
                selections = self.prompt_resource_selection(
                    dice_pool, options, max_selections, unit_name
                )
                
                # ✅ FIX: Apply selected effects properly
                for selection in selections:
                    option = selection["option"]
                    option_effects = option.get("effects", [])
                    
                    # Process each option effect
                    for opt_effect in option_effects:
                        opt_type = opt_effect.get("type")
                        
                        # Handle all effect types
                        if opt_type == "addWeaponAbility":
                            ability_to_add = opt_effect.get("ability")
                            if ability_to_add and ability_to_add not in results["added_abilities"]:
                                results["added_abilities"].append(ability_to_add)
                        
                        elif opt_type == "modifyHit":
                            results["hit_modifier"] += opt_effect.get("value", 0)
                        
                        elif opt_type == "modifyWound":
                            results["wound_modifier"] += opt_effect.get("value", 0)
                        
                        elif opt_type == "modifyAttacks":
                            results["attacks_modifier"] += opt_effect.get("value", 0)
                        
                        elif opt_type == "modifyDamage":
                            results["damage_modifier"] += opt_effect.get("value", 0)
                        
                        elif opt_type in ["rerollHits", "rerollWounds", "rerollCharges"]:
                            reroll_type = opt_type.replace("reroll", "").lower()
                            results["rerolls"][reroll_type] = opt_effect.get("value", "all")
                        
                        elif opt_type == "modifyMovement":
                            # Store special movement modifications
                            results["special_effects"].append(("MODIFY_MOVEMENT", opt_effect))
                        
                        # Add more as needed...
                
                results["special_effects"].append(("RESOURCE_SELECTIONS", selections))
        
        if self.logger:
            ability_name = ability.get("name", "Unknown Ability")
            unit_name = kwargs.get("unit_name", "Unknown Unit")
            self.logger.log_ability_effects(ability_name, unit_name, results)

        return results
    
    def mark_ability_used(self, ability: dict, unit_name: str):
        """Mark an ability as used (for limited-use abilities)"""
        ability_name = ability.get("name")
        use_key = f"{unit_name}_{ability_name}_used"
        
        current_uses = self.game_state.get(use_key, 0)
        self.game_state[use_key] = current_uses + 1
    
    def prompt_player_activation(self, ability: dict, unit_name: str) -> bool:
        """
        Prompt player to activate an ability that requires choice
        
        Returns:
            True if player chooses to activate
        """
        if not ability.get("player_choice", False):
            return True  # Auto-activate if no choice needed
        
        ability_name = ability.get("name", "Unknown Ability")
        description = ability.get("description", "")
        
        print(f"\n{'='*60}")
        print(f"⚡ {unit_name.upper()} - {ability_name.upper()}")
        print(f"{'='*60}")
        
        if description:
            print(f"{description}")
        
        uses = ability.get("uses")
        if uses:
            print(f"\n⚠️ This ability can only be used {uses} time(s) per battle!")
        
        print(f"{'='*60}")
        
        response = input(f"Activate {ability_name}? (y/n): ").lower()
        activated = (response == 'y')

        # ADD: Log activation decision
        if self.logger:
            self.logger.log_ability_activation(
                ability_name, unit_name,
                ability.get("trigger", "unknown"),
                player_choice=True,
                activated=activated
            )

        return activated


# ============================================
# ABILITY APPLICATION HELPERS
# ============================================

def apply_weapon_abilities_to_attack(weapon: dict, ability_processor: AbilityProcessor,
                                     **context) -> dict:
    """
    Apply all weapon abilities to an attack
    
    Returns:
        Dict with all modifiers and effects
    """
    # Get weapon abilities
    weapon_abilities = weapon.get("weapon abilities", [])
    
    # Process each ability through the system
    combined_effects = {
        "hit_modifier": 0,
        "wound_modifier": 0,
        "save_modifier": 0,
        "damage_modifier": 0,
        "attacks_modifier": 0,
        "added_abilities": list(weapon_abilities),  # Start with base abilities
        "rerolls": {},
        "special_effects": []
    }
    
    return combined_effects


def apply_unit_ability_effects(unit: dict, ability_processor: AbilityProcessor,
                               trigger: str, **context) -> dict:
    """
    Apply unit ability effects at a specific trigger
    
    Returns:
        Dict with all modifiers and effects
    """
    unit_ability = unit.get("Ability", {})
    
    if not unit_ability:
        return {}
    
    # Check if ability triggers
    if ability_processor.check_trigger(unit_ability, trigger, **context):
        return ability_processor.apply_effects(unit_ability, **context)
    
    return {}


def apply_faction_ability_effects(unit: dict, ability_processor: AbilityProcessor,
                                  trigger: str, **context) -> dict:
    """
    Apply faction ability effects at a specific trigger
    
    Returns:
        Dict with all modifiers and effects
    """
    from TestPhases.datasheets import FACTION_ABILITIES
    
    faction_name = unit.get("Faction Ability", "")
    
    if not faction_name or faction_name not in FACTION_ABILITIES:
        return {}
    
    faction_ability = FACTION_ABILITIES[faction_name]
    
    # Check if ability triggers
    if ability_processor.check_trigger(faction_ability, trigger, **context):
        return ability_processor.apply_effects(faction_ability, **context)
    
    return {}


# ============================================
# PHASE-SPECIFIC HELPERS
# ============================================

def process_command_phase_abilities(attacker_unit: dict, defender_unit: dict,
                                    game_state: dict):
    """
    Process all abilities that trigger in command phase
    Returns: Updated game_state
    """
    processor = AbilityProcessor(game_state)
    
    # Start of command phase
    context = {
        "unit_name": attacker_unit["Name"],
        "target_name": defender_unit["Name"]
    }
    
    # Process attacker abilities
    attacker_effects = apply_unit_ability_effects(
        attacker_unit, processor, "start_of_command", **context
    )
    
    # Process faction abilities
    faction_effects = apply_faction_ability_effects(
        attacker_unit, processor, "start_of_command", **context
    )
    
    # Apply effects to game state
    for effect_type, effect_list in attacker_effects.get("special_effects", []):
        if effect_type == "OATH_TARGET":
            game_state["oath_target"] = defender_unit["Name"]
    
    # End of command phase
    defender_effects = apply_unit_ability_effects(
        defender_unit, processor, "end_of_command",
        unit_name=defender_unit["Name"]
    )
    
    return game_state


def get_hit_modifiers(attacker_unit: dict, target_unit: dict, weapon: dict,
                     game_state: dict, **context) -> int:
    """
    Get all hit roll modifiers from abilities
    
    Returns:
        Total hit modifier
    """
    processor = AbilityProcessor(game_state)
    
    total_modifier = 0
    
    # Unit ability
    unit_effects = apply_unit_ability_effects(
        attacker_unit, processor, "on_hit_roll",
        **context
    )
    total_modifier += unit_effects.get("hit_modifier", 0)
    
    # Target defensive ability
    target_effects = apply_unit_ability_effects(
        target_unit, processor, "on_defense",
        **context
    )
    total_modifier += target_effects.get("hit_modifier", 0)
    
    return total_modifier


def get_wound_modifiers(attacker_unit: dict, weapon: dict, game_state: dict,
                       **context) -> int:
    """
    Get all wound roll modifiers from abilities
    
    Returns:
        Total wound modifier
    """
    processor = AbilityProcessor(game_state)
    
    unit_effects = apply_unit_ability_effects(
        attacker_unit, processor, "on_wound_roll",
        **context
    )
    
    return unit_effects.get("wound_modifier", 0)


# ============================================
# LOGGING HELPERS
# ============================================

def log_ability_activation(ability: dict, unit_name: str, context: str = ""):
    """Log when an ability activates"""
    print(f"\n⚡ [{ability['name'].upper()}] activated - {unit_name}")
    if context:
        print(f"   Context: {context}")