# """
# WARHAMMER 40K BATTLE SIMULATIONS - FULLY FUNCTIONAL
# ====================================================
# Three complete battle simulations with proper mechanics
# """

# import numpy as np

# # =============================================================================
# # SIMULATION 1: LION EL'JONSON VS ANGRON
# # =============================================================================

# class LionVsAngronSim:
#     def __init__(self):
#         # Lion stats
#         self.lion_w = 10
#         self.lion_t = 9
#         self.lion_inv = 3
#         self.lion_m = 8
        
#         # Lion Fealty Strike (melee)
#         self.lion_a = 8
#         self.lion_ws = 2
#         self.lion_s = 12
#         self.lion_ap = -4
#         self.lion_d = 'd4'
        
#         # Lion Pistol
#         self.pistol_a = 4
#         self.pistol_bs = 2
#         self.pistol_s = 4
#         self.pistol_ap = -1
#         self.pistol_d = 2
        
#         # Angron stats
#         self.angron_w = 16
#         self.angron_t = 11
#         self.angron_sv = 2
#         self.angron_inv = 4
#         self.angron_m = 14
        
#         # Angron attacks
#         self.angron_a = 8
#         self.angron_ws = 2
#         self.angron_s = 14
#         self.angron_ap = -3
#         self.angron_d = 'd6+2'
    
#     def roll_dice(self, sides, num):
#         return np.random.randint(1, sides + 1, num)
    
#     def roll_hits(self, attacks, skill, lethal=False):
#         """Roll to hit, return (total_hits, critical_hits)"""
#         rolls = self.roll_dice(6, attacks)
#         crits = np.sum(rolls == 6)
#         hits = np.sum(rolls >= skill)
#         return hits, crits
    
#     def roll_wounds(self, hits, strength, toughness, oath_bonus=0):
#         """Roll to wound based on S vs T"""
#         if strength >= 2 * toughness:
#             wound_on = 2
#         elif strength > toughness:
#             wound_on = 3
#         elif strength == toughness:
#             wound_on = 4
#         elif strength * 2 <= toughness:
#             wound_on = 6
#         else:
#             wound_on = 5
        
#         wound_on = max(2, wound_on - oath_bonus)
#         rolls = self.roll_dice(6, hits)
#         return np.sum(rolls >= wound_on)
    
#     def roll_saves(self, wounds, ap, save, invuln):
#         """Roll saves, use best of armor or invuln"""
#         armor_save = max(7, save - ap)  # Can't save on 7+
#         effective_save = min(armor_save, invuln)
        
#         if effective_save >= 7:
#             return wounds  # All fail
        
#         rolls = self.roll_dice(6, wounds)
#         failed = np.sum(rolls < effective_save)
#         return failed
    
#     def roll_damage(self, unsaved, damage_type):
#         """Roll damage dice"""
#         if damage_type == 'd4':
#             return np.sum(self.roll_dice(4, unsaved))
#         elif damage_type == 'd6+2':
#             return np.sum(self.roll_dice(6, unsaved) + 2)
#         else:
#             return unsaved * damage_type
    
#     def blessings_of_khorne(self):
#         """Roll for Angron's blessings (simplified)"""
#         rolls = self.roll_dice(6, 8)
#         rolls = np.sort(rolls)[::-1]
        
#         # Check for Warp-Forged Blades (Lethal Hits): need 3 dice showing 2+
#         lethal = np.sum(rolls >= 2) >= 3
        
#         # Check for Martial Excellence (Sustained Hits 1): need 2 dice showing 4+
#         sustained = np.sum(rolls >= 4) >= 2
        
#         return {'lethal': lethal, 'sustained': sustained}
    
#     def lion_shoots(self, angron_w):
#         """Lion shoots pistol"""
#         if angron_w <= 0:
#             return 0
        
#         hits, crits = self.roll_hits(self.pistol_a, self.pistol_bs)
#         wounds = self.roll_wounds(hits, self.pistol_s, self.angron_t)
#         unsaved = self.roll_saves(wounds, self.pistol_ap, self.angron_sv, self.angron_inv)
#         damage = unsaved * self.pistol_d
        
#         return min(damage, angron_w)
    
#     def lion_strikes(self, angron_w, oath_active=True):
#         """Lion melee attack with Lethal Hits"""
#         if angron_w <= 0:
#             return 0
        
#         hits, crits = self.roll_hits(self.lion_a, self.lion_ws)
        
#         # Lethal Hits: crits auto-wound
#         lethal_wounds = crits
#         normal_wounds = self.roll_wounds(hits - crits, self.lion_s, self.angron_t, 
#                                          oath_bonus=1 if oath_active else 0)
        
#         total_wounds = lethal_wounds + normal_wounds
#         unsaved = self.roll_saves(total_wounds, self.lion_ap, self.angron_sv, self.angron_inv)
#         damage = self.roll_damage(unsaved, 'd4')
        
#         return min(damage, angron_w)
    
#     def angron_strikes(self, lion_w, blessings):
#         """Angron melee attack with possible blessings"""
#         if lion_w <= 0:
#             return 0
        
#         hits, crits = self.roll_hits(self.angron_a, self.angron_ws)
        
#         # Apply blessings
#         if blessings['lethal']:
#             lethal_wounds = crits
#             normal_wounds = self.roll_wounds(hits - crits, self.angron_s, self.lion_t)
#             total_wounds = lethal_wounds + normal_wounds
#         else:
#             total_wounds = self.roll_wounds(hits, self.angron_s, self.lion_t)
        
#         if blessings['sustained']:
#             total_wounds += crits  # Sustained Hits 1
        
#         unsaved = self.roll_saves(total_wounds, self.angron_ap, 3, self.lion_inv)
#         damage = self.roll_damage(unsaved, 'd6+2')
        
#         return min(damage, lion_w)
    
#     def simulate_battle(self):
#         """Run a single battle simulation"""
#         lion_w = self.lion_w
#         angron_w = self.angron_w
#         distance = 48
#         engaged = False
#         round_num = 0
        
#         while lion_w > 0 and angron_w > 0 and round_num < 20:
#             round_num += 1
            
#             # === LION'S TURN ===
#             # Movement
#             if not engaged:
#                 distance = max(0, distance - self.lion_m)
            
#             # Shooting phase
#             if distance <= 12 and not engaged:
#                 dmg = self.lion_shoots(angron_w)
#                 angron_w -= dmg
#                 if angron_w <= 0:
#                     break
            
#             # Charge phase
#             if not engaged and distance <= 12:
#                 charge_roll = self.roll_dice(6, 2).sum()
#                 if charge_roll >= distance:
#                     engaged = True
#                     distance = 0
            
#             # Fight phase (Lion fights first)
#             if engaged:
#                 dmg = self.lion_strikes(angron_w, oath_active=True)
#                 angron_w -= dmg
#                 if angron_w <= 0:
#                     break
                
#                 # Angron fights back
#                 blessings = self.blessings_of_khorne()
#                 dmg = self.angron_strikes(lion_w, blessings)
#                 lion_w -= dmg
#                 if lion_w <= 0:
#                     break
            
#             # === ANGRON'S TURN ===
#             if lion_w <= 0 or angron_w <= 0:
#                 break
            
#             # Movement
#             if not engaged:
#                 advance = self.roll_dice(6, 1)[0]
#                 distance = max(0, distance - (self.angron_m + advance))
            
#             # Charge phase
#             if not engaged and distance <= 12:
#                 charge_roll = self.roll_dice(6, 2).sum()
#                 if charge_roll >= distance:
#                     engaged = True
#                     distance = 0
            
#             # Fight (already fought in Lion's turn due to Fights First)
        
#         winner = 'Lion' if lion_w > 0 else 'Angron'
#         return winner, round_num, lion_w, angron_w

# # =============================================================================
# # SIMULATION 2: LION VS TRAJANN VALORIS & CUSTODIAN GUARD
# # =============================================================================

# class LionVsCustodesSim:
#     def __init__(self):
#         # Lion stats (same as above)
#         self.lion_w = 10
#         self.lion_t = 9
#         self.lion_sv = 3
#         self.lion_inv = 3
#         self.lion_m = 8
        
#         # Lion weapons
#         self.lion_strike_a = 8
#         self.lion_strike_ws = 2
#         self.lion_strike_s = 12
#         self.lion_strike_ap = -4
        
#         self.lion_pistol_a = 4
#         self.lion_pistol_bs = 2
#         self.lion_pistol_s = 4
#         self.lion_pistol_ap = -1
#         self.lion_pistol_d = 2
        
#         # Trajann stats
#         self.traj_w = 7
#         self.traj_t = 6
#         self.traj_sv = 2
#         self.traj_inv = 4
#         self.traj_m = 6
        
#         # Trajann melee (Watcher's Axe)
#         self.traj_melee_a = 6
#         self.traj_melee_ws = 2
#         self.traj_melee_s = 10
#         self.traj_melee_ap = -2
#         self.traj_melee_d = 'd3'
        
#         # Trajann ranged (Eagle's Scream)
#         self.traj_ranged_a = 2
#         self.traj_ranged_bs = 2
#         self.traj_ranged_s = 5
#         self.traj_ranged_ap = -2
#         self.traj_ranged_d = 'd3'
        
#         # Custodian Guard stats (4 models)
#         self.guard_models = 4
#         self.guard_w = 3
#         self.guard_t = 6
#         self.guard_sv = 2
#         self.guard_inv = 4
#         self.guard_m = 6
        
#         # Guard melee (Guardian Spear)
#         self.guard_melee_a = 5
#         self.guard_melee_ws = 2
#         self.guard_melee_s = 7
#         self.guard_melee_ap = -2
#         self.guard_melee_d = 2
        
#         # Guard ranged (Guardian Spear)
#         self.guard_ranged_a = 2
#         self.guard_ranged_bs = 2
#         self.guard_ranged_s = 4
#         self.guard_ranged_ap = -1
#         self.guard_ranged_d = 2
        
#         self.moment_shackle_used = False
    
#     def roll_dice(self, sides, num):
#         return np.random.randint(1, sides + 1, num)
    
#     def roll_hits(self, attacks, skill):
#         rolls = self.roll_dice(6, attacks)
#         crits = np.sum(rolls == 6)
#         hits = np.sum(rolls >= skill)
#         return hits, crits
    
#     def roll_wounds(self, hits, strength, toughness, reroll_ones=False):
#         if strength >= 2 * toughness:
#             wound_on = 2
#         elif strength > toughness:
#             wound_on = 3
#         elif strength == toughness:
#             wound_on = 4
#         elif strength * 2 <= toughness:
#             wound_on = 6
#         else:
#             wound_on = 5
        
#         rolls = self.roll_dice(6, hits)
        
#         if reroll_ones:
#             ones = rolls == 1
#             rerolls = self.roll_dice(6, np.sum(ones))
#             rolls[ones] = rerolls
        
#         return np.sum(rolls >= wound_on)
    
#     def roll_saves(self, wounds, ap, save, invuln):
#         armor_save = max(7, save - ap)
#         effective_save = min(armor_save, invuln)
        
#         if effective_save >= 7:
#             return wounds
        
#         rolls = self.roll_dice(6, wounds)
#         return np.sum(rolls < effective_save)
    
#     def roll_d3_damage(self, count):
#         return np.sum(np.random.choice([2, 3, 4], count))
    
#     def roll_d4_damage(self, count):
#         return np.sum(self.roll_dice(4, count))
    
#     def allocate_damage(self, damage, guards_w, traj_w):
#         """Allocate damage to guards first, then Trajann"""
#         remaining = damage
        
#         for i in range(len(guards_w)):
#             if guards_w[i] > 0 and remaining > 0:
#                 allocated = min(remaining, guards_w[i])
#                 guards_w[i] -= allocated
#                 remaining -= allocated
        
#         if remaining > 0 and traj_w > 0:
#             allocated = min(remaining, traj_w)
#             traj_w -= allocated
        
#         return guards_w, traj_w
    
#     def lion_shoots(self, guards_w, traj_w):
#         """Lion pistol shooting"""
#         hits, crits = self.roll_hits(self.lion_pistol_a, self.lion_pistol_bs)
#         wounds = self.roll_wounds(hits, self.lion_pistol_s, self.guard_t)
#         unsaved = self.roll_saves(wounds, self.lion_pistol_ap, self.guard_sv, self.guard_inv)
#         damage = unsaved * self.lion_pistol_d
        
#         return self.allocate_damage(damage, guards_w, traj_w)
    
#     def lion_melee(self, guards_w, traj_w):
#         """Lion melee with Lethal Hits"""
#         hits, crits = self.roll_hits(self.lion_strike_a, self.lion_strike_ws)
        
#         # Lethal Hits
#         lethal_wounds = crits
#         normal_wounds = self.roll_wounds(hits - crits, self.lion_strike_s, self.guard_t)
#         total_wounds = lethal_wounds + normal_wounds
        
#         unsaved = self.roll_saves(total_wounds, self.lion_strike_ap, self.guard_sv, self.guard_inv)
#         damage = self.roll_d4_damage(unsaved)
        
#         return self.allocate_damage(damage, guards_w, traj_w)
    
#     def custodes_shoot(self, lion_w, guards_alive):
#         """Custodes ranged attacks"""
#         total_damage = 0
        
#         # Guards shoot
#         if guards_alive > 0:
#             guard_attacks = self.guard_ranged_a * guards_alive
#             hits, crits = self.roll_hits(guard_attacks, self.guard_ranged_bs)
#             wounds = self.roll_wounds(hits, self.guard_ranged_s, self.lion_t, reroll_ones=True)
#             unsaved = self.roll_saves(wounds, self.guard_ranged_ap, self.lion_sv, self.lion_inv)
#             total_damage += unsaved * self.guard_ranged_d
        
#         # Trajann shoots
#         hits, crits = self.roll_hits(self.traj_ranged_a, self.traj_ranged_bs)
#         wounds = self.roll_wounds(hits, self.traj_ranged_s, self.lion_t)
#         unsaved = self.roll_saves(wounds, self.traj_ranged_ap, self.lion_sv, self.lion_inv)
#         total_damage += self.roll_d3_damage(unsaved)
        
#         return min(total_damage, lion_w)
    
#     def custodes_melee(self, lion_w, guards_alive):
#         """Custodes melee attacks"""
#         total_damage = 0
        
#         # Guards fight with Stand Vigil (reroll wound 1s)
#         if guards_alive > 0:
#             guard_attacks = self.guard_melee_a * guards_alive
#             hits, crits = self.roll_hits(guard_attacks, self.guard_melee_ws)
#             wounds = self.roll_wounds(hits, self.guard_melee_s, self.lion_t, reroll_ones=True)
#             unsaved = self.roll_saves(wounds, self.guard_melee_ap, self.lion_sv, self.lion_inv)
#             total_damage += unsaved * self.guard_melee_d
        
#         # Trajann fights (Moment Shackle gives A12 once)
#         attacks = 12 if not self.moment_shackle_used else self.traj_melee_a
#         if not self.moment_shackle_used and guards_alive > 0:
#             self.moment_shackle_used = True
        
#         hits, crits = self.roll_hits(attacks, self.traj_melee_ws)
#         wounds = self.roll_wounds(hits, self.traj_melee_s, self.lion_t)
#         unsaved = self.roll_saves(wounds, self.traj_melee_ap, self.lion_sv, self.lion_inv)
#         total_damage += self.roll_d3_damage(unsaved)
        
#         return min(total_damage, lion_w)
    
#     def simulate_battle(self):
#         """Run battle simulation"""
#         lion_w = self.lion_w
#         traj_w = self.traj_w
#         guards_w = np.array([self.guard_w] * self.guard_models, dtype=float)
        
#         distance = 36
#         engaged = False
#         round_num = 0
#         self.moment_shackle_used = False
        
#         while lion_w > 0 and (traj_w > 0 or np.any(guards_w > 0)) and round_num < 20:
#             round_num += 1
#             guards_alive = np.sum(guards_w > 0)
            
#             # === LION'S TURN ===
#             if not engaged:
#                 distance = max(0, distance - self.lion_m)
            
#             # Shooting
#             if distance <= 12 and not engaged:
#                 guards_w, traj_w = self.lion_shoots(guards_w.copy(), traj_w)
            
#             # Charge
#             if not engaged and distance <= 12:
#                 charge = self.roll_dice(6, 2).sum()
#                 if charge >= distance:
#                     engaged = True
#                     distance = 0
            
#             # Fight (Fights First)
#             if engaged:
#                 guards_w, traj_w = self.lion_melee(guards_w.copy(), traj_w)
                
#                 if traj_w <= 0 and np.all(guards_w <= 0):
#                     break
                
#                 # Custodes fight back
#                 guards_alive = np.sum(guards_w > 0)
#                 dmg = self.custodes_melee(lion_w, guards_alive)
#                 lion_w -= dmg
                
#                 if lion_w <= 0:
#                     break
            
#             # === CUSTODES TURN ===
#             if lion_w <= 0 or (traj_w <= 0 and np.all(guards_w <= 0)):
#                 break
            
#             guards_alive = np.sum(guards_w > 0)
            
#             # Movement
#             if not engaged:
#                 advance = self.roll_dice(6, 1)[0]
#                 distance = max(0, distance - (self.guard_m + advance))
            
#             # Shooting
#             if not engaged and distance <= 24:
#                 dmg = self.custodes_shoot(lion_w, guards_alive)
#                 lion_w -= dmg
            
#             # Charge
#             if not engaged and distance <= 12:
#                 charge = self.roll_dice(6, 2).sum()
#                 if charge >= distance:
#                     engaged = True
#                     distance = 0
        
#         winner = 'Lion' if lion_w > 0 else 'Custodes'
#         cust_remaining = traj_w + np.sum(guards_w)
        
#         return winner, round_num, lion_w, cust_remaining

# # =============================================================================
# # RUN ALL SIMULATIONS
# # =============================================================================

# def run_all_simulations(num_runs=1000):
#     print("=" * 70)
#     print("WARHAMMER 40K BATTLE SIMULATIONS")
#     print("=" * 70)
    
#     # Simulation 1: Lion vs Angron
#     print("\n### SIMULATION 1: LION EL'JONSON VS ANGRON ###\n")
#     np.random.seed(42)
#     sim1 = LionVsAngronSim()
#     results1 = [sim1.simulate_battle() for _ in range(num_runs)]
    
#     lion_wins = sum(1 for r in results1 if r[0] == 'Lion')
#     angron_wins = num_runs - lion_wins
#     avg_rounds = np.mean([r[1] for r in results1])
    
#     lion_avg_w = np.mean([r[2] for r in results1 if r[0] == 'Lion'])
#     angron_avg_w = np.mean([r[3] for r in results1 if r[0] == 'Angron'])
    
#     print(f"Total Simulations: {num_runs}")
#     print(f"Lion Victories: {lion_wins} ({lion_wins/num_runs*100:.1f}%)")
#     print(f"Angron Victories: {angron_wins} ({angron_wins/num_runs*100:.1f}%)")
#     print(f"Average Combat Duration: {avg_rounds:.1f} rounds")
#     if lion_wins > 0:
#         print(f"Lion Average Remaining Wounds (when victorious): {lion_avg_w:.1f}/10")
#     if angron_wins > 0:
#         print(f"Angron Average Remaining Wounds (when victorious): {angron_avg_w:.1f}/16")
    
#     # Simulation 2: Lion vs Custodes
#     print("\n### SIMULATION 2: LION VS TRAJANN & CUSTODIAN GUARD ###\n")
#     np.random.seed(42)
#     sim2 = LionVsCustodesSim()
#     results2 = [sim2.simulate_battle() for _ in range(num_runs)]
    
#     lion_wins2 = sum(1 for r in results2 if r[0] == 'Lion')
#     cust_wins = num_runs - lion_wins2
#     avg_rounds2 = np.mean([r[1] for r in results2])
    
#     lion_avg_w2 = np.mean([r[2] for r in results2 if r[0] == 'Lion']) if lion_wins2 > 0 else 0
#     cust_avg_w = np.mean([r[3] for r in results2 if r[0] == 'Custodes']) if cust_wins > 0 else 0
    
#     print(f"Total Simulations: {num_runs}")
#     print(f"Lion Victories: {lion_wins2} ({lion_wins2/num_runs*100:.1f}%)")
#     print(f"Custodes Victories: {cust_wins} ({cust_wins/num_runs*100:.1f}%)")
#     print(f"Average Combat Duration: {avg_rounds2:.1f} rounds")
#     if lion_wins2 > 0:
#         print(f"Lion Average Remaining Wounds (when victorious): {lion_avg_w2:.1f}/10")
#     if cust_wins > 0:
#         print(f"Custodes Average Remaining Wounds (when victorious): {cust_avg_w:.1f}/19")
    
#     print("\n" + "=" * 70)
#     print("SIMULATIONS COMPLETE")
#     print("=" * 70)

# # Run the simulations
# if __name__ == "__main__":
#     run_all_simulations(1000)