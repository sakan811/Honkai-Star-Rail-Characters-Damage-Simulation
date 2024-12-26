from hsr_simulation.dmg_calculator import calculate_res_multipliers

def test_calculate_res_multipliers_default():
    """Test RES multipliers with default (None) value"""
    result = calculate_res_multipliers()
    assert result == 1  # Default multiplier when no RES pen

def test_calculate_res_multipliers_empty_list():
    """Test RES multipliers with empty list"""
    result = calculate_res_multipliers(res_pen=[])
    assert result == 1  # Base multiplier with empty RES pen list

def test_calculate_res_multipliers_single_value():
    """Test RES multipliers with single penetration value"""
    result = calculate_res_multipliers(res_pen=[0.2])
    assert result == 1.2  # 1 + 0.2

def test_calculate_res_multipliers_multiple_values():
    """Test RES multipliers with multiple penetration values"""
    result = calculate_res_multipliers(res_pen=[0.2, 0.3, 0.1])
    assert result == 1.6  # 1 + (0.2 + 0.3 + 0.1) 