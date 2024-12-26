from hsr_simulation.dmg_calculator import calculate_def_multipliers

def test_calculate_def_multipliers_default():
    """Test DEF multipliers with default (None) value"""
    result = calculate_def_multipliers()
    assert result == 1  # Default multiplier when no DEF reduction

def test_calculate_def_multipliers_empty_list():
    """Test DEF multipliers with empty list"""
    result = calculate_def_multipliers(def_reduction_multiplier=[])
    assert result == 1  # Base multiplier with empty DEF reduction list

def test_calculate_def_multipliers_single_value():
    """Test DEF multipliers with single reduction value"""
    result = calculate_def_multipliers(def_reduction_multiplier=[0.18])
    assert result == 1.18  # 1 + 0.18

def test_calculate_def_multipliers_multiple_values():
    """Test DEF multipliers with multiple reduction values"""
    result = calculate_def_multipliers(def_reduction_multiplier=[0.18, 0.12, 0.2])
    assert result == 1.5  # 1 + (0.18 + 0.12 + 0.2) 