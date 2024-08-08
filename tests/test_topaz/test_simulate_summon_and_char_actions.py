from hsr_simulation.character import Character
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.simulate_turns import simulate_turns_for_char_with_summon

import pytest


@pytest.mark.parametrize("index, speed, expected_turn_count", [
    (0, 90, 6),
    (1, 93.4, 7),
    (2, 106.7, 8),
    (3, 120.1, 9),
    (4, 133.4, 10),
    (5, 146.7, 11),
    (6, 160.1, 12),
    (7, 173.4, 13),
    (8, 186.7, 14),
    (9, 200.1, 15),
])
def test_spd(index, speed, expected_turn_count):
    # Given:
    base_char = Character()
    topaz = Topaz(base_char=base_char, speed=speed)
    numby = topaz.summon_numby()
    numby.inherit_topaz(topaz)

    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_turns_for_char_with_summon(
        cycles_action_val, cycles_action_val, numby, numby_end, topaz, topaz_end
    )

    # Then:
    assert topaz_turn_count == expected_turn_count






