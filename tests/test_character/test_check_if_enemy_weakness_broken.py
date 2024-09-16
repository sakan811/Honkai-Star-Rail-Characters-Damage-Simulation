import pytest
from hsr_simulation.character import Character

@pytest.fixture
def character():
    return Character()

def test_enemy_weakness_broken(character):
    # Set up the character with enemy toughness <= 0 and weakness not broken
    character.current_enemy_toughness = 0
    character.enemy_weakness_broken = False

    # Call the method
    character.check_if_enemy_weakness_broken()

    # Assert the enemy weakness is broken and turn delayed duration is set
    assert character.enemy_weakness_broken is True
    assert character.enemy_turn_delayed_duration_weakness_broken == 1

def test_enemy_weakness_not_broken(character):
    # Set up the character with enemy toughness > 0
    character.current_enemy_toughness = 10
    character.enemy_weakness_broken = False

    # Call the method
    character.check_if_enemy_weakness_broken()

    # Assert the enemy weakness is not broken
    assert character.enemy_weakness_broken is False
    assert character.enemy_turn_delayed_duration_weakness_broken == 0

def test_enemy_already_weakness_broken(character):
    # Set up the character with enemy weakness already broken
    character.current_enemy_toughness = 0
    character.enemy_weakness_broken = True

    # Call the method
    character.check_if_enemy_weakness_broken()

    # Assert the enemy weakness remains broken and turn delayed duration is unchanged
    assert character.enemy_weakness_broken is True
    assert character.enemy_turn_delayed_duration_weakness_broken == 0