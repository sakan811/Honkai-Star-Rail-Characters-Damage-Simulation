from hsr_simulation.character import Character
from hsr_simulation.simulate_turns import simulate_turns

import pytest


@pytest.mark.parametrize(
    "speed, expected_turn_count",
    [
        (90, 6),
        (93.4, 7),
        (106.7, 8),
        (120.1, 9),
        (133.4, 10),
        (146.7, 11),
        (160.1, 12),
        (173.4, 13),
        (186.7, 14),
        (200.1, 15),
    ],
)
def test_spd(speed, expected_turn_count):
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=speed)
    turn_count = simulate_turns(
        character=character, cycles_action_val=cycles_action_val
    )
    assert turn_count == expected_turn_count
