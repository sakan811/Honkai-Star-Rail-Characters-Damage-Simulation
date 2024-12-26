from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

def test_reduce_enemy_toughness():
    """Test enemy toughness reduction."""
    char = HarmonyCharacter()
    initial_toughness = char.enemy_toughness
    
    char.reduce_enemy_toughness(30)
    assert char.enemy_toughness == initial_toughness - 30
    
    # Test minimum bound
    char.reduce_enemy_toughness(200)
    assert char.enemy_toughness == 0

def test_handle_super_break_damage():
    """Test super break damage handling in different states."""
    char = HarmonyCharacter()
    dmg_list = []
    
    # Test normal toughness reduction
    char.handle_super_break_damage(dmg_list, 100)
    assert char.enemy_toughness == char.DEFAULT_ENEMY_TOUGHNESS - 20
    assert len(dmg_list) == 0
    
    # Test with turn delay
    char.enemy_turn_delay = 1
    char.handle_super_break_damage(dmg_list, 100)
    assert len(dmg_list) == 1
    assert dmg_list[0] == 100
    assert char.enemy_turn_delay == 0

def test_handle_break_damage():
    """Test break damage application."""
    char = HarmonyCharacter()
    dmg_list = []
    
    # Set up break condition
    char.enemy_toughness = 0
    char.has_broken_once = False
    
    char.handle_break_damage(dmg_list, 100, 200)
    assert len(dmg_list) == 2
    assert dmg_list == [100, 200]
    assert char.has_broken_once
    assert char.enemy_turn_delay == 1 