from hsr_simulation.dmg_calculator import calculate_total_damage


def test_calculate_total_damage_base():
    """Test total damage calculation with base values"""
    result = calculate_total_damage(
        base_dmg=1000,
        dmg_multipliers=1.0,
        res_multipliers=1.0,
        dmg_reduction=1.0,
        def_reduction_multiplier=1.0,
    )
    assert result == 1000  # No multipliers applied


def test_calculate_total_damage_with_multipliers():
    """Test total damage with all multipliers"""
    result = calculate_total_damage(
        base_dmg=1000,
        dmg_multipliers=1.5,  # 50% DMG increase
        res_multipliers=1.2,  # 20% RES penetration
        dmg_reduction=0.9,  # 10% DMG reduction
        def_reduction_multiplier=1.18,  # 18% DEF reduction
    )
    assert (
        abs(result - 1911.6) < 1e-10
    )  # Compare with small epsilon for floating point precision


def test_calculate_total_damage_zero_base():
    """Test total damage with zero base damage"""
    result = calculate_total_damage(
        base_dmg=0,
        dmg_multipliers=2.0,
        res_multipliers=1.5,
        dmg_reduction=0.9,
        def_reduction_multiplier=1.3,
    )
    assert result == 0  # Zero base damage results in zero total damage


def test_calculate_total_damage_high_multipliers():
    """Test total damage with high multipliers"""
    result = calculate_total_damage(
        base_dmg=1000,
        dmg_multipliers=3.0,  # 200% DMG increase
        res_multipliers=2.0,  # 100% RES penetration
        dmg_reduction=1.0,  # No reduction
        def_reduction_multiplier=2.0,  # 100% DEF reduction
    )
    assert result == 12000  # 1000 * 3.0 * 2.0 * 1.0 * 2.0
