from hsr_simulation.character import Character
from hsr_simulation.nihility.kafka import Kafka
from hsr_simulation.simulate_battles import start_simulations


def test_character():
    character = Character()
    dict_list = start_simulations(character, max_cycles=10, simulation_num=2)
    print(dict_list)

    assert len(dict_list) > 0
    assert character.atk == 2000
    assert character.crit_rate == 0.5
    assert character.crit_dmg == 1.0
    assert character.speed == 90
    assert character.ult_energy == 140

    # test whether Simulate Round No. is correct
    for index, element in enumerate(dict_list):
        if 'Simulate Round No.' in element:
            for i in element['Simulate Round No.']:
                if index == 0:
                    assert i == 0
                elif index == 1:
                    assert i == 1


def test_subclass_character():
    character = Kafka()
    dict_list = start_simulations(character, max_cycles=10, simulation_num=2)

    assert len(dict_list) > 0
    assert character.atk == 2000
    assert character.crit_rate == 0.5
    assert character.crit_dmg == 1.0
    assert character.speed == 100
    assert character.ult_energy == 120

    # test whether Simulate Round No. is correct
    for index, element in enumerate(dict_list):
        if 'Simulate Round No.' in element:
            for i in element['Simulate Round No.']:
                if index == 0:
                    assert i == 0
                elif index == 1:
                    assert i == 1


def test_character_initialization():
    character = Character(
        atk=2000,
        crit_rate=0.5,
        crit_dmg=1.0,
        speed=90,
        ult_energy=140
    )
    
    # Test default stats initialization
    assert character.atk == 2000
    assert character.crit_rate == 0.5
    assert character.crit_dmg == 1.0
    assert character.speed == 90
    assert character.ult_energy == 140
    assert character.current_ult_energy == 0
    assert character.skill_points == Character.DEFAULT_SKILL_POINTS
    assert character.enemy_toughness == Character.DEFAULT_ENEMY_TOUGHNESS


def test_character_reset():
    character = Character()
    
    # Modify some stats
    character.current_ult_energy = 100
    character.skill_points = 0
    character.enemy_weakness_broken = True
    
    character.reset_character_data_for_each_battle()
    
    assert character.current_ult_energy == 0
    assert character.skill_points == Character.DEFAULT_SKILL_POINTS
    assert character.enemy_weakness_broken == False
    assert character.data == {'DMG': [], 'DMG_Type': [], 'Simulate Round No.': []}

