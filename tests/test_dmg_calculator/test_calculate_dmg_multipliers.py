from hsr_simulation.dmg_calculator import calculate_dmg_multipliers

def test_calculate_dmg_multipliers_default_values():
    """Test calculate_dmg_multipliers with default values"""
    result = calculate_dmg_multipliers()
    assert result == 1  # (1 + 0) * (1 + 0 + 0)

def test_calculate_dmg_multipliers_with_crit():
    """Test calculate_dmg_multipliers with crit damage"""
    result = calculate_dmg_multipliers(crit_dmg=0.5)
    assert result == 1.5  # (1 + 0.5) * (1 + 0 + 0)

def test_calculate_dmg_multipliers_with_dot():
    """Test calculate_dmg_multipliers with DoT damage"""
    result = calculate_dmg_multipliers(dot_dmg=[0.2, 0.3])
    assert result == 1.5  # (1 + 0) * (1 + 0.5 + 0)

def test_calculate_dmg_multipliers_with_dmg():
    """Test calculate_dmg_multipliers with damage multipliers"""
    result = calculate_dmg_multipliers(dmg_multipliers=[0.3, 0.2])
    assert result == 1.5  # (1 + 0) * (1 + 0 + 0.5)

def test_calculate_dmg_multipliers_all_parameters():
    """Test calculate_dmg_multipliers with all parameters"""
    result = calculate_dmg_multipliers(
        crit_dmg=0.5,
        dot_dmg=[0.2, 0.3],
        dmg_multipliers=[0.3, 0.2]
    )
    assert result == 3.0  # (1 + 0.5) * (1 + 0.5 + 0.5)

def test_calculate_dmg_multipliers_empty_lists():
    """Test calculate_dmg_multipliers with empty lists"""
    result = calculate_dmg_multipliers(
        crit_dmg=0.5,
        dot_dmg=[],
        dmg_multipliers=[]
    )
    assert result == 1.5  # (1 + 0.5) * (1 + 0 + 0) 