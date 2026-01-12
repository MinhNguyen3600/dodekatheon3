# import random
# import numpy as np

# def roll_d6(n=1):
#     return [random.randint(1,6) for _ in range(n)]

# def sim_weapon_ev(A, WS, S, AP, D_avg, T, Sv_mod, invuln=None, num_attacks_per_sim=1, num_sims=10000):
#     hit_req = 2 if WS == '2+' else 3
#     wound_req_base = (S - T + 4) if S >= T else (T - S + 4)
#     if S > T:
#         wound_req = max(2, wound_req_base -1)  # Shield -1 if attacker S > def T, but wait no: Shield is def ability for Lion etc, attacker here Warden
#     else:
#         wound_req = wound_req_base
#     save_req = Sv_mod - AP +1 if Sv_mod else 7
#     p_hit = (7 - hit_req)/6.0
#     p_wound = max(0, (7 - wound_req)/6.0)
#     if invuln:
#         p_unsaved = (7 - int(invuln[1:])) /6.0
#     else:
#         p_unsaved = max(0, (7 - save_req)/6.0)
#     ev = A * p_hit * p_wound * p_unsaved * D_avg
#     return ev

# # Correct Shield: for targets with Shield (Lion/Angron/Trajann), if attacker S > target T, wound_req +=1 (subtract 1 from roll = harder)
# # So p_wound lower

# def sim_single_activation(weapon, target, seed=None):
#     if seed:
#         random.seed(seed)
#     A, WS, S, AP, D_type = weapon  # D_type 'D2','D3','D4' etc
#     T, Sv, invuln, has_shield = target
#     hits = []
#     for _ in range(A):
#         hit_roll = random.randint(1,6)
#         if hit_roll >= (2 if WS=='2+' else 3):
#             # wound
#             wound_roll = random.randint(1,6)
#             wound_req = max(2, (T - S + 4) if S < T else (S - T + 4))
#             if has_shield and S > T:
#                 wound_roll -=1  # effective
#                 if wound_roll <2: wound_roll=1  # min1
#             if wound_roll >= wound_req:
#                 # save
#                 if invuln:
#                     save_roll = random.randint(1,6)
#                     save_req = int(invuln.replace('+',''))
#                     if save_roll < save_req:
#                         # dmg
#                         if D_type == 'D2':
#                             dmg = random.randint(1,2)
#                         elif D_type == 'D3':
#                             dmg = random.randint(1,3)
#                         elif D_type == 'D6+2':
#                             dmg = random.randint(1,6) +2
#                         hits.append(dmg)
#                 else:
#                     save_roll = random.randint(1,6)
#                     save_req = Sv - AP +1
#                     if save_req >6: save_req=7
#                     if save_roll < save_req:
#                         dmg = random.randint(1, int(D_type[1]))
#                         hits.append(dmg)
#     return sum(hits)

# # Targets
# sm_target = (4, 3, None, False)  # T4 Sv3+
# traj_target = (6, 3, '4+', True)  # T6, Shield
# lion_target = (9, 3, '3+', True)  # T9 3++
# angron_target = (11, 2, '4+', True)  # T11 4++

# # Weapons
# spear = (5, '2+', 7, -2, 'D2')
# axe = (4, '2+', 9, -1, 'D3')

# # EV approx manual
# print("EV vs SM:")
# print("Spear:", 5*(5/6)*(4/6)*(4/6)*2)
# print("Axe:", 4*(5/6)*(5/6)*(3/6)*2)

# print("\nEV vs Traj (4++ 50% unsaved, wound 4+ both Shield):")
# print("Spear:", 5*(5/6)*(3/6)*(3/6)*2)
# print("Axe:", 4*(5/6)*(3/6)*(3/6)*2)

# print("\nEV vs Lion (3++ 67% unsaved, wound 5+ both):")
# print("Spear:", 5*(5/6)*(2/6)*(4/6)*2)
# print("Axe:", 4*(5/6)*(2/6)*(4/6)*2)

# print("\nEV vs Angron (4++ 50%, wound 6+ both):")
# print("Spear:", 5*(5/6)*(1/6)*(3/6)*2)
# print("Axe:", 4*(5/6)*(1/6)*(3/6)*2)

# # Sim 10 activations each vs each target, seed for repro
# random.seed(42)
# print("\nSim 10 Spear vs SM:")
# spear_sm = [sim_single_activation(spear, sm_target) for _ in range(10)]
# print(spear_sm, "Avg:", np.mean(spear_sm), "Total:", sum(spear_sm))

# print("\nSim 10 Axe vs SM:")
# axe_sm = [sim_single_activation(axe, sm_target) for _ in range(10)]
# print(axe_sm, "Avg:", np.mean(axe_sm), "Total:", sum(axe_sm))

# random.seed(42)
# print("\nSim 10 Spear vs Traj:")
# spear_traj = [sim_single_activation(spear, traj_target) for _ in range(10)]
# print(spear_traj, "Avg:", np.mean(spear_traj), "Total:", sum(spear_traj))

# print("\nSim 10 Axe vs Traj:")
# axe_traj = [sim_single_activation(axe, traj_target) for _ in range(10)]
# print(axe_traj, "Avg:", np.mean(axe_traj), "Total:", sum(axe_traj))

# random.seed(42)
# print("\nSim 10 Spear vs Lion:")
# spear_lion = [sim_single_activation(spear, lion_target) for _ in range(10)]
# print(spear_lion, "Avg:", np.mean(spear_lion), "Total:", sum(spear_lion))

# print("\nSim 10 Axe vs Lion:")
# axe_lion = [sim_single_activation(axe, lion_target) for _ in range(10)]
# print(axe_lion, "Avg:", np.mean(axe_lion), "Total:", sum(axe_lion))

# random.seed(42)
# print("\nSim 10 Spear vs Angron:")
# spear_angron = [sim_single_activation(spear, angron_target) for _ in range(10)]
# print(spear_angron, "Avg:", np.mean(spear_angron), "Total:", sum(spear_angron))

# print("\nSim 10 Axe vs Angron:")
# axe_angron = [sim_single_activation(axe, angron_target) for _ in range(10)]
# print(axe_angron, "Avg:", np.mean(axe_angron), "Total:", sum(axe_angron))

# # For SM kills: assume W2 models, alloc to max kills: dmg//2 full kills + partial
# def expected_sm_kills(dmgs):
#     total_kills = 0
#     for d in dmgs:
#         kills = d // 2
#         total_kills += kills
#     return total_kills / len(dmgs)

# print("\nAvg SM kills Spear:", expected_sm_kills(spear_sm))
# print("Avg SM kills Axe:", expected_sm_kills(axe_sm))