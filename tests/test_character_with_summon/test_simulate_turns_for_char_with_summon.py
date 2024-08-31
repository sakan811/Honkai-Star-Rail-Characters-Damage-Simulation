import pytest

from hsr_simulation.erudition.jingyuan import Jingyuan
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.simulate_cycles import simulate_cycles_for_character_with_summon


@pytest.fixture
def setup_character():
    def _setup_character(character_class):
        character = character_class()
        summon = None
        if isinstance(character, Topaz):
            summon = character.summon_numby(character)
        elif isinstance(character, Jingyuan):
            summon = character.summon_lightning_lord(character)
        return character, summon

    return _setup_character


@pytest.mark.parametrize("character_class, max_cycles, simulate_round, expected_dmg_len, expected_dmg_type_len, "
                         "expected_round_no_len", [
                             (Topaz, 5, 1, True, True, True),
                             (Topaz, 0, 1, False, False, False),
                             (Jingyuan, 5, 1, True, True, True),
                             (Jingyuan, 0, 1, False, False, False)
                         ])
def test_simulate_turns(setup_character, character_class, max_cycles, simulate_round, expected_dmg_len,
                        expected_dmg_type_len, expected_round_no_len):
    # Given
    character, summon = setup_character(character_class)

    # When
    result = simulate_cycles_for_character_with_summon(character, summon, max_cycles, simulate_round)

    # Then
    assert isinstance(result, dict)
    assert 'DMG' in result
    assert 'DMG_Type' in result
    assert 'Simulate Round No.' in result
    assert (len(result['DMG']) > 0) == expected_dmg_len
    assert (len(result['DMG_Type']) > 0) == expected_dmg_type_len
    assert (len(result['Simulate Round No.']) > 0) == expected_round_no_len
