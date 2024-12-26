from hsr_simulation.dmg_calculator import calculate_universal_dmg_reduction

def test_calculate_universal_dmg_reduction_weakness_broken():
    """Test damage reduction when enemy is weakness broken"""
    result = calculate_universal_dmg_reduction(weakness_broken=True)
    assert result == 1.0  # No damage reduction when broken

def test_calculate_universal_dmg_reduction_not_broken():
    """Test damage reduction when enemy is not weakness broken"""
    result = calculate_universal_dmg_reduction(weakness_broken=False)
    assert result == 0.9  # 10% damage reduction when not broken 