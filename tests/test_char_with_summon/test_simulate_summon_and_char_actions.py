from hsr_simulation.hunt.topaz import Topaz, Numby
from hsr_simulation.simulate_turns import simulate_actions_for_char_with_summon


def test_spd_90():
    # Given:
    topaz = Topaz(speed=90)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 6


def test_spd_93_dot_4():
    # Given:
    topaz = Topaz(speed=93.4)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 7


def test_spd_106_dot_7():
    # Given:
    topaz = Topaz(speed=106.7)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 8


def test_spd_120_dot_1():
    # Given:
    topaz = Topaz(speed=120.1)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 9


def test_spd_133_dot_4():
    # Given:
    topaz = Topaz(speed=133.4)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 10


def test_spd_146_dot_7():
    # Given:
    topaz = Topaz(speed=146.7)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 11


def test_spd_160_dot_1():
    # Given:
    topaz = Topaz(speed=160.1)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 12


def test_spd_173_dot_4():
    # Given:
    topaz = Topaz(speed=173.4)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 13


def test_spd_186_dot_7():
    # Given:
    topaz = Topaz(speed=186.7)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 14


def test_spd_200_dot_1():
    # Given:
    topaz = Topaz(speed=200.1)
    numby = Numby(topaz)

    max_cycles = 7

    cycles_action_val = 150 + ((max_cycles - 1) * 100)

    cycles_action_value_for_topaz = cycles_action_val
    cycles_action_value_for_numby = cycles_action_val

    topaz_end = False
    numby_end = False

    # When:
    numby_turn_count, topaz_turn_count = simulate_actions_for_char_with_summon(cycles_action_value_for_numby,
                                                                               cycles_action_value_for_topaz, numby,
                                                                               numby_end,
                                                                               topaz, topaz_end)

    assert topaz_turn_count == 15
