import pytest
from hsr_simulation.character import Character


@pytest.fixture
def character():
    return Character()


def test_break_effect_setting(character):
    """Test break effect setting"""
    min_break = 1.0
    max_break = 2.0

    character.set_break_effect(min_break, max_break)

    assert character.break_effect in [min_break, max_break]


def test_effect_hit_rate_setting(character):
    """Test effect hit rate setting"""
    min_rate = 0.5
    max_rate = 0.8

    character.set_effect_hit_rate(min_rate, max_rate)

    assert character.effect_hit_rate in [min_rate, max_rate]


def test_super_break_damage(character):
    """Test super break damage calculation"""
    toughness_reduction = 30
    break_effect = 1.5

    damage = character._deal_super_break_dmg(toughness_reduction, break_effect)

    assert damage > 0
    assert isinstance(damage, float)
