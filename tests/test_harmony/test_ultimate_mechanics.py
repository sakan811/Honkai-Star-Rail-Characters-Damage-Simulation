from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

def test_can_use_ultimate():
    """Test ultimate usage conditions."""
    char = HarmonyCharacter()
    assert not char._can_use_ultimate()
    
    char.trailblazer_current_energy = char.DEFAULT_ULT_ENERGY
    assert char._can_use_ultimate()

def test_apply_ultimate():
    """Test ultimate application with full energy."""
    char = HarmonyCharacter()
    dmg_list = []
    char.trailblazer_current_energy = char.DEFAULT_ULT_ENERGY
    
    char.apply_ultimate(
        dmg_list=dmg_list,
        atk=1000,
        dmg_bonus_multiplier=1.0,
        elemental_dmg_multiplier=1.0,
        res_pen_multiplier=1.0,
        additional_dmg=0,
        super_break_dmg=100,
        break_dmg=50
    )
    
    assert len(dmg_list) == 1
    assert dmg_list[0] == 4250  # 1000 * 4.25
    assert char.trailblazer_current_energy == 0 