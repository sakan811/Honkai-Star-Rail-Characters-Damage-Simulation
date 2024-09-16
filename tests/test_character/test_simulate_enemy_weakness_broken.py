import pytest
from hsr_simulation.character import Character


@pytest.fixture
def character():
    return Character()


def test_enemy_weakness_broken(character):
    # Set up the character with enemy weakness broken
    character.enemy_weakness_broken = True
    character.enemy_turn_delayed_duration_weakness_broken = 1

    # Call the method
    character._simulate_enemy_weakness_broken()

    # Assert the enemy turn delayed duration is decreased
    assert character.enemy_turn_delayed_duration_weakness_broken == 0


def test_enemy_weakness_broken_regenerate(character):
    # Set up the character with enemy weakness broken and no delay duration
    character.enemy_weakness_broken = True
    character.enemy_turn_delayed_duration_weakness_broken = 0

    # Call the method
    character._simulate_enemy_weakness_broken()

    # Assert the enemy toughness is regenerated and weakness is not broken
    assert character.current_enemy_toughness == character.enemy_toughness
    assert not character.enemy_weakness_broken


def test_enemy_not_weakness_broken(character):
    # Set up the character with enemy not weakness broken
    character.enemy_weakness_broken = False

    # Call the method
    character._simulate_enemy_weakness_broken()

    # Assert nothing changes
    assert character.enemy_turn_delayed_duration_weakness_broken == 0
    assert character.current_enemy_toughness == character.enemy_toughness
    assert not character.enemy_weakness_broken
