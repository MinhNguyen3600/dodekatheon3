from numpy import random as rand
import weaponAbilityDict as weaponAbilityDict
import testPhases as testPhases
import rolls as rolls

# Test control Unit dict
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
        "oc": 5
    },
    "Weapons":
    [ 
        {
            "name": "Doomsday Cannon",
            "weapon abilities": ["BLAST", "HEAVY"],
            "range": 72,
            "a": "D6 + 1",
            "bs": 3,
            "s": 18,
            "ap": 4,
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
        }
    ],
    "Faction Ability": "Reanimation Protocols",
    #Unit Ability modified by Claude
    "Ability": {
        "name": "Overwhelming Obliteration",
        "trigger": "start_of_shooting",  # NEW
        "condition": "isStationary",
        "target": "weapon:Doomsday Cannon",  # FIXED - specify weapon
        "modifier": "gain",
        "keyword": "DEVASTATING WOUNDS",
        "duration": "this_phase"
    },
    "Model Count": 1,
    "Keyword":["VEHICLE", "FLY", "DOOMSDAY ARK"]
}

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
            "range": "Melee",
            "a": 3,
            "bs": 4,
            "s": 8,
            "ap": -2,
            "d": 2            
        }

    ],
    "Faction Ability": "Oath of the Moment",
    #Unit Ability modified by Claude
    "Ability": {
        "name": "Fury of the First",  # FIXED typo
        "trigger": "on_attack",  # NEW
        "condition": "isOathTarget",
        "target": "currentUnit.hitRolls",
        "modifier": "add",
        "value": 1,
        "exclude": [6]  # Explicit exclusion
    },
    "Model Count": 10,
    "Keyword":["INFANTRY", "IMPERIUM", "TERMINATOR", "TERMINATOR SQUAD"]

}

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
            "ap": 3,
            "d": 2
        },
        {
            "name": "Fealty - strike",
            "weapon abilities": ["LETHAL HITS"],
            "range": "Melee",
            "a": 8,
            "bs": 2,
            "s": 12,
            "ap": 4,
            "d": 4            
        }

    ],
    "Faction Ability": "Oath of the Moment",
    #Unit Ability modified by Claude
    "Ability": {
        "name": "Emperor's Shield",
        "trigger": "on_defense",  # NEW
        "condition": "attackingWeapon.s > 9",  # FIXED (was "S >= 8")
        "target": "attacker.woundRoll",  # More explicit
        "modifier": "subtract",
        "value": 1  # Explicit value
    },
    "Model Count": 1,
    "Keyword":["MONSTER", "CHARACTER", "EPIC HERO", "IMPERIUM", "PRIMARCH", "LION EL' JONSON"]
}

# --------------- PERSONALLY WRITTEN ---------------------
"Faction Ability Index" = {
    "oom":{
        "name": "Oath of the Moment",
        "faction": "Space Marines",
        "condition": "isOathTarget",
        "action": "reroll",
        "changes": "hit rolls",
        "special condition":{
            "condition": 'cuKeywords not in ["BLACK TEMPLARS", "SPACE WOLVES"]',
            "action": "add",
            "changes": "[rolls += 1 for rolls in woundRoll if woundRoll != 6]"
        }
    },
    "reanim protocols": {
        "name": "Reanimation Protcols",
        "faction": "Necrons",
        "condition": "startTurn and currentModelWounds != modelWounds",
        "action": "currentModelWounds += rollD3()",
        "special condition":{
            "condition": "modelsRemaining != targetModelCount and modelsRemaining != 0 and targetModelCount != 1",
            "action": "return model",
            "changes": "modelsRemaining += 1 and currentModelWounds = 1" #a previously destroyed model is returned to the unit, with 1 wound remaining
        }
    }
}


# ------------------- CLAUDE IMPROVEMENT --------------------
"oom"= {
    "condition": "isOathTarget",
    "effects": [
        {
            "type": "reroll",
            "target": "hitRolls"
        },
        {
            "condition": 'cuKeywords not in ["BLACK TEMPLARS", "SPACE WOLVES"]',
            "type": "modify",
            "target": "woundRolls",
            "modifier": "+1",
            "exclude": [6]  # Don't modify natural 6s
        }
    ]
}
"reanim protocols"= {
    "timing": "startOfTurn",
    "phases": [
        {
            "phase": "heal",
            "condition": "currentModelWounds < modelWounds",
            "action": "currentModelWounds += rollD3()"
        },
        {
            "phase": "resurrect",
            "condition": "modelsDestroyed > 0 and modelsRemaining > 0 and targetModelCount > 1",
            "action": "returnModel(wounds=1)"
        }
    ]
}

# Test target unit dict


# weaponAtks = 5
# weaponAbilityModifier = 5

# hitRoll = rolls.rollBox(weaponAtks)

# print(weaponAbilityDict.rapidFire(12, 24, hitRoll, weaponAbilityModifier))

