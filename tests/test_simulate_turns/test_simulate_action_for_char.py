from hsr_simulation.character import Character
from hsr_simulation.simulate_turns import simulate_turns


def test_spd_90():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=90)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 6


def test_spd_93_dot_4():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=93.4)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 7


def test_spd_106_dot_7():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=106.7)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 8


def test_spd_120_dot_1():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=120.1)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 9


def test_spd_133_dot_4():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=133.4)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 10


def test_spd_146_dot_7():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=146.7)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 11


def test_spd_160_dot_1():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=160.1)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 12


def test_spd_173_dot_4():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=173.4)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 13


def test_spd_186_dot_7():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=186.7)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 14


def test_spd_200_dot_1():
    max_cycles = 7
    cycles_action_val = 150 + ((max_cycles - 1) * 100)
    character = Character(speed=200.1)
    turn_count = simulate_turns(character=character, cycles_action_val=cycles_action_val)
    assert turn_count == 15
