import pytest
from hsr_simulation.character import Character


@pytest.fixture
def character():
    return Character()


def test_dmg_reduction_when_enemy_not_broken(character):
    # Set up the character with enemy not broken
    character.enemy_weakness_broken = False
    initial_toughness = character.current_enemy_toughness

    # Call the method
    dmg = character._calculate_damage(skill_multiplier=1, break_amount=10, can_crit=False)

    # Assert the damage is reduced
    assert dmg < character.atk
    assert character.current_enemy_toughness == initial_toughness - 10


def test_no_dmg_reduction_when_enemy_broken(character):
    # Set up the character with enemy broken
    character.enemy_weakness_broken = True
    initial_toughness = character.current_enemy_toughness

    # Call the method
    dmg = character._calculate_damage(skill_multiplier=1, break_amount=10, can_crit=False)

    # Assert the damage is not reduced
    assert dmg == character.atk
    assert character.current_enemy_toughness == initial_toughness - 10
