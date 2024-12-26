from hsr_simulation.dmg_calculator import calculate_super_break_dmg

def test_calculate_super_break_dmg_default_break_effect():
    """Test super break damage with default break effect"""
    result = calculate_super_break_dmg(base_toughness_reduce=100)
    expected = 3767.5533 * (100/10) * (1 + 1)  # Default break_effect=1
    assert result == expected

def test_calculate_super_break_dmg_with_break_effect():
    """Test super break damage with custom break effect"""
    result = calculate_super_break_dmg(
        base_toughness_reduce=100,
        break_effect=1.3  # Common break effect value
    )
    expected = 3767.5533 * (100/10) * (1 + 1.3)
    assert result == expected

def test_calculate_super_break_dmg_zero_toughness():
    """Test super break damage with zero toughness reduction"""
    result = calculate_super_break_dmg(
        base_toughness_reduce=0,
        break_effect=1.5
    )
    assert result == 0  # Zero toughness reduction should result in zero damage

def test_calculate_super_break_dmg_large_values():
    """Test super break damage with large toughness reduction"""
    result = calculate_super_break_dmg(
        base_toughness_reduce=1000,
        break_effect=2.0
    )
    expected = 3767.5533 * (1000/10) * (1 + 2.0)
    assert result == expected 