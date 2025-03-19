from hsr_simulation.harmony.harmony_base_char import HarmonyCharacter


def test_process_multiplier():
    """Test multiplier processing."""
    char = HarmonyCharacter()
    assert char._process_multiplier(None) == 1
    assert char._process_multiplier(0.5) == 1.5
    assert char._process_multiplier(1.0) == 2.0


def test_calculate_percent_change():
    """Test percentage change calculation."""
    char = HarmonyCharacter()

    # Test decimal mode off
    assert char.calculate_percent_change(100, 150) == 50

    # Test decimal mode on
    assert char.calculate_percent_change(100, 150, decimal_mode=True) == 0.5


def test_crit_buff():
    """Test critical hit buff calculation."""
    # Test with default base values (0, 0)
    crit_rate, crit_dmg = 0.5, 2.0
    buff = HarmonyCharacter.crit_buff(crit_rate, crit_dmg)

    # Calculate expected result manually
    base_damage = 1
    baseline_avg_damage = 1  # With base_crit_rate=0 and base_crit_dmg=0, this is just 1
    new_avg_damage = (1 - crit_rate) * base_damage + crit_rate * (
        base_damage * (1 + crit_dmg)
    )
    expected = (new_avg_damage / baseline_avg_damage) - 1

    assert abs(buff - expected) < 0.001

    # Test with custom base values
    base_crit_rate, base_crit_dmg = 0.3, 1.0
    buff = HarmonyCharacter.crit_buff(
        crit_rate, crit_dmg, base_crit_rate, base_crit_dmg
    )

    # Calculate expected result manually
    baseline_avg_damage = (1 - base_crit_rate) * base_damage + base_crit_rate * (
        base_damage * (1 + base_crit_dmg)
    )
    new_avg_damage = (1 - crit_rate) * base_damage + crit_rate * (
        base_damage * (1 + crit_dmg)
    )
    expected = (new_avg_damage / baseline_avg_damage) - 1

    assert abs(buff - expected) < 0.001
