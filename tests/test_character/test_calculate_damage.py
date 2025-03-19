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
    dmg = character._calculate_damage(
        skill_multiplier=1, break_amount=10, can_crit=False
    )

    # Assert the damage is reduced
    assert dmg < character.atk
    assert character.current_enemy_toughness == initial_toughness - 10


def test_no_dmg_reduction_when_enemy_broken(character):
    # Set up the character with enemy broken
    character.enemy_weakness_broken = True
    initial_toughness = character.current_enemy_toughness

    # Call the method
    dmg = character._calculate_damage(
        skill_multiplier=1, break_amount=10, can_crit=False
    )

    # Assert the damage is not reduced
    assert dmg == character.atk
    assert character.current_enemy_toughness == initial_toughness - 10


def test_skill_damage_calculation(character):
    """Test skill damage calculation"""
    initial_toughness = character.current_enemy_toughness

    # Use skill
    character.skill_points = 1
    character._use_skill()

    # Verify damage recording and skill point consumption
    assert len(character.data["DMG"]) == 1
    assert character.data["DMG_Type"][-1] == "Skill"
    assert character.skill_points == 0
    assert (
        character.current_enemy_toughness
        == initial_toughness - Character.SKILL_BREAK_AMOUNT
    )


def test_ultimate_damage_calculation(character):
    """Test ultimate damage calculation"""
    character.current_ult_energy = character.ult_energy
    initial_toughness = character.current_enemy_toughness

    character._use_ult()

    assert len(character.data["DMG"]) == 1
    assert character.data["DMG_Type"][-1] == "Ultimate"
    assert character.current_ult_energy == Character.DEFAULT_ULT_ENERGY_AFTER_ULT
    assert (
        character.current_enemy_toughness
        == initial_toughness - Character.ULT_BREAK_AMOUNT
    )
