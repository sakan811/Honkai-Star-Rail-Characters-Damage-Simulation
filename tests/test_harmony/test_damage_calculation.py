from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter

def test_calculate_damage_basic():
    """Test basic damage calculation with default values."""
    char = HarmonyCharacter()
    damage = char._calculate_damage(
        atk=1000,
        multiplier=1.5,
        dmg_bonus_multiplier=1.0,
        elemental_dmg_multiplier=1.0,
        res_pen_multiplier=1.0
    )
    assert damage == 1500

def test_calculate_damage_with_multipliers():
    """Test damage calculation with various multipliers."""
    char = HarmonyCharacter()
    damage = char._calculate_damage(
        atk=1000,
        multiplier=1.5,
        dmg_bonus_multiplier=1.2,
        elemental_dmg_multiplier=1.3,
        res_pen_multiplier=1.1,
        additional_dmg=100
    )
    expected = (1000 * 1.5 + 100) * 1.2 * 1.3 * 1.1
    assert abs(damage - expected) < 0.001 