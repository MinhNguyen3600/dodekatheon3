"""
Unit datasheets and faction ability definitions
"""

# ============================================
#               UNIT DATASHEETS
# ============================================

# ============================================
# NECRON UNITS
# ============================================

# NECRON CHARACTERS

nightbringer = {
    "Name": "C'tan Shard Of The Nightbringer",
    "Piece": "N",
    "Profile":{
        "m": 10,
        "t": 11,
        "sv": 3,
        "inv-sv": 4,
        "w": 16,
        "ld": 6,
        "oc": 4
    },
    "Weapons":
    [ 
        {
            "name": "Gaze of Death",
            "weapon abilities": ["BLAST", "HEAVY"],
            "range": 18,
            "a": "D3",
            "bs": 2,
            "s": 12,
            "ap": -3,
            "d": "D6+3"
        },
        {
            "name": "Scythe of the Nightbringer - strike",
            "weapon abilities": ["DEVASTATING WOUNDS"],
            "range": "Melee",
            "a": 6,
            "ws": 2,
            "s": 14,
            "ap": -4,
            "d": "D6+2"
        },
        {
            "name": "Scythe of the Nightbringer - sweep",
            "weapon abilities": [],
            "range": "Melee",
            "a": 14,
            "ws": 2,
            "s": 8,
            "ap": -2,
            "d": 2
        }
    ],
    "Faction Ability": "Reanimation Protocols",
    "Ability": {},
    "Feel No Pain": "5+",
    "Deadly Demise": "D6",
    "Model Count": 1,
    "Keyword": ["MONSTER", "CHARACTER", "EPIC HERO", "FLY", "C'TAN SHARD OF THE NIGHTBRINGER"]
}

void_dragon = {
    "Name": "C'tan Shard Of The Void Dragon",
    "Piece": "N",
    "Profile":{
        "m": 10,
        "t": 11,
        "sv": 3,
        "inv-sv": 4,
        "w": 16,
        "ld": 6,
        "oc": 4
    },
    "Weapons":
    [ 
        {
            "name": "Spear of the Void Dragon",
            "weapon abilities": ["BLAST", "HEAVY"],
            "range": 18,
            "a": "D3",
            "bs": 2,
            "s": 12,
            "ap": -3,
            "d": "D6+3"
        },
        {
            "name": "Spear of the Void Dragon - strike",
            "weapon abilities": ["ANTI-VEHICLE 2+"],
            "range": "Melee",
            "a": 5,
            "ws": 2,
            "s": 12,
            "ap": -4,
            "d": "D6+2"
        },
        {
            "name": "Spear of the Void Dragon - sweep",
            "weapon abilities": [],
            "range": "Melee",
            "a": 10,
            "ws": 2,
            "s": 8,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Spear of the Void Dragon - sweep",
            "weapon abilities": ["EXTRA ATTACKS"],
            "range": "Melee",
            "a": 10,
            "ws": 2,
            "s": 8,
            "ap": -1,
            "d": 2
        }
    ],
    "Faction Ability": "Reanimation Protocols",
    "Ability": {},
    "Feel No Pain": "5+",
    "Deadly Demise": "D6",
    "Model Count": 1,
    "Keyword": ["MONSTER", "CHARACTER", "EPIC HERO", "FLY", "C'TAN SHARD OF THE NIGHTBRINGER"]
}

ammentar = {
    "Name": "Nekrosor Ammentar",
    "Piece": "A",
    "Profile":{
        "m": 10,
        "t": 8,
        "sv": 3,
        "inv-sv": 4,
        "w": 9,
        "ld": 6,
        "oc": 3
    },
    "Weapons":
    [ 
        {
            "name": "Gaze of Death",
            "weapon abilities": ["IGNORES COVER", "PISTOL", "SUSTAINED HITS 2"],
            "range": 18,
            "a": 4,
            "bs": 2,
            "s": 6,
            "ap": -2,
            "d": 1
        },
        {
            "name": "Blade tail and whip coils",
            "weapon abilities": ["EXTRA ATTACKS"],
            "range": "Melee",
            "a": 6,
            "ws": 2,
            "s": 6,
            "ap": -1,
            "d": 1
        },
        {
            "name": "Unmaker Gauntlet",
            "weapon abilities": [],
            "range": "Melee",
            "a": 6,
            "ws": 2,
            "s": 10,
            "ap": -3,
            "d": 3
        }
    ],
    "Faction Ability": "Reanimation Protocols",
    "Ability": {},
    "Fights First": True,
    "Model Count": 1,
    "Keyword": ["INFANTRY", "CHARACTER", "EPIC HERO", "DESTROYER CULT", "NEKROSOR AMMENTAR"]
}

# NECRON SQUADS



# NECRON VEHICLES

doomsday_ark = {
    "Name": "Doomsday Ark",
    "Piece": "D",
    "Profile":{
        "m": 10,
        "t": 9,
        "sv": 3,
        "inv-sv": 4,
        "w": 14,
        "ld": 7,
        "oc": 5,
        "damaged_threshold": 5  # ✅ NEW: DAMAGED 1-5 WOUNDS (adjust as needed)
    },
    "Weapons":
    [ 
        {
            "name": "Doomsday Cannon",
            "weapon abilities": ["BLAST", "HEAVY"],
            "range": 72,
            "a": "D6+1",
            "bs": 3,
            "s": 18,
            "ap": -4,
            "d": 4
        },
        {
            "name": "Gauss Flayer Array",
            "weapon abilities": ["LETHAL HITS", "RAPID FIRE 5"],
            "range": 24,
            "a": 5,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Gauss Flayer Array",
            "weapon abilities": [],
            "range": "Melee",
            "a": 3,
            "ws": 4,
            "s": 6,
            "ap": 0,
            "d": 1
        }
    ],
    "Faction Ability": "Reanimation Protocols",
    "Ability": {
        "name": "Overwhelming Obliteration",
        "trigger": "start_of_shooting",
        "condition": "isStationary",
        "target": "weapon:Doomsday Cannon",
        "modifier": "gain",
        "keyword": "DEVASTATING WOUNDS",
        "duration": "this_phase"
    },
    "Deadly Demise": "D3", 
    "Model Count": 1,
    "Keyword": ["VEHICLE", "FLY", "DOOMSDAY ARK"]
}


# ============================================
# MONSTER UNITS
# ============================================

vashtorr = {
    "Name": "Vashtorr the Arkifane",
    "Piece": "V",
    "Profile":{
        "m": 12,
        "t": 10,
        "sv": 2,
        "inv-sv": 4,
        "w": 13,
        "ld": 6,
        "oc": 3
    },
    "Weapons":
    [ 
        {
            "name": "Vashtorr's claw",
            "weapon abilities": ["ANTI-VEHICLE 4+", "TORRENT"],
            "range": 12,
            "a": "D6",
            "bs": 0,
            "s": 5,
            "ap": -2,
            "d": 1
        },
        {
            "name": "Vashtorr's hammer - strike",
            "weapon abilities": ["ANTI-VEHICLE 4+", "DEVASTATING WOUNDS"],
            "range": "Melee",
            "a": 6,
            "ws": 2,
            "s": 14,
            "ap": -3,
            "d": 3
        },
        {
            "name": "Vashtorr's hammer - sweep",
            "weapon abilities": ["ANTI-VEHICLE 4+", "DEVASTATING WOUNDS"],
            "range": "Melee",
            "a": 12,
            "ws": 2,
            "s": 8,
            "ap": -1,
            "d": 2
        }
    ],
    "Faction Ability": "",
    "Ability": {
        "name": "Reorder Reality",
        "trigger": "on_defense",
        "condition": "attackerWithin18",
        "effects": [
            {
                "type": "modifyHit",
                "target": "attacker",
                "value": -1
            },
            {
                "type": "addWeaponAbility",
                "target": "attacker.rangedWeapons",
                "ability": "HAZARDOUS"
            }
        ],
        "duration": "this_phase",
        "description": "Each time an enemy unit within 18\" targets this model, subtract 1 from the Hit roll and that unit's ranged weapons gain [HAZARDOUS]."
    },
    "Deadly Demise": "D6", 
    "Model Count": 1,
    "Keyword": ["MONSTER", "CHARACTER", "EPIC HERO", "FLY", "CHAOS", "DAEMON", "VASHTORR THE ARKIFANE"]
}

angron = {
    "Name": "Angron",
    "Piece": "A",
    "Profile":{
        "m": 14,
        "t": 11,
        "sv": 2,
        "inv-sv": 4,
        "w": 16,
        "ld": 5,
        "oc": 6,
        "damaged_threshold": 6
    },
    "Weapons":
    [ 
        {
            "name": "Samni'arius and Spinegrinder - strike",
            "weapon abilities": ["DEVASTATING WOUNDS"],
            "range": "Melee",
            "a": 8,
            "ws": 2,
            "s": 14,
            "ap": -3,
            "d": "D6+2"
        },
        {
            "name": "Samn'arius and Spinegrinder - sweep",
            "weapon abilities": ["DEVASTATING WOUNDS"],
            "range": "Melee",
            "a": 16,
            "ws": 2,
            "s": 7,
            "ap": -2,
            "d": 2
        }
    ],
    "Faction Ability": "Blessings of Khorne",
    "Ability": {},
    "Deadly Demise": "D6",
    "Model Count": 1,
    "Keyword": ["MONSTER", "CHARACTER", "EPIC HERO", "FLY", "C'TAN SHARD OF THE NIGHTBRINGER"]
}

# ============================================
# SM SQUAD UNITS
# ============================================

terminator_squad = {
    "Name": "Terminator Squad",
    "Piece": "T",
    "Profile":{
        "m": 5,
        "t": 5,
        "sv": 2,
        "inv-sv": 4,
        "w": 3,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [ 
        {
            "name": "Storm bolter",
            "weapon abilities": ["RAPID FIRE 2"],
            "range": 24,
            "a": 2,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Chainfist",
            "weapon abilities": ["ANTI-VEHICLE 3+"],
            "range" : "Melee",
            "a": 3,
            "ws": 4,
            "s": 8,
            "ap": -2,
            "d": 2            
        },
        {
            "name": "Power Fist",
            "weapon abilities": [],
            "range" : "Melee",
            "a": 3,
            "ws": 3,
            "s": 8,
            "ap": -2,
            "d": 2            
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Fury of the First",
        "trigger": "on_attack",
        "condition": "isOathTarget",
        "target": "currentUnit.hitRolls",
        "modifier": "add",
        "value": 1,
        "exclude": [6]
    },
    "Model Count": 10,
    "Keyword":["INFANTRY", "IMPERIUM", "TERMINATOR", "TERMINATOR SQUAD"]
}

eradicators = {
    "Name": "Eradicator Squad",
    "Piece": "E",
    "Profile":{
        "m": 5,
        "t": 6,
        "sv": 3,
        "w": 3,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [
        {
            "name": "Bolt pistol",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 1,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Melta rifle",
            "weapon abilities": ["HEAVY","MELTA 2"],
            "range" : 18,
            "a": 3,
            "bs": 4,
            "s": 9,
            "ap": -4,
            "d": "D6"            
        },
        {
            "name": "Close combat weapon",
            "weapon abilities": [],
            "range" : "Melee",
            "a": 3,
            "ws": 3,
            "s": 4,
            "ap": 0,
            "d": 1          
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {},
    "Model Count": 3,
    "Keyword":["INFANTRY", "GRENADES", "IMPERIUM", "GRAVIS", "ERADICATOR SQUAD"]
}

eliminators = {
    "Name": "Eliminator Squad",
    "Piece": "E",
    "Profile":{
        "m": 6,
        "t": 4,
        "sv": 3,
        "w": 2,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [
        {
            "name": "Bolt pistol",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 1,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Las fusil",
            "weapon abilities": ["HEAVY"],
            "range" : 36,
            "a": 1,
            "bs": 3,
            "s": 9,
            "ap": -3,
            "d": "D6"            
        },
        {
            "name": "Bolt Sniper rifle",
            "weapon abilities": ["HEAVY", "PRECISION"],
            "range" : 36,
            "a": 1,
            "bs": 3,
            "s": 5,
            "ap": -2,
            "d": 3            
        },
        {
            "name": "Close combat weapon",
            "weapon abilities": [],
            "range" : "Melee",
            "a": 3,
            "ws": 3,
            "s": 4,
            "ap": 0,
            "d": 1          
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Mark the Target",
        "trigger": "start_of_shooting",
        "condition": "isStationary",
        "target": "weapon:Bolt Sniper rifle",
        "modifier": "gain",
        "keyword": "DEVASTATING WOUNDS",
        "duration": "this_phase"
    },
    "Model Count": 3,
    "Keyword":["INFANTRY", "GRENADES", "IMPERIUM", "PHOBOS", "ELIMINATOR SQUAD"]
}

heavy_ints = {
    "Name": "Heavy Intercessor Squad",
    "Piece": "H",
    "Profile":{
        "m": 5,
        "t": 6,
        "sv": 3,
        "w": 3,
        "ld": 6,
        "oc": 2
    },
    "Weapons":
    [
        {
            "name": "Bolt pistol",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 1,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Heavy bolt rifle",
            "weapon abilities": ["ASSAULT", "HEAVY"],
            "range" : 30,
            "a": 2,
            "bs": 3,
            "s": 5,
            "ap": -1,
            "d": 2            
        },
        {
            "name": "Close combat weapon",
            "weapon abilities": [],
            "range" : "Melee",
            "a": 3,
            "ws": 3,
            "s": 4,
            "ap": 0,
            "d": 1          
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {},
    "Model Count": 5,
    "Keyword":["INFANTRY", "BATTLELINE", "GRENADES", "IMPERIUM", "GRAVIS", "HEAVY INTERCESSOR SQUAD"]
}

# ============================================
# SM VEHICLES
# ============================================

repulsor_executioner = {
    "Name": "Repulsor Executioner",
    "Piece": "R",
    "Profile":{
        "m": 10,
        "t": 12,
        "sv": 3,
        "inv-sv": 7,  # No invuln (set to 7 so it's never used)
        "w": 16,
        "ld": 6,
        "oc": 5,
        "damaged_threshold": 5  # ✅ NEW: DAMAGED 1-5 WOUNDS
    },
    "Weapons":
    [ 
        {
            "name": "Heavy Laser Destroyer",
            "weapon abilities": ["HEAVY"],
            "range": 72,
            "a": 2,
            "bs": 3,
            "s": 16,
            "ap": -4,
            "d": "D6+4"
        },
        {
            "name": "Heavy onslaught gatling cannon",
            "weapon abilities": ["DEVASTATING WOUNDS"],
            "range": 24,
            "a": 12,
            "bs": 3,
            "s": 6,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Icarus rocket pod",
            "weapon abilities": ["ANTI-FLY 2+"],
            "range": 24,
            "a": "D3",
            "bs": 3,
            "s": 8,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Ironhail heavy stubber",
            "weapon abilities": ["RAPID FIRE 3"],
            "range": 36,
            "a": 3,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Twin heavy bolter",
            "weapon abilities": ["SUSTAINED HITS 1", "TWIN-LINKED"],
            "range": 36,
            "a": 3,
            "bs": 3,
            "s": 5,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Twin Icarus ironhail heavy stubber",
            "weapon abilities": ["ANTI-FLY 4+", "RAPID FIRE 3", "TWIN-LINKED"],
            "range": 36,
            "a": 3,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Armored Hull",
            "weapon abilities": [],
            "range": "Melee",
            "a": 6,
            "ws": 4,
            "s": 8,
            "ap": 0,
            "d": 1
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Executioner",
        "trigger": "on_attack",
        "condition": "targetBelowHalfStrength",
        "effects": [
            {
                "type": "modifyHit",
                "value": 1
            }
        ],
        "duration": "permanent",
        "description": "Each time this model makes an attack that targets a unit that is Below Half-strength, add 1 to the Hit roll."
    },
    "Deadly Demise": "D6",  # ✅ NEW: DEADLY DEMISE D6
    "Model Count": 1,
    "Keyword": ["VEHICLE", "SMOKE", "TRANSPORT", "IMPERIUM", "REPULSOR EXECUTIONER"]
}

bs_dread = {
    "Name": "Ballistus Dreadnought",
    "Piece": "R",
    "Profile":{
        "m": 8,
        "t": 10,
        "sv": 2,
        "inv-sv": 7,  # No invuln (set to 7 so it's never used)
        "w": 12,
        "ld": 6,
        "oc": 4,
        "damaged_threshold": 4  # NEW: DAMAGED 1-5 WOUNDS
    },
    "Weapons":
    [ 
        {
            "name": "Ballistus lascannon",
            "weapon abilities": [],
            "range": 48,
            "a": 2,
            "bs": 3,
            "s": 12,
            "ap": -3,
            "d": "D6+1"
        },
        {
            "name": "Ballistus missile launcher - krak",
            "weapon abilities": [],
            "range": 24,
            "a": 2,
            "bs": 3,
            "s": 10,
            "ap": -2,
            "d": "D6"
        },
        {
            "name": "Twin Storm bolter",
            "weapon abilities": ["RAPID FIRE 2", "TWIN-LINKED"],
            "range": 24,
            "a": 2,
            "bs": 3,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Armored Feet",
            "weapon abilities": [],
            "range": "Melee",
            "a": 5,
            "ws": 3,
            "s": 7,
            "ap": 0,
            "d": 1
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Executioner",
        "trigger": "on_attack",
        "condition": "targetBelowHalfStrength",
        "effects": [
            {
                "type": "modifyHit",
                "value": 1
            }
        ],
        "duration": "permanent",
        "description": "Each time this model makes an attack that targets a unit that is Below Half-strength, add 1 to the Hit roll."
    },
    "Deadly Demise": "D3",  # NEW: DEADLY DEMISE D6
    "Model Count": 1,
    "Keyword": ["VEHICLE", "SMOKE", "TRANSPORT", "IMPERIUM", "REPULSOR EXECUTIONER"]
}

# ============================================
# SM CHARACTER UNITS
# ============================================

lion = {
    "Name": "Lion el' Jonson",
    "Piece": "L",
    "Profile":{
        "m": 8,
        "t": 9,
        "sv": 2,
        "inv-sv": 3,
        "w": 10,
        "ld": 5,
        "oc": 4
    },
    "Weapons":
    [ 
        {
            "name": "Arma Luminis - plasma",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 2,
            "bs": 2,
            "s": 8,
            "ap": -3,
            "d": 2
        },
        {
            "name": "Arma Luminis - bolt",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 4,
            "bs": 2,
            "s": 4,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Fealty - strike",
            "weapon abilities": ["LETHAL HITS"],
            "range" : "Melee",
            "a": 8,
            "ws": 2,
            "s": 12,
            "ap": -4,
            "d": 4            
        },
        {
            "name": "Fealty - sweep",
            "weapon abilities": ["SUSTAINED HITS 1"],
            "range" : "Melee",
            "a": 16,
            "ws": 2,
            "s": 6,
            "ap": -3,
            "d": 2            
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Emperor's Shield",
        "trigger": "on_defense",
        "condition": "attackingWeapon.s > 9",
        "target": "attacker.woundRoll",
        "modifier": "subtract",
        "value": 1
    },
    "Fights First": True,
    "Model Count": 1,
    "Keyword":["MONSTER", "CHARACTER", "EPIC HERO", "IMPERIUM", "PRIMARCH", "LION EL' JONSON"]
}

cpt_titus = {
    "Name": "Captain Titus",
    "Piece": "T",
    "Profile":{
        "m": 6,
        "t": 4,
        "sv": 3,
        "inv-sv": 4,
        "w": 6,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [ 
        {
            "name": "Master-Crafted Bolter",
            "weapon abilities": ["ASSAULT", "HEAVY"],
            "range": 24,
            "a": 2,
            "bs": 2,
            "s": 4,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Boltpistol",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 1,
            "bs": 2,
            "s": 4,
            "ap": 0,
            "d": 1
        },
        {
            "name": "Master-Crafted Chainsword",
            "weapon abilities": ["ANTI-INFANTRY 2+"],
            "range": "Melee",
            "a": 8,
            "ws": 2,
            "s": 5,
            "ap": -1,
            "d": 2
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Honor of Ultramar",
        "trigger": "on_destruction_melee",
        "condition": "hasNotFoughtThisPhase",
        "effects": [
            {
                "type": "survivalRoll",
                "threshold": 2
            },
            {
                "type": "fightBack",
                "condition": "survivalSucceeded"
            },
            {
                "type": "conditional",
                "check": "killedEnemyModels",
                "if_true": {
                    "type": "healWounds",
                    "value": "D3"
                },
                "if_false": {
                    "type": "removeFromPlay"
                }
            }
        ],
        "duration": "instant",
        "description": "If destroyed by melee attack before fighting, roll D6: on 2+, fight back. If you kill enemy models, regain D3 wounds and survive; otherwise, removed from play."
    },
    "Feel No Pain": "5+",
    "Model Count": 1,
    "Keyword": ["INFANTRY", "CHARACTER", "EPIC HERO", "IMPERIUM", "TACTICUS", "GRENADES", "CAPTAIN", "TITUS"]
}

ba_cpt = {
    "Name": "Blood Angels Captain",
    "Piece": "B",
    "Profile":{
        "m": 6,
        "t": 4,
        "sv": 3,
        "inv-sv": 4,
        "w": 5,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [
        {
            "name": "Inferno pistol",
            "weapon abilities": ["PISTOL", "MELTA 2"],
            "range": 6,
            "a": 1,
            "bs": 2,
            "s": 8,
            "ap": -4,
            "d": "D3"
        },
        {
            "name": "Power Fist",
            "weapon abilities": [],
            "range": "Melee",
            "a": 5,
            "ws": 2,
            "s": 8,
            "ap": -2,
            "d": 2
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Finest Hour",
        "trigger": "start_of_fight",
        "condition": "notUsedThisBattle",
        "effects": [
            {
                "type": "modifyAttacks",
                "target": "meleeWeapons",
                "value": 3
            },
            {
                "type": "addWeaponAbility",
                "target": "meleeWeapons",
                "ability": "DEVASTATING WOUNDS"
            }
        ],
        "duration": "this_phase",
        "uses": 1,
        "player_choice": True,
        "description": "Once per battle, at the start of the Fight phase, add 3 to the Attacks characteristic of melee weapons and those weapons gain [DEVASTATING WOUNDS]."
    },  
    "Model Count": 1,
    "Keyword": ["INFANTRY", "CHARACTER", "GRENADES", "IMPERIUM", "TACTICUS", "CAPTAIN"]
}

sm_cpt = {
    "Name": "Captain",
    "Piece": "C",
    "Profile":{
        "m": 6,
        "t": 4,
        "sv": 3,
        "inv-sv": 4,
        "w": 5,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [
        {
            "name": "Master-Crafted Bolter",
            "weapon abilities": [],
            "range": 24,
            "a": 2,
            "bs": 2,
            "s": 4,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Heavy Bolt Pistol",
            "weapon abilities": ["PISTOL"],
            "range": 12,
            "a": 1,
            "bs": 2,
            "s": 4,
            "ap": -1,
            "d": 1
        },
        {
            "name": "Power Fist",
            "weapon abilities": [],
            "range": "Melee",
            "a": 5,
            "ws": 2,
            "s": 8,
            "ap": -2,
            "d": 2
        }
    ],
    "Faction Ability": "Oath of the Moment",
    "Ability": {
        "name": "Finest Hour",
        "trigger": "start_of_fight",
        "condition": "notUsedThisBattle",
        "effects": [
            {
                "type": "modifyAttacks",
                "target": "meleeWeapons",
                "value": 3
            },
            {
                "type": "addWeaponAbility",
                "target": "meleeWeapons",
                "ability": "DEVASTATING WOUNDS"
            }
        ],
        "duration": "this_phase",
        "uses": 1,
        "player_choice": True,
        "description": "Once per battle, at the start of the Fight phase, add 3 to the Attacks characteristic of melee weapons and those weapons gain [DEVASTATING WOUNDS]."
    },
    "Model Count": 1,
    "Keyword": ["INFANTRY", "CHARACTER", "GRENADES", "IMPERIUM", "TACTICUS", "CAPTAIN"]
}

#=============== ADEPTUS CUSTODES ================

# =========== CUSTODES CHARACTER UNITS ===========
trajann = {
    "Name": "Trajann Valoris",
    "Piece": "T",
    "Profile":{
        "m": 6,
        "t": 6,
        "sv": 2,
        "inv-sv": 4,
        "w": 7,
        "ld": 5,
        "oc": 2
    },
    "Weapons":
    [ 
        {
            "name": "Eagle's Scream",
            "weapon abilities": ["ASSAULT"],
            "range": 24,
            "a": 2,
            "bs": 2,
            "s": 5,
            "ap": -2,
            "d": 3
        },
        {
            "name": "Watcher's Axe",
            "weapon abilities": ["LETHAL HITS"],
            "range": "Melee",
            "a": 6,
            "ws": 2,
            "s": 10,
            "ap": -2,
            "d": 3
        }
    ],
    "Faction Ability": "Martial Ka'tah",
    "Ability": {
        "name": "Moment Shackle",
        "trigger": "start_of_fight",
        "condition": "notUsedThisBattle",
        "effects": [
            {
                "type": "chooseStance",
                "options": {
                    "attacks": {
                        "name": "Attacks Overdrive",
                        "type": "modifyAttacks",
                        "weapon": "Watcher's Axe",
                        "value": 12,
                        "operation": "set"
                    },
                    "invuln": {
                        "name": "Invulnerable Aegis",
                        "type": "changeInvuln",
                        "value": 2
                    }
                }
            }
        ],
        "duration": "this_phase",
        "uses": 1,
        "player_choice": True,
        "description": "Once per battle, at the start of the Fight phase, choose: Watcher's Axe has 12 Attacks OR model gains 2+ invulnerable save."
    },
    "Feel No Pain": "5+",
    "Model Count": 1,
    "Keyword": ["INFANTRY", "CHARACTER", "EPIC HERO", "IMPERIUM", "TRAJANN VALORIS"]
}

aleya = {
    "Name": "Aleya",
    "Piece": "A",
    "Profile":{
        "m": 6,
        "t": 3,
        "sv": 3,
        "inv-sv": 5,
        "w": 4,
        "ld": 6,
        "oc": 1
    },
    "Weapons":
    [ 
        {
            "name": "Somnus",
            "weapon abilities": ["DEVASTATING WOUNDS", "ANTI-PSYKER 5+"],
            "range" : "Melee",
            "a": 4,
            "ws": 2,
            "s": 6,
            "ap": -3,
            "d": 3            
        }
    ],
    "Faction Ability": "Martial Ka'tah",
    "Ability": {
        "name": "Deft Parry",
        "trigger": "on_defense",
        "condition": "isMeleeAttack",
        "effects": [
            {
                "type":"modifyHit",
                "target":"attacker",
                "value": -1
            }
        ],
        "duration":"permanent",
        "description": "Each time a melee attack targets this model, subtract 1 from the Hit roll."
    },
    "Model Count": 1,
    "Keyword":["INFANTRY", "CHARACTER", "EPIC HERO", "IMPERIUM", "ANATHEMA PSYKANA", "ALEYA"]
}

# ============= CUSTODES SQUAD UNITS =============
cust_guard = {

    "Name": "Custodian Guard",
    "Piece": "T",
    "Profile":{
        "m": 6,
        "t": 6,
        "sv": 2,
        "inv-sv": 4,
        "w": 3,
        "ld": 6,
        "oc": 2
    },
    "Weapons":
    [ 
        {
            "name": "Guardian spear",
            "weapon abilities": ["ASSAULT"],
            "range": 24,
            "a": 2,
            "bs": 2,
            "s": 4,
            "ap": -1,
            "d": 2
        },
        {
            "name": "Guardian spear",
            "weapon abilities": ["LETHAL HITS"],
            "range": "Melee",
            "a": 5,
            "ws": 2,
            "s": 7,
            "ap": -2,
            "d": 2
        }
    ],
    "Faction Ability": "",
    "Ability": {
        "name": "Stand Vigil",
        "trigger": "on_wound_roll",
        "condition": "always",
        "effects": [
            {
                "type": "rerollWounds",
                "value": "1s"
            }
        ],
        "duration": "permanent",
        "description": "Each time a model in this unit makes an attack, re-roll a Wound roll of 1."
    },
    "Secondary Ability": {
        "name": "Sentinel Storm",
        "trigger": "after_shooting",
        "condition": "notUsedThisBattle",
        "effects": [
            {
                "type": "shootAgain",
            }
        ],
        "duration":"instant",
        "player_choice" : True,
        "description": "Once per battle, after this unit has shot, it can shoot again."
    },
    "Model Count": 5,
    "Keyword": ["INFANTRY", "BATTLELINE", "IMPERIUM", "CUSTODIAN GUARD"]
}


# ============================================
#               FACTION ABILITIES
# ============================================

FACTION_ABILITIES = {
    "Oath of the Moment": {
        "name": "Oath of the Moment",
        "trigger": "start_of_command",
        "condition": "always",
        "effects": [
            {
                "type": "selectOathTarget",
                "description": "Select one enemy unit as Oath target"
            },
            {
                "type": "rerollHits",
                "condition": "isOathTarget",
                "value": "all"
            },
            {
                "type": "modifyWound",
                "condition": "isOathTarget",
                "value": 1
            }
        ],
        "duration": "this_turn",
        "description": "At the start of your Command phase, select one enemy unit as your Oath target. Until the start of your next Command phase, when targeting that unit: re-roll hit rolls, and improve wound rolls by 1."
    },
    "Reanimation Protocols": {
        "name": "Reanimation Protocols",
        "trigger": "end_of_command",
        "condition": "always",
        "effects": [
            {
                "type": "healWounds",
                "value": "D3",
            },
            {
                "type": "returnModel",
                "condition": "unitBelowStartingStrength"
            }
        ]
    },
    "Martial Ka'tah": {
        "name": "Martial Ka'tah",
        "trigger": "before_fight",
        "condition": "always",
        "effects": [
            {
                "type": "chooseStance",
                "options": {
                    "dacatarai": {
                        "name": "Dacatarai Stance",
                        "type": "addWeaponAbility",
                        "target": "meleeWeapons",
                        "ability": "SUSTAINED HITS 1"
                    },
                    "rendax": {
                        "name": "Rendax Stance",
                        "type": "addWeaponAbility",
                        "target": "meleeWeapons",
                        "ability": "LETHAL HITS"
                    }
                }
            }
        ],
        "duration": "until_attacks_complete",
        "player_choice": True,
        "description": "Each time this unit is selected to fight, select one Ka'tah Stance. Until that unit has finished making its attacks, melee weapons gain the selected ability."
    },
    "Blessings of Khorne": {
        "name": "Blessings of Khorne",
        "trigger": "start_of_battle_round",
        "condition": "always",
        "scope": "army_wide",  # Applies to all units with this faction ability
        "player_choice": True,
        "description": (
            "At the start of each battle round, roll eight D6. "
            "You can use these dice to activate up to two Blessings. "
            "Each can only be activated once per battle round."
        ),
        "effects": [
            {
                "type": "rollResourcePool",
                "count": 8,
                "dice_type": "D6",
                "store_as": "khorne_blessings_pool"
            },
            {
                "type": "selectResourceOptions",
                "resource_pool": "khorne_blessings_pool",
                "max_selections": 2,
                "once_per_round": True,
                "options": {
                    "unbridled_bloodlust": {
                        "name": "Unbridled Bloodlust",
                        "description": "You can re-roll Charge rolls made for this unit.",
                        "requires": {
                            "type": "double",
                            "value": 1  # (1,1)+
                        },
                        "effects": [
                            {
                                "type": "rerollCharges",
                                "value": "all"
                            }
                        ]
                    },
                    "rage_fuelled_invigoration": {
                        "name": "Rage-Fuelled Invigoration",
                        "description": "Pile-in/Consolidation moves are 6\" instead of 3\".",
                        "requires": {
                            "type": "double",
                            "value": 2  # (2,2)+
                        },
                        "effects": [
                            {
                                "type": "modifyMovement",
                                "movement_type": "pile_in",
                                "value": 6,
                                "operation": "set"
                            },
                            {
                                "type": "modifyMovement",
                                "movement_type": "consolidation",
                                "value": 6,
                                "operation": "set"
                            }
                        ]
                    },
                    "total_carnage": {
                        "name": "Total Carnage",
                        "description": "When destroyed by melee before fighting, roll D6: on 4+, can fight back then removed.",
                        "requires": {
                            "type": "double",
                            "value": 3  # (3,3)+
                        },
                        "effects": [
                            {
                                "type": "fightOnDeath",
                                "threshold": 4,
                                "condition": "destroyed_by_melee_before_fighting"
                            }
                        ]
                    },
                    "martial_excellence": {
                        "name": "Martial Excellence",
                        "description": "Melee weapons gain [SUSTAINED HITS 1].",
                        "requires": {
                            "type": "double",
                            "value": 3  # (3,3)+
                        },
                        "alt_requires": {  # ✅ OR condition
                            "type": "triple",
                            "value": 1  # (1,1,1)+
                        },
                        "effects": [
                            {
                                "type": "addWeaponAbility",
                                "target": "meleeWeapons",
                                "ability": "SUSTAINED HITS 1"
                            }
                        ]
                    },
                    "warp_blades": {
                        "name": "Warp Blades",
                        "description": "Melee weapons gain [LETHAL HITS].",
                        "requires": {
                            "type": "double",
                            "value": 5  # (5,5)+
                        },
                        "alt_requires": {  # ✅ OR condition
                            "type": "triple",
                            "value": 2  # (2,2,2)+
                        },
                        "effects": [
                            {
                                "type": "addWeaponAbility",
                                "target": "meleeWeapons",
                                "ability": "LETHAL HITS"
                            }
                        ]
                    },
                    "decapitating_strikes": {
                        "name": "Decapitating Strikes",
                        "description": "Melee attacks vs INFANTRY gain [DEVASTATING WOUNDS].",
                        "requires": {
                            "type": "double",
                            "value": 6  # (6,6)+
                        },
                        "alt_requires": {  # ✅ OR condition
                            "type": "triple",
                            "value": 3  # (3,3,3)+
                        },
                        "effects": [
                            {
                                "type": "addWeaponAbility",
                                "target": "meleeWeapons",
                                "ability": "DEVASTATING WOUNDS",
                                "condition": "targetHasKeyword:INFANTRY"  # Conditional
                            }
                        ]
                    }
                }
            }
        ],
        "duration": "this_battle_round"
    }


}