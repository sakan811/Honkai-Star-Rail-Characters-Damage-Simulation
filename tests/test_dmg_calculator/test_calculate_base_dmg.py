from hsr_simulation.dmg_calculator import calculate_base_dmg


def test_calculate_base_dmg_default_values():
    """Test calculate_base_dmg with default values"""
    result = calculate_base_dmg()
    assert result == 1  # skill_multiplier=1 * atk=1 + extra_dmg=0


def test_calculate_base_dmg_with_skill_multiplier():
    """Test calculate_base_dmg with skill multiplier"""
    result = calculate_base_dmg(skill_multiplier=2.0, atk=1000)
    assert result == 2000  # 2.0 * 1000


def test_calculate_base_dmg_with_extra_multipliers():
    """Test calculate_base_dmg with extra multipliers"""
    result = calculate_base_dmg(
        skill_multiplier=1.5, extra_multipliers=[0.2, 0.3], atk=1000
    )
    assert result == 2000  # (1.5 + 0.5) * 1000


def test_calculate_base_dmg_with_extra_dmg():
    """Test calculate_base_dmg with extra flat damage"""
    result = calculate_base_dmg(skill_multiplier=2.0, atk=1000, extra_dmg=500)
    assert result == 2500  # (2.0 * 1000) + 500


def test_calculate_base_dmg_all_parameters():
    """Test calculate_base_dmg with all parameters"""
    result = calculate_base_dmg(
        skill_multiplier=2.0, extra_multipliers=[0.3, 0.2], atk=1000, extra_dmg=500
    )
    assert result == 3000  # (2.0 + 0.5) * 1000 + 500
