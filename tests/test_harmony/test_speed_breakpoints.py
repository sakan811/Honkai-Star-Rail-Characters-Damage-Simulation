from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

def test_speed_breakpoint_no_bonus():
    """Test speed breakpoint calculation with no bonus speed."""
    char = HarmonyCharacter()
    assert char.calculate_spd_breakpoint() == 0

def test_speed_breakpoint_threshold():
    """Test speed breakpoint calculation at various thresholds."""
    char = HarmonyCharacter()
    test_cases = [
        (100, 0),  # Below first threshold
        (120, 1),  # At first threshold
        (160, 3),  # Middle threshold
        (200, 6),  # Maximum threshold
        (220, 6)   # Above maximum threshold
    ]
    
    for speed_bonus, expected_turns in test_cases:
        bonus_turns = char.calculate_spd_breakpoint(speed_bonus - char.DEFAULT_SPD)
        assert bonus_turns == expected_turns 