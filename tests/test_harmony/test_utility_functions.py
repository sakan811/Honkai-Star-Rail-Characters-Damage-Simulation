from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

def test_process_multiplier():
    """Test multiplier processing."""
    char = HarmonyCharacter()
    assert char._process_multiplier(None) == 1
    assert char._process_multiplier(0.5) == 1.5
    assert char._process_multiplier(1.0) == 2.0

def test_calculate_turn_count():
    """Test turn count calculation."""
    char = HarmonyCharacter()
    assert char._calculate_turn_count() == 5
    assert char._calculate_turn_count(2) == 7
    assert char._calculate_turn_count(None) == 5

def test_calculate_percent_change():
    """Test percentage change calculation."""
    char = HarmonyCharacter()
    
    # Test decimal mode off
    assert char.calculate_percent_change(100, 150) == 50
    
    # Test decimal mode on
    assert char.calculate_percent_change(100, 150, decimal_mode=True) == 0.5

def test_crit_buff():
    """Test critical hit buff calculation."""
    char = HarmonyCharacter()
    buff = char.crit_buff(0.5, 2.0)
    expected = ((1 - 0.5) * 1 + 0.5 * 2) / 1 - 1
    assert abs(buff - expected) < 0.001 