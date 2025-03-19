from hsr_simulation.dmg_calculator import calculate_break_effect


def test_calculate_break_effect_base():
    """Test break effect with base multiplier (1.0)"""
    result = calculate_break_effect(break_amount=100, break_effect=1.0)
    assert result == 100  # No increase in break amount


def test_calculate_break_effect_increased():
    """Test break effect with increased multiplier"""
    result = calculate_break_effect(break_amount=100, break_effect=1.3)
    assert result == 130  # 30% increase in break amount


def test_calculate_break_effect_zero_amount():
    """Test break effect with zero break amount"""
    result = calculate_break_effect(break_amount=0, break_effect=1.5)
    assert result == 0  # Zero break amount remains zero


def test_calculate_break_effect_large_values():
    """Test break effect with large values"""
    result = calculate_break_effect(break_amount=1000, break_effect=2.0)
    assert result == 2000  # Double break amount
