from hsr_simulation.dmg_calculator import calculate_break_damage


def test_calculate_break_damage_physical():
    """Test break damage for Physical type"""
    result = calculate_break_damage(break_type="Physical", target_max_toughness=100)
    expected = 2 * 3767 * (0.5 + 100 / 40)  # base_multiplier=2
    assert result == expected


def test_calculate_break_damage_fire():
    """Test break damage for Fire type"""
    result = calculate_break_damage(break_type="Fire", target_max_toughness=100)
    expected = 2 * 3767 * (0.5 + 100 / 40)  # base_multiplier=2
    assert result == expected


def test_calculate_break_damage_ice():
    """Test break damage for Ice type"""
    result = calculate_break_damage(break_type="Ice", target_max_toughness=100)
    expected = 1 * 3767 * (0.5 + 100 / 40)  # base_multiplier=1
    assert result == expected


def test_calculate_break_damage_lightning():
    """Test break damage for Lightning type"""
    result = calculate_break_damage(break_type="Lightning", target_max_toughness=100)
    expected = 1 * 3767 * (0.5 + 100 / 40)  # base_multiplier=1
    assert result == expected


def test_calculate_break_damage_wind():
    """Test break damage for Wind type"""
    result = calculate_break_damage(break_type="Wind", target_max_toughness=100)
    expected = 1.5 * 3767 * (0.5 + 100 / 40)  # base_multiplier=1.5
    assert result == expected


def test_calculate_break_damage_quantum():
    """Test break damage for Quantum type"""
    result = calculate_break_damage(break_type="Quantum", target_max_toughness=100)
    expected = 0.5 * 3767 * (0.5 + 100 / 40)  # base_multiplier=0.5
    assert result == expected


def test_calculate_break_damage_imaginary():
    """Test break damage for Imaginary type"""
    result = calculate_break_damage(break_type="Imaginary", target_max_toughness=100)
    expected = 0.5 * 3767 * (0.5 + 100 / 40)  # base_multiplier=0.5
    assert result == expected


def test_calculate_break_damage_unknown_type():
    """Test break damage for unknown break type"""
    result = calculate_break_damage(break_type="Unknown", target_max_toughness=100)
    expected = 1 * 3767 * (0.5 + 100 / 40)  # base_multiplier=1 (default)
    assert result == expected


def test_calculate_break_damage_zero_toughness():
    """Test break damage with zero toughness"""
    result = calculate_break_damage(break_type="Physical", target_max_toughness=0)
    expected = 2 * 3767 * 0.5  # Only base toughness multiplier (0.5)
    assert result == expected
