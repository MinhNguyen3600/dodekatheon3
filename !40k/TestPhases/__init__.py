"""
TestPhases package - Modular 40K game phase implementations
"""

# Import all functions and data to maintain backward compatibility
from .datasheets import *
from .utilityFunctions import *
from .commandPhase import *
from .movementPhase import *
from .shootingPhase import *
from .chargePhase import *  
from .fightPhase import *   

__all__ = [
    # Datasheets
    'doomsday_ark', 'terminator_squad', 'lion', 'aleya',
    'FACTION_ABILITIES',
    
    # Utility functions
    'rollD6', 'rollD3', 'parseDiceNotation', 'dataLoad',
    
    # Command phase
    'commandPhase',
    
    # Movement phase
    'generateMap', 'mapInit', 'displayMap', 'movePhase',
    
    # Shooting phase
    'getRangedWeapons', 'selectWeapon', 'getAttackCount',
    'hitRollPhase', 'woundRollPhase', 'saveRollPhase',
    'allocateDamage', 'shootingPhase', 'getDamageValue',
    
    # Charge phase
    'chargePhase', 'isChargeEligible', 'makeChargeRoll', 'canDeclareCharge',
    
    # Fight phase
    'fightPhase', 'getMeleeWeapons', 'selectMeleeWeapon', 'resolveMeleeAttacks'
]