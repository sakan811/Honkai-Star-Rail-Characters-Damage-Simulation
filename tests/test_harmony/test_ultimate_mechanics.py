from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

def test_ultimate_energy_management():
    """Test ultimate energy management."""
    char = HarmonyCharacter()
    
    # Initial energy is 0
    assert char.trailblazer_current_energy == 0
    
    # Fill energy to max
    char.trailblazer_current_energy = char.DEFAULT_ULT_ENERGY
    assert char.trailblazer_current_energy == char.DEFAULT_ULT_ENERGY
    
    # Calculate ultimate damage
    damage = char.calculate_ultimate_damage(
        atk=1000,
        dmg_bonus_multiplier=1.0,
        elemental_dmg_multiplier=1.0,
        res_pen_multiplier=1.0
    )
    
    assert damage == 1000 * 4.25  # 1000 * 4.25 * 1.0 * 1.0 * 1.0 