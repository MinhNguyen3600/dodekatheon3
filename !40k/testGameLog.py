"""
testGameLog.py - Comprehensive Game Logging System with Ability Tracking
Generates detailed markdown logs of 40K battles with ability system integration
"""

import datetime
import os


class GameLogger:
    """
    Comprehensive game logger that tracks all combat actions, game state, and ability activations
    """
    
    def __init__(self, unit1_name: str, unit2_name: str):
        self.unit1_name = unit1_name
        self.unit2_name = unit2_name
        self.log_entries = []
        self.current_turn = 0
        self.game_start_time = None
        self.ability_log_buffer = []  # Buffer for ability events within a phase
        
    def start_game(self, game_state: dict):
        """Log game start"""
        self.game_start_time = datetime.datetime.now()
        
        self.log_entries.append("="*80)
        self.log_entries.append("WARHAMMER 40,000 BATTLE SIMULATOR - GAME LOG")
        self.log_entries.append("="*80)
        self.log_entries.append(f"Date: {self.game_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_entries.append(f"")
        self.log_entries.append(f"Unit 1: {self.unit1_name}")
        self.log_entries.append(f"Unit 2: {self.unit2_name}")
        self.log_entries.append("")
        
    def start_turn(self, turn_number: int, game_state: dict):
        """Log turn start"""
        self.current_turn = turn_number
        
        attacker = game_state["attacker_unit"]
        defender = game_state["defender_unit"]
        
        a_count = game_state["attacker_count"]
        a_wounds = game_state["attacker_current_wounds"]
        d_count = game_state["defender_count"]
        d_wounds = game_state["defender_current_wounds"]
        
        self.log_entries.append("")
        self.log_entries.append("="*80)
        self.log_entries.append(f"TURN {turn_number}")
        self.log_entries.append("="*80)
        self.log_entries.append(f"Turn Start: {attacker['Name']} ({a_count} models, {a_wounds}W) vs {defender['Name']} ({d_count} models, {d_wounds}W)")
        
        distance = abs(game_state.get("attacker_position", 0) - game_state.get("defender_position", 0))
        self.log_entries.append(f"Distance: {distance}\"")
        
    # ============================================
    # ABILITY LOGGING METHODS
    # ============================================
    
    def log_ability_trigger_check(self, ability_name: str, unit_name: str, 
                                   trigger: str, condition: str, 
                                   trigger_met: bool, condition_met: bool):
        """Log ability trigger and condition evaluation"""
        if trigger_met and condition_met:
            self.ability_log_buffer.append(f"  ⚡ [{ability_name}] - Checking activation for {unit_name}")
            self.ability_log_buffer.append(f"     Trigger: {trigger} ✓")
            self.ability_log_buffer.append(f"     Condition: {condition} ✓")
        elif trigger_met and not condition_met:
            self.ability_log_buffer.append(f"  ⚠️  [{ability_name}] - Trigger met but condition failed for {unit_name}")
            self.ability_log_buffer.append(f"     Trigger: {trigger} ✓")
            self.ability_log_buffer.append(f"     Condition: {condition} ✗")
    
    def log_ability_activation(self, ability_name: str, unit_name: str, 
                               trigger: str, player_choice: bool = False, 
                               activated: bool = True):
        """Log when an ability activates"""
        if player_choice:
            if activated:
                self.ability_log_buffer.append(f"  ✅ [{ability_name}] - ACTIVATED by player choice ({unit_name})")
            else:
                self.ability_log_buffer.append(f"  ❌ [{ability_name}] - DECLINED by player ({unit_name})")
        else:
            self.ability_log_buffer.append(f"  ⚡ [{ability_name}] - AUTO-ACTIVATED ({unit_name})")
    
    def log_ability_effects(self, ability_name: str, unit_name: str, effects: dict):
        """Log the effects an ability applies"""
        if not effects:
            return
        
        self.ability_log_buffer.append(f"  📊 [{ability_name}] - Effects Applied:")
        
        # Modifiers
        if effects.get("hit_modifier", 0) != 0:
            mod = effects["hit_modifier"]
            self.ability_log_buffer.append(f"     • Hit Roll: {mod:+d}")
        
        if effects.get("wound_modifier", 0) != 0:
            mod = effects["wound_modifier"]
            self.ability_log_buffer.append(f"     • Wound Roll: {mod:+d}")
        
        if effects.get("save_modifier", 0) != 0:
            mod = effects["save_modifier"]
            self.ability_log_buffer.append(f"     • Save Roll: {mod:+d}")
        
        if effects.get("damage_modifier", 0) != 0:
            mod = effects["damage_modifier"]
            self.ability_log_buffer.append(f"     • Damage: {mod:+d}")
        
        if effects.get("attacks_modifier", 0) != 0:
            mod = effects["attacks_modifier"]
            self.ability_log_buffer.append(f"     • Attacks: {mod:+d}")
        
        # Added abilities
        if effects.get("added_abilities"):
            for ability in effects["added_abilities"]:
                self.ability_log_buffer.append(f"     • Weapon Gained: [{ability}]")
        
        # Rerolls
        rerolls = effects.get("rerolls", {})
        if rerolls:
            for reroll_type, value in rerolls.items():
                self.ability_log_buffer.append(f"     • Re-roll {reroll_type}: {value}")
        
        # Special effects
        special = effects.get("special_effects", [])
        if special:
            for effect in special:
                if isinstance(effect, tuple):
                    effect_type, effect_value = effect[0], effect[1] if len(effect) > 1 else None
                    if effect_type == "HEAL":
                        self.ability_log_buffer.append(f"     • Heal: {effect_value} wounds")
                    elif effect_type == "RETURN_MODEL":
                        self.ability_log_buffer.append(f"     • Return Model: {effect_value} wounds")
                    elif effect_type == "CHANGE_INVULN":
                        self.ability_log_buffer.append(f"     • Invulnerable Save: {effect_value}+")
                    elif effect_type == "CHOOSE_STANCE":
                        self.ability_log_buffer.append(f"     • Stance Selection Available")
                else:
                    self.ability_log_buffer.append(f"     • Special: {effect}")
        
        # Mortal damage
        if effects.get("mortal_damage", 0) > 0:
            self.ability_log_buffer.append(f"     • Mortal Wounds: {effects['mortal_damage']}")
    
    def log_stance_selection(self, unit_name: str, stance_name: str, stance_effects: dict):
        """Log stance/option selection"""
        self.ability_log_buffer.append(f"  🎯 [{unit_name}] - Selected Stance: {stance_name}")
        
        if stance_effects.get("ability"):
            self.ability_log_buffer.append(f"     • Melee weapons gain: [{stance_effects['ability']}]")
    
    def log_weapon_modification(self, weapon_name: str, unit_name: str, 
                                modification_type: str, old_value, new_value):
        """Log weapon stat modifications from abilities"""
        self.ability_log_buffer.append(f"  🔧 [{weapon_name}] - Modified by {unit_name} ability:")
        self.ability_log_buffer.append(f"     • {modification_type}: {old_value} → {new_value}")
    
    def log_ability_used_limited(self, ability_name: str, unit_name: str, 
                                 uses_remaining: int, max_uses: int):
        """Log limited-use ability usage"""
        self.ability_log_buffer.append(f"  ⏳ [{ability_name}] - Limited use ability")
        self.ability_log_buffer.append(f"     • Uses remaining: {uses_remaining}/{max_uses}")
    
    def log_reroll_decision(self, ability_name: str, unit_name: str, 
                           reroll_type: str, count: int, accepted: bool):
        """Log reroll decisions"""
        if accepted:
            self.ability_log_buffer.append(f"  🎲 [{ability_name}] - Re-rolling {count} {reroll_type}")
        else:
            self.ability_log_buffer.append(f"  🎲 [{ability_name}] - Re-roll declined for {count} {reroll_type}")
    
    def flush_ability_buffer(self):
        """Flush buffered ability logs to main log"""
        if self.ability_log_buffer:
            self.log_entries.append("")
            self.log_entries.append("  💫 ABILITY SYSTEM:")
            self.log_entries.extend(self.ability_log_buffer)
            self.ability_log_buffer = []
    
    # ============================================
    # PHASE LOGGING METHODS
    # ============================================
    
    def log_command_phase(self, oath_declared: bool = False, oath_target: str = None):
        """Log command phase actions"""
        self.log_entries.append(f"📋 COMMAND PHASE")
        self.log_entries.append("-"*80)
        
        self.log_entries.append(f"Command Points Gained:")
        self.log_entries.append(f"  • {self.unit1_name}: +1 CP")
        self.log_entries.append(f"  • {self.unit2_name}: +1 CP")
        
        if oath_declared and oath_target:
            self.log_entries.append(f"")
            self.log_entries.append(f"⚔️ OATH OF MOMENT DECLARED")
            self.log_entries.append(f"  Target: {oath_target}")
            self.log_entries.append(f"  Effects: Re-roll hit rolls, +1 to wound rolls")
        
        # Flush any ability logs from command phase
        self.flush_ability_buffer()
    
    def log_movement(self, distance: int, movement_actions: dict, movement_details: dict = None):
        """Log movement phase"""
        self.log_entries.append(f"🏃 MOVEMENT PHASE")
        self.log_entries.append("-"*80)
        self.log_entries.append(f"Final Distance: {distance}\"")
        
        if movement_actions:
            self.log_entries.append(f"Movement Actions:")
            for unit, action in movement_actions.items():
                self.log_entries.append(f"  • {unit}: {action}")
        
        self.flush_ability_buffer()
    
    def log_shooting(self, shooter: str, target: str, weapon_name: str,
                     weapon_stats: dict = None, hits: int = 0, wounds: int = 0,
                     saves_failed: int = 0, damage_dealt: int = 0,
                     models_destroyed: int = 0, hazardous_damage: int = 0,
                     special_effects: list = None):
        """Log shooting phase with weapon stats and ability modifications"""
        shooting_count = sum(1 for entry in self.log_entries if "🔫 SHOOTING PHASE" in entry and f"TURN {self.current_turn}" in "\n".join(self.log_entries[-50:]))
        phase_num = shooting_count + 1
        
        self.log_entries.append(f"🔫 SHOOTING PHASE #{phase_num}: {shooter} → {target}")
        self.log_entries.append("-"*80)
        self.log_entries.append(f"Weapon Selected: {weapon_name}")
        
        if weapon_stats:
            weapon_range = weapon_stats.get("range", "N/A")
            attacks = weapon_stats.get("a", "N/A")
            bs = weapon_stats.get("bs", "N/A")
            strength = weapon_stats.get("s", "N/A")
            ap = weapon_stats.get("ap", "N/A")
            damage = weapon_stats.get("d", "N/A")
            
            if isinstance(ap, int) and ap != 0:
                ap_str = f"-{abs(ap)}" if ap > 0 else str(ap)
            else:
                ap_str = str(ap) if ap != "N/A" else "N/A"
            
            bs_str = f"{bs}+" if bs != "N/A" else "N/A"
            
            self.log_entries.append(f"  Stats: Range {weapon_range}\", A{attacks} BS{bs_str} S{strength} AP{ap_str} D{damage}")
        else:
            self.log_entries.append(f"  Stats: Weapon data not available")
        
        # Flush ability logs BEFORE attack summary
        self.flush_ability_buffer()
        
        self.log_entries.append(f"Attack Summary:")
        self.log_entries.append(f"  • Total Hits: {hits}")
        self.log_entries.append(f"  • Total Wounds: {wounds}")
        self.log_entries.append(f"  • Failed Saves: {saves_failed}")
        self.log_entries.append(f"  • Damage Dealt: {damage_dealt}")
        self.log_entries.append(f"  • Models Destroyed: {models_destroyed}")
        
        if hazardous_damage > 0:
            self.log_entries.append(f"  ⚠️ Hazardous: {shooter} suffers {hazardous_damage} mortal wounds")
        
        if special_effects:
            self.log_entries.append(f"Special Effects:")
            for effect in special_effects:
                self.log_entries.append(f"  • {effect}")
    
    def log_charge(self, charger: str, charge_roll: int = None, charge_dice: list = None,
                   successful: bool = False, distance_before: int = 0, distance_needed: int = 0):
        """Log charge phase"""
        self.log_entries.append(f"⚔️ CHARGE PHASE: {charger}")
        self.log_entries.append("-"*80)
        
        if charge_roll is not None:
            self.log_entries.append(f"Charge Roll: {charge_roll}\" (needed {distance_needed}\")")
            
            if successful:
                self.log_entries.append(f"✅ CHARGE SUCCESSFUL - {charger} moves into engagement")
            else:
                self.log_entries.append(f"❌ CHARGE FAILED - {charger} falls short")
        else:
            self.log_entries.append(f"No charge declared")
        
        self.flush_ability_buffer()
    
    def log_fight(self, fighter: str, target: str, weapon_name: str,
                  weapon_stats: dict = None, hits: int = 0, wounds: int = 0,
                  saves_failed: int = 0, damage_dealt: int = 0,
                  models_destroyed: int = 0, fights_first: bool = False,
                  special_effects: list = None):
        """Log fight phase with weapon stats and ability modifications"""
        fight_type = "⚡ FIGHTS FIRST" if fights_first else "⚔️ FIGHTS"
        
        self.log_entries.append(f"{fight_type}: {fighter} → {target}")
        self.log_entries.append("-"*80)
        self.log_entries.append(f"Weapon Selected: {weapon_name}")
        
        if weapon_stats:
            weapon_range = weapon_stats.get("range", "Melee")
            attacks = weapon_stats.get("a", "N/A")
            ws = weapon_stats.get("ws", "N/A")
            strength = weapon_stats.get("s", "N/A")
            ap = weapon_stats.get("ap", "N/A")
            damage = weapon_stats.get("d", "N/A")
            
            if isinstance(ap, int) and ap != 0:
                ap_str = f"-{abs(ap)}" if ap > 0 else str(ap)
            else:
                ap_str = str(ap) if ap != "N/A" else "N/A"
            
            ws_str = f"{ws}+" if ws != "N/A" else "N/A"
            
            self.log_entries.append(f"  Stats: Range {weapon_range}, A{attacks} WS{ws_str} S{strength} AP{ap_str} D{damage}")
        else:
            self.log_entries.append(f"  Stats: Weapon data not available")
        
        # Flush ability logs BEFORE combat summary
        self.flush_ability_buffer()
        
        self.log_entries.append(f"Combat Summary:")
        self.log_entries.append(f"  • Total Hits: {hits}")
        self.log_entries.append(f"  • Total Wounds: {wounds}")
        self.log_entries.append(f"  • Failed Saves: {saves_failed}")
        self.log_entries.append(f"  • Damage Dealt: {damage_dealt}")
        self.log_entries.append(f"  • Models Destroyed: {models_destroyed}")
        
        if special_effects:
            self.log_entries.append(f"Special Effects:")
            for effect in special_effects:
                self.log_entries.append(f"  • {effect}")
    
    def log_special_event(self, event_name: str, event_data: dict):
        """Log special events (abilities, mortal wounds, etc.)"""
        self.log_entries.append(f"")
        self.log_entries.append(f"⚡ SPECIAL EVENT: {event_name}")
        self.log_entries.append("-"*80)
        
        for key, value in event_data.items():
            self.log_entries.append(f"  {key}: {value}")
        
        self.flush_ability_buffer()
    
    def end_turn(self, game_state: dict):
        """Log turn end"""
        attacker = game_state["attacker_unit"]
        defender = game_state["defender_unit"]
        
        a_count = game_state["attacker_count"]
        a_wounds = game_state["attacker_current_wounds"]
        d_count = game_state["defender_count"]
        d_wounds = game_state["defender_current_wounds"]
        
        distance = abs(game_state.get("attacker_position", 0) - game_state.get("defender_position", 0))
        
        self.log_entries.append(f"Turn End: {attacker['Name']} ({a_count} models, {a_wounds}W) vs {defender['Name']} ({d_count} models, {d_wounds}W)")
        self.log_entries.append(f"Distance: {distance}\"")
    
    def log_game_end(self, winner: str, total_turns: int, reason: str = ""):
        """Log game end"""
        self.log_entries.append("")
        self.log_entries.append("="*80)
        self.log_entries.append("GAME END")
        self.log_entries.append("="*80)
        self.log_entries.append(f"Winner: {winner}")
        self.log_entries.append(f"Total Turns: {total_turns}")
        if reason:
            self.log_entries.append(f"Reason: {reason}")
        
        if self.game_start_time:
            end_time = datetime.datetime.now()
            duration = end_time - self.game_start_time
            self.log_entries.append(f"Game Duration: {duration}")
    
    def write_to_file(self, filename: str = None):
        """Write log to file"""
        if filename is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"game_log_{timestamp}.txt"
        
        os.makedirs("logs", exist_ok=True)
        filepath = os.path.join("logs", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for entry in self.log_entries:
                f.write(entry + '\n')
        
        print(f"\n📝 Game log saved to: {filepath}")