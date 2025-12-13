#/test.py
import menu
import utils
import army
import gameOBJ.dicebox as dicebox
import phases.testPhases as testPhases

# print("===---------------------------------------===")
# currentKT, loaded, chosenVal = menu.ktSelectScreen()
# print("----------------------")
# selectedOps = menu.opSelectScreen(currentKT, loaded, chosenVal)
# # print(f"Test.py Output: {selectedOps}")
# print("----------------------")
# opData = army.getOpData(currentKT, selectedOps)
# # print(f"Test.py Output: {opData}")
# print("----------------------")
# # [PROBLEM] This screen should display shooting and melee weapon selection one-by-one, but shows a whole list instead
# # then only prompts user to 
# opLoadouts = menu.opLoadoutScreen(currentKT, opData)
# print(f"Test.py Output: {opLoadouts}")
# print("----------------------")
# finalOpData = army.finalizeOp(currentKT, opData, opLoadouts)
# # print(f"Test.py Output: {finalOpData}")
# print("----------------------")
# army.opDatasheet(finalOpData)
# print("===---------------------------------------===")




print("===---------------------------------------===")
print("-------- 'gamOBJ/dicebox.py' TEST -------")
atk = 4
hit = 3
sv = 3
testOperativeHP = 15
testOpponentDmg = 3
testOpponentCrit = 4

hRollRes, successRolls, critRolls, totalSuccessRolls, failedRolls = dicebox.hRoll(atk, hit)
print(f"ROLLED {atk} HIT ROLL! DICE BOX SHOWS: {hRollRes}; \nSUCCESSFULL ROLLS ARE ON A {hit}+;")
if successRolls != 0:
    print(f"    YOU'VE SUCCESSFULLY ROLLED {successRolls} HITS!")

if critRolls != 0:
    print(f"    YOU'VE SUCCESSFULLY ROLLED {critRolls} CRITIAL HITS!")

if failedRolls != 0:
    print(f"    YOU'VE AUTO FAILED {failedRolls} (rolls = 1) ROLLS!")

if successRolls != 0 or critRolls != 0:
    print(f">>> YOU'VE SUCCESSFULLY ROLLED {totalSuccessRolls} ROLLS IN TOTAL! <<<")
elif successRolls == 0 and critRolls == 0:
    print(f">>> YOU'VE FAILLED ALL HITs ROLLS! <<<")

print("----------------------")

saveDiceBox, svSuccessCtr, svCritCtr, failedSvs = dicebox.saveRoll(sv)
print("----------------------")
hits, crits = testPhases.defenseScreen(svSuccessCtr, svCritCtr, failedSvs, successRolls, critRolls, totalSuccessRolls)
print("----------------------")
testOperativeRemainingHP = testPhases.damageAllocation(hits, crits, testOperativeHP, testOpponentDmg, testOpponentCrit)
print(f"\n ----- OPERATIVE HAS {testOperativeRemainingHP} WOUNDS REMAINING! -----")
print("----------------------")



# ------------------- WOUND ROLL TESTING, RESEVERVED FOR LATER TESTING IN 40K ---------------------
# print("----------------------")
# weaponStr = 4
# opponentTough = 5
# wRollRes, wSuccessRolls, wCritRolls, finalSuccessRolls, successCond = dicebox.wRoll(totalSuccessRolls, weaponStr, opponentTough)
# print(f"ROLLED {rolls} WOUND ROLLS! DICE BOX SHOWS: {wRollRes}; \nSUCCESSFULL ROLLS ARE ON A {successCond}+")
# if wSuccessRolls != 0:
#     print(f"    YOU'VE SUCCESSFULLY ROLLED {wSuccessRolls} HITS!")

# if wCritRolls != 0:
#     print(f"    YOU'VE SUCCESSFULLY ROLLED {wCritRolls} CRITIAL HITS!")

# if wSuccessRolls != 0 or wCritRolls != 0:
#     print(f">>> YOU'VE SUCCESSFULLY ROLLED {finalSuccessRolls} WOUND ROLLS IN TOTAL! <<<")
# elif wSuccessRolls == 0 and wCritRolls == 0:
#     print(f">>> YOU'VE FAILLED ALL WOUND ROLLS! <<<")

print("===---------------------------------------===")

# import numpy as np
# np.random.seed(42)

# def roll_d6(n=1):
#     return np.random.randint(1, 7, n)

# def lion_strike_damage(guards_w, traj_w):
#     # Lion Fealty-Strike: A8 WS2+ S12 -4 D4 Lethal Hits vs T6 4++
#     hits_raw = roll_d6(8)
#     crit_hits = np.sum(hits_raw == 6)
#     normal_hits = np.sum((hits_raw >= 2) & (hits_raw < 6))
#     total_hits = normal_hits + crit_hits
#     lethal_wounds = crit_hits  # auto-wound
#     normal_wounds_roll = roll_d6(normal_hits)
#     normal_wounds = np.sum(normal_wounds_roll >= 2)  # 2+
#     total_wounds = lethal_wounds + normal_wounds
#     save_fails = roll_d6(total_wounds)
#     unsaved = np.sum(save_fails <= 3)  # 4++ fail 1-3
#     dmg_rolls = roll_d6(unsaved)  # D4 as D6/1.75 approx but use D6 mean adjust? Wait D4: 1-4
#     dmg = np.sum(np.clip(dmg_rolls, 1, 4))  # D4
#     # Allocate to guards first
#     dmg_dealt = 0
#     for i in range(4):
#         if guards_w[i] > 0:
#             alloc = min(dmg, guards_w[i])
#             guards_w[i] -= alloc
#             dmg -= alloc
#             dmg_dealt += alloc
#             if dmg == 0:
#                 break
#     if dmg > 0 and traj_w > 0:
#         alloc = min(dmg, traj_w)
#         traj_w -= alloc
#         dmg_dealt += alloc
#     return dmg_dealt, guards_w, traj_w

# def cust_fight_damage(lion_w):
#     # 4 Guards Spear Melee A5 WS2+ S7 -2 D2 Stand Vigil reroll wound 1s; T9 Shield -> wound 5+ reroll1 ~3+/6
#     # Trajann Axe A6 WS2+ S10 -2 D3; wound 4+ Shield
#     # Assume Moment Shackle A12 on Turn2+ for fair
#     guard_att = 5 * np.sum([g > 0 for g in guards_w])
#     traj_att = 12 if moment_used else 6  # placeholder
#     # Simplified EV but full dice
#     # Guards
#     guard_hits = np.sum(roll_d6(guard_att) >=2)
#     guard_wounds_raw = roll_d6(guard_hits)
#     guard_wounds_reroll = guard_wounds_raw[guard_wounds_raw ==1]
#     if len(guard_wounds_reroll):
#         rerolls = roll_d6(len(guard_wounds_reroll))
#         guard_wounds = np.sum(guard_wounds_raw >=5) + np.sum(rerolls >=5)
#     else:
#         guard_wounds = np.sum(guard_wounds_raw >=5)
#     guard_unsaved = np.sum(roll_d6(guard_wounds) <=3)  # 3++ fail 1-3
#     guard_dmg = 2 * guard_unsaved  # D2
#     # Trajann
#     traj_hits = np.sum(roll_d6(traj_att) >=2)
#     traj_wounds_raw = roll_d6(traj_hits)
#     traj_wounds = np.sum(traj_wounds_raw >=4)  # 4+
#     traj_unsaved = np.sum(roll_d6(traj_wounds) <=3)
#     traj_dmg = np.sum(roll_d6(traj_unsaved) +1)  # D3 avg 2 but roll D6/2 +1 approx D3 2-4 -> D6//2 +2? Use np.random.choice([2,3,4])
#     traj_dmg = sum(np.random.choice([2,3,4], traj_unsaved))
#     total_dmg = guard_dmg + traj_dmg
#     lion_w -= total_dmg
#     return lion_w

# # Full battle sim
# def run_battle():
#     lion_w = 10
#     traj_w = 7
#     guards_w = [3.0] * 4  # float for sub
#     gap = 36.0
#     rounds = 0
#     engaged = False
#     moment_used = False
#     lion_wins = 0
#     while lion_w > 0 and (traj_w > 0 or any(g > 0 for g in guards_w)) and rounds <20:
#         rounds +=1
#         # Lion turn
#         # Move
#         gap -= 8
#         if gap < 0:
#             gap = 0
#         # Shoot if <=12 (Pistol A4 BS2+ S4 -1 D2 vs T6 4++)
#         if gap <=12:
#             hits = np.sum(roll_d6(4) >=2)
#             wounds = np.sum(roll_d6(hits) >=4)  # 4+
#             unsaved = np.sum(roll_d6(wounds) <=3)  # 4++
#             dmg = 2 * unsaved
#             # Alloc
#             for i in range(4):
#                 if guards_w[i] > 0:
#                     alloc = min(dmg, guards_w[i])
#                     guards_w[i] -= alloc
#                     dmg -= alloc
#                     if dmg == 0:
#                         break
#             if dmg > 0 and traj_w > 0:
#                 traj_w -= min(dmg, traj_w)
#         # Charge if not engaged and gap <=12
#         if not engaged and gap <=12:
#             charge = roll_d6(2).sum()
#             if gap <= charge:
#                 engaged = True
#                 # Fight Strike Fights First
#                 dmg_dealt, guards_w, traj_w = lion_strike_damage(guards_w, traj_w)
#         # Cust turn
#         # Advance if not engaged
#         if not engaged:
#             adv = roll_d6() +6
#             gap -= adv
#             if gap <0:
#                 gap = 0
#         # Shoot if <=24 and not engaged
#         if not engaged and gap <=24:
#             # 4 Guards A2 BS2+ S4 -1 D2 Stand Vigil? No for ranged
#             guard_hits = np.sum(roll_d6(8) >=2)
#             guard_wounds = np.sum(roll_d6(guard_hits) >=6)  # S4 vs T9 6+
#             guard_reroll1 = roll_d6(np.sum(guard_wounds_raw ==1)) if 'guard_wounds_raw' else 0  # approx np.sum >=6 ~16.7%
#             guard_unsaved = np.sum(roll_d6(guard_wounds) <=3)  # 3++
#             guard_dmg = 2 * guard_unsaved
#             # Trajann Eagle A2 BS2+ S5 -2 D3 vs T9 6+
#             traj_hits = np.sum(roll_d6(2) >=2)
#             traj_wounds = np.sum(roll_d6(traj_hits) >=6)
#             traj_unsaved = np.sum(roll_d6(traj_wounds) <=3)
#             traj_dmg_rolls = np.random.choice([2,3,4], traj_unsaved)
#             traj_dmg = sum(traj_dmg_rolls)
#             total_dmg = guard_dmg + traj_dmg
#             lion_w -= total_dmg
#         # Charge if not engaged
#         if not engaged and gap <=12:
#             charge = roll_d6(2).sum()
#             if gap <= charge:
#                 engaged = True
#         # Fight if engaged
#         if engaged:
#             # Lion Fights First Strike
#             dmg_dealt, guards_w, traj_w = lion_strike_damage(guards_w, traj_w)
#             if traj_w <=0 and all(g <=0 for g in guards_w):
#                 break
#             # Cust fight
#             if moment_used == False and rounds >=2:
#                 traj_att = 12
#                 moment_used = True
#             else:
#                 traj_att = 6
#             # Guards Spear
#             num_alive = sum(1 for g in guards_w if g >0)
#             guard_att = 5 * num_alive
#             guard_hits = np.sum(roll_d6(int(guard_att)) >=2)
#             guard_wounds_raw = roll_d6(guard_hits)
#             guard_wounds1 = np.sum(guard_wounds_raw >=5)  # 5+
#             num1s = np.sum(guard_wounds_raw ==1)
#             if num1s >0:
#                 rerolls = roll_d6(int(num1s))
#                 guard_wounds1 += np.sum(rerolls >=5)
#             guard_unsaved = np.sum(roll_d6(int(guard_wounds1)) <=3)  # 3++
#             guard_dmg = 2 * guard_unsaved
#             # Trajann Axe
#             traj_hits = np.sum(roll_d6(traj_att) >=2)
#             traj_wounds_raw = roll_d6(traj_hits)
#             traj_wounds = np.sum(traj_wounds_raw >=4)  # 4+
#             traj_unsaved = np.sum(roll_d6(int(traj_wounds)) <=3)
#             traj_dmg_rolls = np.random.choice([2,3,4], int(traj_unsaved))
#             traj_dmg = sum(traj_dmg_rolls)
#             total_cust_dmg = guard_dmg + traj_dmg
#             lion_w -= total_cust_dmg
#             if lion_w <=0:
#                 break
#     if lion_w >0:
#         return 'Lion', rounds, 10 - lion_w  # dmg taken
#     else:
#         return 'Cust', rounds, 16 - (sum(guards_w) + traj_w)  # total Cust W 7+12=19? Guards 12W, Traj7 =19

# # Run 100
# np.random.seed(42)
# results = []
# lion_wins = 0
# cust_wins = 0
# avg_rounds_lion = []
# avg_rounds_cust = []
# avg_dmg_lion = []
# avg_dmg_cust = []
# for i in range(100):
#     winner, rounds, dmg_dealt = run_battle()
#     results.append((winner, rounds, dmg_dealt))
#     if winner == 'Lion':
#         lion_wins +=1
#         avg_rounds_lion.append(rounds)
#         avg_dmg_lion.append(dmg_dealt)
#     else:
#         cust_wins +=1
#         avg_rounds_cust.append(rounds)
#         avg_dmg_cust.append(dmg_dealt)

# print(f"Lion Win Rate: {lion_wins/100*100:.1f}% ({lion_wins}/100)")
# print(f"Cust Win Rate: {cust_wins/100*100:.1f}% ({cust_wins}/100)")
# print(f"Avg Rounds Lion Win: {np.mean(avg_rounds_lion):.1f}")
# print(f"Avg Rounds Cust Win: {np.mean(avg_rounds_cust):.1f}")
# print(f"Avg Dmg Dealt Lion Wins: {np.mean(avg_dmg_lion):.1f}")
# print(f"Avg Dmg Dealt Cust Wins: {np.mean(avg_dmg_cust):.1f}")
# print("Sample 10 runs winners:", [r[0] for r in results[:10]])