import pytest

from hsr_simulation.erudition.jingyuan import Jingyuan
from hsr_simulation.hunt.topaz import Topaz, Numby
from hsr_simulation.simulate_turns import simulate_turns_for_char_with_summon


@pytest.mark.parametrize("index, speed, expected_char_turn_count, expected_summon_turn_count", [
    (0, 90, 6, 6),
    (1, 93.4, 7, 7),
    (2, 106.7, 8, 8),
    (3, 120.1, 9, 9),
    (4, 133.4, 10, 10),
    (5, 146.7, 11, 11),
    (6, 160.1, 12, 12),
    (7, 173.4, 13, 13),
    (8, 186.7, 14, 14),
    (9, 200.1, 15, 15),
])
def test_spd_topaz(index, speed, expected_char_turn_count, expected_summon_turn_count):
    # Given:
    topaz = Topaz(speed=speed)
    numby = topaz.summon_numby(topaz, speed=speed)
    numby.set_test(True)

    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_turns_for_char_with_summon(
        cycles_action_val, cycles_action_val, numby, numby_end, topaz, topaz_end
    )

    # Then:
    assert topaz_turn_count == expected_char_turn_count
    assert numby_turn_count == expected_summon_turn_count


@pytest.mark.parametrize("index, speed, expected_char_turn_count, expected_summon_turn_count", [
    (0, 90, 6, 6),
    (1, 93.4, 7, 7),
    (2, 106.7, 8, 8),
    (3, 120.1, 9, 9),
    (4, 133.4, 10, 10),
    (5, 146.7, 11, 11),
    (6, 160.1, 12, 12),
    (7, 173.4, 13, 13),
    (8, 186.7, 14, 14),
    (9, 200.1, 15, 15),
])
def test_spd_jingyuan(index, speed, expected_char_turn_count, expected_summon_turn_count):
    # Given:
    jingyuan = Jingyuan(speed=speed)
    lightning_lord = jingyuan.summon_lightning_lord(jingyuan, speed=speed)
    lightning_lord.set_test(True)

    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    jingyuan_end = False
    lightning_end = False

    # When:
    lightning_lord_turn_count, jingyuan_turn_count = simulate_turns_for_char_with_summon(
        cycles_action_val, cycles_action_val, lightning_lord, lightning_end, jingyuan, jingyuan_end
    )

    print(lightning_lord.speed)

    # Then:
    assert jingyuan_turn_count == expected_char_turn_count
    assert lightning_lord_turn_count == expected_summon_turn_count







