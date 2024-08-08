from hsr_simulation.character import Character
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.simulate_cycles import simulate_cycles_for_character_with_summon


def test_simulate_turns_with_default_parameters():
    # Given
    base_char = Character()
    topaz = Topaz(base_char)
    numby = topaz.summon_numby()

    max_cycles = 5
    simulate_round = 1

    # When
    result = simulate_cycles_for_character_with_summon(topaz, numby, max_cycles, simulate_round)

    # Then
    assert isinstance(result, dict)
    assert 'DMG' in result
    assert 'DMG_Type' in result
    assert 'Simulate Round No.' in result
    assert len(result['DMG']) > 0
    assert len(result['DMG_Type']) > 0
    assert len(result['Simulate Round No.']) > 0


def test_simulate_turns_with_zero_max_cycles():
    # Given
    base_char = Character()
    topaz = Topaz(base_char)
    numby = topaz.summon_numby()
    max_cycles = 0
    simulate_round = 1

    # When
    result = simulate_cycles_for_character_with_summon(topaz, numby, max_cycles, simulate_round)

    # Then
    assert isinstance(result, dict)
    assert 'DMG' in result
    assert 'DMG_Type' in result
    assert 'Simulate Round No.' in result
    assert len(result['DMG']) == 0
    assert len(result['DMG_Type']) == 0
    assert len(result['Simulate Round No.']) == 0