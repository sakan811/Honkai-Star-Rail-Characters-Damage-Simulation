from hsr_simulation.erudition.jingyuan import Jingyuan
from hsr_simulation.hunt.topaz import Topaz
from hsr_simulation.simulate_battles import start_simulations_for_char_with_summon


def test_subclass_topaz_and_numby():
    # Given:
    topaz = Topaz()
    numby = topaz.summon_numby(topaz)

    # When:
    dict_list = start_simulations_for_char_with_summon(
        topaz, numby, max_cycles=10, simulation_num=2
    )

    # Then:
    # Ensure the simulations returned a non-empty list
    assert len(dict_list) > 0

    # Validate Topaz's attributes
    assert topaz.atk == 2000
    assert topaz.crit_rate == 0.5
    assert topaz.crit_dmg == 1.0
    assert topaz.speed == 110
    assert topaz.ult_energy == 130

    # Validate Numby's attributes
    assert numby.atk == 2000
    assert numby.crit_rate == 0.5
    assert numby.crit_dmg == 1.0
    assert numby.speed == 80
    assert numby.ult_energy == 0

    # Validate 'Simulate Round No.' correctness
    for index, element in enumerate(dict_list):
        if "Simulate Round No." in element:
            for i in element["Simulate Round No."]:
                assert i == index


def test_subclass_jingyuan_and_lighting_lord():
    # Given:
    jingyuan = Jingyuan()
    lightning_lord = jingyuan.summon_lightning_lord(jingyuan)

    # When:
    dict_list = start_simulations_for_char_with_summon(
        jingyuan, lightning_lord, max_cycles=10, simulation_num=2
    )

    # Then:
    # Ensure the simulations returned a non-empty list
    assert len(dict_list) > 0

    # Validate Jing Yuan's attributes
    assert jingyuan.atk == 2000
    assert jingyuan.crit_rate == 0.5
    assert jingyuan.crit_dmg == 1.0
    assert jingyuan.speed == 99
    assert jingyuan.ult_energy == 130

    # Validate Lightning Lord's attributes
    assert lightning_lord.atk == 2000
    assert lightning_lord.crit_rate == 0.5
    assert lightning_lord.crit_dmg == 1.0
    assert lightning_lord.speed == 60
    assert lightning_lord.ult_energy == 0

    # Validate 'Simulate Round No.' correctness
    for index, element in enumerate(dict_list):
        if "Simulate Round No." in element:
            for i in element["Simulate Round No."]:
                assert i == index
