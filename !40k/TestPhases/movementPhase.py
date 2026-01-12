"""
Movement Phase implementation - Map, movement, positioning with Advance
"""
import random


def generateMap():
    """Generate a 30-space 1D battlefield"""
    mapList = ["o" for i in range(30)]
    return mapList


def mapInit(cuPiece: str, tuPiece: str):
    """Initialize map with units at starting positions"""
    gameMap = generateMap()
    cuPos = 29
    tuPos = 0
    
    gameMap[cuPos] = cuPiece
    gameMap[tuPos] = tuPiece
    
    return gameMap, cuPos, tuPos


def displayMap(currMap: list, cuPos: int, tuPos: int):
    """Display the map with position indicators"""
    print("\n" + "=" * 32)
    print("".join(currMap))
    print(f"Target Unit Position: {tuPos} | Control Unit Position: {cuPos}")
    print(f"Distance between units: {cuPos - tuPos}")
    print("=" * 32 + "\n")


def rollD6():
    """Roll a D6"""
    return random.randint(1, 6)


def movePhase(cuMove: int, tuMove: int, currMap: list, cuPos: int, tuPos: int, cuPiece: str, tuPiece: str):
    """
    Movement phase handler with Advance option
    
    Returns: (updated map, new CU position, new TU position, is_stationary, did_advance)
    """
    
    print(f"\n--- MOVE PHASE ---")
    print(f"Control Unit Move characteristic: {cuMove}\"")
    print(f"Target Unit will automatically move {tuMove} spaces")
    
    displayMap(currMap, cuPos, tuPos)
    
    # Movement type selection
    print("\nControl Unit Movement Options:")
    print("1. Remain Stationary (0\" movement)")
    print("2. Normal Move (up to M\")")
    print("3. Advance (M\" + D6\")")
    
    while True:
        try:
            movement_choice = int(input("Choose movement type (1-3): "))
            if 1 <= movement_choice <= 3:
                break
            else:
                print("Please enter 1, 2, or 3")
        except ValueError:
            print("INPUT NOT AN INTEGER! Please try again.")
    
    # Initialize movement state flags
    is_stationary = False
    did_advance = False
    actual_move_distance = 0
    max_movement = cuMove
    
    # Handle movement based on choice
    if movement_choice == 1:
        # Remain Stationary
        is_stationary = True
        actual_move_distance = 0
        max_movement = 0
        print(f"\n✓ Control Unit REMAINS STATIONARY")
        print("  • HEAVY weapons gain +1 to Hit")
        print("  • Can shoot and charge normally")
        
    elif movement_choice == 2:
        # Normal Move
        print(f"\n✓ Control Unit performs NORMAL MOVE (up to {cuMove}\")")
        while True:
            try:
                actual_move_distance = int(input(f"Move Control Unit forward (0-{cuMove}): "))
                if 0 <= actual_move_distance <= cuMove:
                    # Auto-detect if they chose 0 movement
                    if actual_move_distance == 0:
                        is_stationary = True
                        print("  • Moved 0\", counted as STATIONARY")
                        print("  • HEAVY weapons gain +1 to Hit")
                    break
                else:
                    print(f"Please enter a value between 0 and {cuMove}")
            except ValueError:
                print("INPUT NOT AN INTEGER! Please try again.")
                
    elif movement_choice == 3:
        # Advance
        did_advance = True
        advance_roll = rollD6()
        max_movement = cuMove + advance_roll
        
        print(f"\n✓ Control Unit ADVANCES!")
        print(f"  • Base Movement: {cuMove}\"")
        print(f"  • Advance Roll: {advance_roll}\" (D6)")
        print(f"  • Total Available: {max_movement}\"")
        print(f"  • Cannot shoot (unless ASSAULT weapons)")
        print(f"  • Cannot charge this turn")
        
        while True:
            try:
                actual_move_distance = int(input(f"Move Control Unit forward (0-{max_movement}): "))
                if 0 <= actual_move_distance <= max_movement:
                    break
                else:
                    print(f"Please enter a value between 0 and {max_movement}")
            except ValueError:
                print("INPUT NOT AN INTEGER! Please try again.")
    
    # Clear old positions
    currMap[cuPos] = "o"
    currMap[tuPos] = "o"
    
    # Calculate new positions
    newCuPos = cuPos - actual_move_distance
    newTuPos = tuPos + tuMove
    
    # Check for collision/engagement
    if newTuPos >= newCuPos:
        print("\n!!! UNITS ARE NOW IN ENGAGEMENT RANGE !!!")
        newTuPos = newCuPos - 1
        if newTuPos < 0:
            newTuPos = 0
            newCuPos = 1
    
    # Update map
    currMap[newCuPos] = cuPiece
    currMap[newTuPos] = tuPiece
    
    # Display movement summary
    print(f"\n--- Movement Summary ---")
    print(f"Control Unit moved {actual_move_distance}\" forward")
    print(f"Target Unit moved {tuMove}\" forward")
    
    if is_stationary:
        print(f"Status: ⏸️ STATIONARY (HEAVY +1 to Hit)")
    elif did_advance:
        print(f"Status: 🏃 ADVANCED (Cannot shoot non-ASSAULT/Cannot charge)")
    else:
        print(f"Status: 🚶 NORMAL MOVE")
    
    displayMap(currMap, newCuPos, newTuPos)
    
    return currMap, newCuPos, newTuPos, is_stationary, did_advance
