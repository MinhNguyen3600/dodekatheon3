"""
Complete Test Suite for 40K Weapon Abilities
Tests all implemented weapon abilities with known inputs/outputs
"""

import testPhases as tp
import rolls as rolls

# Override rolls for deterministic testing
class MockRolls:
    def __init__(self, sequence):
        self.sequence = sequence
        self.index = 0
    
    def rollBox(self, count):
        results = []
        for _ in range(count):
            if self.index < len(self.sequence):
                results.append(self.sequence[self.index])
                self.index += 1
            else:
                results.append(4)  # Default to 4
        return results
    
    def reset(self):
        self.index = 0

# Test results tracker
test_results = {
    "passed": 0,
    "failed": 0,
    "tests": []
}

def assert_equal(test_name, expected, actual, description=""):
    """Assert that expected equals actual"""
    if expected == actual:
        print(f"✅ PASS: {test_name}")
        if description:
            print(f"   {description}")
        test_results["passed"] += 1
        test_results["tests"].append((test_name, True))
        return True
    else:
        print(f"❌ FAIL: {test_name}")
        print(f"   Expected: {expected}")
        print(f"   Got: {actual}")
        if description:
            print(f"   {description}")
        test_results["failed"] += 1
        test_results["tests"].append((test_name, False))
        return False

def print_test_header(test_name):
    """Print a formatted test header"""
    print("\n" + "="*70)
    print(f"TEST: {test_name}")
    print("="*70)

def print_test_summary():
    """Print final test summary"""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {test_results['passed'] + test_results['failed']}")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    
    if test_results['failed'] > 0:
        print("\nFailed Tests:")
        for test_name, passed in test_results['tests']:
            if not passed:
                print(f"  • {test_name}")
    
    print("="*70)


# ============================================
# TEST 1: RAPID FIRE
# ============================================
def test_rapid_fire():
    print_test_header("RAPID FIRE X - Increases Attacks Within Half Range")
    
    # Setup: Storm bolter has RAPID FIRE 2, 2 attacks base, 24" range
    weapon = {
        "name": "Storm bolter",
        "weapon abilities": ["RAPID FIRE 2"],
        "range": 24,
        "a": 2,
        "bs": 3,
        "s": 4,
        "ap": 0,
        "d": 1
    }
    
    # Test at 12" (within half range) - should add 2 attacks
    print("\n--- Test 1A: Within Half Range (12\") ---")
    attacks = tp.getAttackCount(weapon, 12, 24, 10, False)
    assert_equal("RAPID FIRE within half range", 4, attacks, 
                 "2 base + 2 from RAPID FIRE = 4")
    
    # Test at 20" (beyond half range) - should NOT add attacks
    print("\n--- Test 1B: Beyond Half Range (20\") ---")
    attacks = tp.getAttackCount(weapon, 20, 24, 10, False)
    assert_equal("RAPID FIRE beyond half range", 2, attacks,
                 "2 base, no RAPID FIRE bonus")


# ============================================
# TEST 2: BLAST
# ============================================
def test_blast():
    print_test_header("BLAST - Add 1 Attack Per 5 Models")
    
    weapon = {
        "name": "Doomsday Cannon",
        "weapon abilities": ["BLAST"],
        "range": 72,
        "a": 3,
        "bs": 3,
        "s": 18,
        "ap": 4,
        "d": 4
    }
    
    # Test against 20 models - should add 4 attacks (20//5 = 4)
    print("\n--- Test 2A: 20 Models in Target Unit ---")
    attacks = tp.getAttackCount(weapon, 36, 72, 20, False)
    assert_equal("BLAST vs 20 models", 7, attacks,
                 "3 base + 4 from BLAST = 7")
    
    # Test against 4 models - should add 0 attacks (4//5 = 0)
    print("\n--- Test 2B: 4 Models in Target Unit ---")
    attacks = tp.getAttackCount(weapon, 36, 72, 4, False)
    assert_equal("BLAST vs 4 models", 3, attacks,
                 "3 base + 0 from BLAST = 3")
    
    # Test in engagement range - should return 0 (cannot shoot)
    print("\n--- Test 2C: Target in Engagement Range ---")
    attacks = tp.getAttackCount(weapon, 1, 72, 20, True)
    assert_equal("BLAST in engagement", 0, attacks,
                 "Cannot use BLAST in engagement range")


# ============================================
# TEST 3: HEAVY
# ============================================
def test_heavy():
    print_test_header("HEAVY - Add 1 to Hit if Stationary")
    
    weapon = {
        "name": "Doomsday Cannon",
        "weapon abilities": ["HEAVY"],
        "range": 72,
        "a": 3,
        "bs": 3,
        "s": 18,
        "ap": 4,
        "d": 4
    }
    
    # Mock rolls: [3, 2, 5] - normally only 3 and 5 hit (BS 3+)
    # With HEAVY (+1): all three should hit (2+1=3, 3+1=4, 5+1=6)
    print("\n--- Test 3A: Stationary (Should Get +1) ---")
    print("Rolls will be: [3, 2, 5]")
    print("Without HEAVY: 2 hits (3 and 5)")
    print("With HEAVY: 3 hits (all modified to 3+)")
    
    # Note: This requires integration testing with actual hit rolls
    # For now, we test the modifier function
    import weaponAbilityDict as wad
    mods = wad.getHitModifiers(["HEAVY"], isStationary=True, didAdvance=False)
    assert_equal("HEAVY when stationary", 1, mods["modifier"],
                 "+1 to hit rolls")
    
    print("\n--- Test 3B: Not Stationary (No Bonus) ---")
    mods = wad.getHitModifiers(["HEAVY"], isStationary=False, didAdvance=False)
    assert_equal("HEAVY when moving", 0, mods["modifier"],
                 "No bonus when not stationary")


# ============================================
# TEST 4: LETHAL HITS
# ============================================
def test_lethal_hits():
    print_test_header("LETHAL HITS - Critical Hits Auto-Wound")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 4A: Unmodified 6 (Should Auto-Wound) ---")
    is_lethal = wad.isLethalHits(6, ["LETHAL HITS"])
    assert_equal("LETHAL HITS on 6", True, is_lethal,
                 "Unmodified 6 triggers LETHAL HITS")
    
    print("\n--- Test 4B: Modified 6 (Should NOT Auto-Wound) ---")
    is_lethal = wad.isLethalHits(5, ["LETHAL HITS"])
    assert_equal("LETHAL HITS on 5", False, is_lethal,
                 "Only unmodified 6 triggers LETHAL HITS")
    
    print("\n--- Test 4C: Without LETHAL HITS Ability ---")
    is_lethal = wad.isLethalHits(6, [])
    assert_equal("No LETHAL HITS ability", False, is_lethal,
                 "Ability must be present to trigger")


# ============================================
# TEST 5: ANTI-X Y+
# ============================================
def test_anti():
    print_test_header("ANTI-X Y+ - Critical Wounds vs Keywords")
    
    import weaponAbilityDict as wad
    
    weapon_abilities = ["ANTI-VEHICLE 4+"]
    target_keywords = ["VEHICLE", "FLY"]
    
    print("\n--- Test 5A: Has Matching Keyword ---")
    has_anti, threshold = wad.hasAntiAbility(weapon_abilities, target_keywords)
    assert_equal("ANTI-VEHICLE applies", True, has_anti,
                 "Target has VEHICLE keyword")
    assert_equal("ANTI-VEHICLE threshold", 4, threshold,
                 "Critical wounds on 4+")
    
    print("\n--- Test 5B: No Matching Keyword ---")
    non_vehicle_keywords = ["INFANTRY", "IMPERIUM"]
    has_anti, threshold = wad.hasAntiAbility(weapon_abilities, non_vehicle_keywords)
    assert_equal("ANTI-VEHICLE doesn't apply", False, has_anti,
                 "Target lacks VEHICLE keyword")
    
    print("\n--- Test 5C: Check Critical Wound on 4 ---")
    is_crit = wad.checkCriticalWound(4, weapon_abilities, target_keywords)
    assert_equal("Wound roll of 4 is critical", True, is_crit,
                 "ANTI-VEHICLE 4+ makes 4 a critical wound")
    
    print("\n--- Test 5D: Check Critical Wound on 3 ---")
    is_crit = wad.checkCriticalWound(3, weapon_abilities, target_keywords)
    assert_equal("Wound roll of 3 not critical", False, is_crit,
                 "Below threshold, not a critical")


# ============================================
# TEST 6: DEVASTATING WOUNDS
# ============================================
def test_devastating_wounds():
    print_test_header("DEVASTATING WOUNDS - Mortal Damage on Crits")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 6A: Has DEVASTATING WOUNDS ---")
    has_dev = wad.checkDevastatingWounds(["DEVASTATING WOUNDS"])
    assert_equal("Has DEVASTATING WOUNDS", True, has_dev)
    
    print("\n--- Test 6B: No DEVASTATING WOUNDS ---")
    has_dev = wad.checkDevastatingWounds(["LETHAL HITS"])
    assert_equal("No DEVASTATING WOUNDS", False, has_dev)


# ============================================
# TEST 7: MELTA
# ============================================
def test_melta():
    print_test_header("MELTA X - Extra Damage Within Half Range")
    
    import weaponAbilityDict as wad
    
    weapon_abilities = ["MELTA 2"]
    
    print("\n--- Test 7A: Within Half Range ---")
    damage = wad.applyMelta(3, 12, 24, weapon_abilities)
    assert_equal("MELTA within half range", 5, damage,
                 "3 base + 2 from MELTA = 5")
    
    print("\n--- Test 7B: Beyond Half Range ---")
    damage = wad.applyMelta(3, 20, 24, weapon_abilities)
    assert_equal("MELTA beyond half range", 3, damage,
                 "No MELTA bonus beyond half range")


# ============================================
# TEST 8: TWIN-LINKED
# ============================================
def test_twin_linked():
    print_test_header("TWIN-LINKED - Re-roll Wound Rolls")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 8A: Has TWIN-LINKED ---")
    can_reroll = wad.canRerollWound(["TWIN-LINKED"])
    assert_equal("Has TWIN-LINKED", True, can_reroll)
    
    print("\n--- Test 8B: No TWIN-LINKED ---")
    can_reroll = wad.canRerollWound(["LETHAL HITS"])
    assert_equal("No TWIN-LINKED", False, can_reroll)


# ============================================
# TEST 9: TORRENT
# ============================================
def test_torrent():
    print_test_header("TORRENT - Auto-Hit")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 9A: Has TORRENT ---")
    mods = wad.getHitModifiers(["TORRENT"], False, False)
    assert_equal("TORRENT auto-hits", True, mods["autoHit"])
    
    print("\n--- Test 9B: No TORRENT ---")
    mods = wad.getHitModifiers(["LETHAL HITS"], False, False)
    assert_equal("No auto-hit", False, mods["autoHit"])


# ============================================
# TEST 10: ASSAULT
# ============================================
def test_assault():
    print_test_header("ASSAULT - Shoot After Advancing")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 10A: Advanced with ASSAULT ---")
    mods = wad.getHitModifiers(["ASSAULT"], False, True)
    assert_equal("Can shoot with ASSAULT", True, mods["canShoot"],
                 "ASSAULT allows shooting after advancing")
    
    print("\n--- Test 10B: Advanced without ASSAULT ---")
    mods = wad.getHitModifiers([], False, True)
    assert_equal("Cannot shoot without ASSAULT", False, mods["canShoot"],
                 "Cannot shoot after advancing without ASSAULT")


# ============================================
# TEST 11: LANCE
# ============================================
def test_lance():
    print_test_header("LANCE - +1 to Wound After Charging")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 11A: Charged with LANCE ---")
    modifier = wad.getWoundModifiers(["LANCE"], didCharge=True)
    assert_equal("LANCE after charge", 1, modifier,
                 "+1 to wound rolls")
    
    print("\n--- Test 11B: Did Not Charge ---")
    modifier = wad.getWoundModifiers(["LANCE"], didCharge=False)
    assert_equal("No LANCE without charge", 0, modifier,
                 "No bonus if didn't charge")


# ============================================
# TEST 12: IGNORES COVER
# ============================================
def test_ignores_cover():
    print_test_header("IGNORES COVER - Target Loses Cover Bonus")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 12A: Has IGNORES COVER ---")
    has_cover = wad.targetHasCover(True, ["IGNORES COVER"])
    assert_equal("Ignores cover", False, has_cover,
                 "Target loses cover benefit")
    
    print("\n--- Test 12B: No IGNORES COVER ---")
    has_cover = wad.targetHasCover(True, [])
    assert_equal("Normal cover", True, has_cover,
                 "Target keeps cover benefit")


# ============================================
# TEST 13: PISTOL
# ============================================
def test_pistol():
    print_test_header("PISTOL - Shoot in Engagement Range")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 13A: Is Pistol ---")
    is_pistol = wad.isPistol(["PISTOL"])
    assert_equal("Is PISTOL weapon", True, is_pistol)
    
    print("\n--- Test 13B: Not Pistol ---")
    is_pistol = wad.isPistol(["RAPID FIRE 2"])
    assert_equal("Not PISTOL weapon", False, is_pistol)


# ============================================
# TEST 14: INDIRECT FIRE
# ============================================
def test_indirect_fire():
    print_test_header("INDIRECT FIRE - Target Non-Visible Units")
    
    import weaponAbilityDict as wad
    
    print("\n--- Test 14A: Target Not Visible ---")
    penalty = wad.getIndirectFirePenalty(False, ["INDIRECT FIRE"])
    assert_equal("INDIRECT FIRE hit penalty", -1, penalty["hitModifier"],
                 "-1 to hit")
    assert_equal("INDIRECT FIRE cover", True, penalty["targetHasCover"],
                 "Target gets cover")
    assert_equal("INDIRECT FIRE min roll", 4, penalty["minHitRoll"],
                 "1-3 always fails")
    
    print("\n--- Test 14B: Target Visible ---")
    penalty = wad.getIndirectFirePenalty(True, ["INDIRECT FIRE"])
    assert_equal("No penalty when visible", 0, penalty["hitModifier"],
                 "No penalty if target visible")


# ============================================
# TEST 15: HAZARDOUS
# ============================================
def test_hazardous():
    print_test_header("HAZARDOUS - Mortal Wounds on Failed Test")
    
    import weaponAbilityDict as wad
    
    # Note: This test requires mocking rolls
    print("\n--- Test 15A: Has HAZARDOUS Ability ---")
    print("(Integration test - checks if function exists)")
    
    # Just verify function exists and accepts parameters
    try:
        damage = wad.performHazardousTests(["HAZARDOUS"], 5)
        print(f"Hazardous test result: {damage} mortal wounds")
        assert_equal("HAZARDOUS function works", True, True,
                     "Function executed without error")
    except Exception as e:
        assert_equal("HAZARDOUS function works", True, False,
                     f"Error: {e}")


# ============================================
# RUN ALL TESTS
# ============================================
def run_all_tests():
    print("\n" + "="*70)
    print("WEAPON ABILITIES TEST SUITE")
    print("Testing all implemented 40K weapon abilities")
    print("="*70)
    
    test_rapid_fire()
    test_blast()
    test_heavy()
    test_lethal_hits()
    test_anti()
    test_devastating_wounds()
    test_melta()
    test_twin_linked()
    test_torrent()
    test_assault()
    test_lance()
    test_ignores_cover()
    test_pistol()
    test_indirect_fire()
    test_hazardous()
    
    print_test_summary()
    
    return test_results["failed"] == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)