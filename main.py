from Hunt import *
from Nihility import *
from Destruction import *

from sql_lite_pipeline import CharacterTable


if __name__ == '__main__':
    seele_with_no_resurgence = Seele().calculate_battles(False)
    seele_with_resurgence = Seele().calculate_battles(True)

    CharacterTable().migrate_to_character_table(
        'Seele', 'Seele With No Resurgence Buff', seele_with_no_resurgence
    )
    CharacterTable().migrate_to_character_table(
        'Seele', 'Seele With Resurgence Buff', seele_with_resurgence
    )

    dr_ratio_zero_debuff = DrRatio().calculate_battles(0)
    dr_ratio_one_debuff = DrRatio().calculate_battles(1)
    dr_ratio_two_debuff = DrRatio().calculate_battles(2)
    dr_ratio_three_debuff = DrRatio().calculate_battles(3)

    CharacterTable().migrate_to_character_table(
        'DrRatio', '0 Debuff', dr_ratio_zero_debuff
    )
    CharacterTable().migrate_to_character_table(
        'DrRatio', '1 Debuff', dr_ratio_one_debuff
    )
    CharacterTable().migrate_to_character_table(
        'DrRatio', '2 Debuff', dr_ratio_two_debuff
    )
    CharacterTable().migrate_to_character_table(
        'DrRatio', '3 Debuff', dr_ratio_three_debuff
    )

    numby_with_no_ult_buff = Numby().calculate_battles(False)
    numby_with_ult_buff = Numby().calculate_battles(True)

    CharacterTable().migrate_to_character_table(
        'Numby', 'Numby With No Ult Buff', numby_with_no_ult_buff
    )
    CharacterTable().migrate_to_character_table(
        'Numby', 'Numby With Ult Buff', numby_with_ult_buff
    )

    acheron_with_no_nihility_teammate = Acheron().calculate_battles(0)
    acheron_with_one_nihility_teammate = Acheron().calculate_battles(1)
    acheron_with_two_nihility_teammate = Acheron().calculate_battles(2)

    CharacterTable().migrate_to_character_table(
        'Acheron', 'Acheron With No Nihility Teammate', acheron_with_no_nihility_teammate
    )
    CharacterTable().migrate_to_character_table(
        'Acheron', 'Acheron With 1 Nihility Teammates', acheron_with_one_nihility_teammate
    )
    CharacterTable().migrate_to_character_table(
        'Acheron', 'Acheron With 2 Nihility Teammates', acheron_with_two_nihility_teammate
    )

    imbibitor_with_enhanced_once_basic_atk = ImbibitorLunae().calculate_battles(1)
    imbibitor_with_enhanced_twice_basic_atk = ImbibitorLunae().calculate_battles(2)
    imbibitor_with_enhanced_thrice_basic_atk = ImbibitorLunae().calculate_battles(3)

    CharacterTable().migrate_to_character_table(
        'ImbibitorLunae',
        'ImbibitorLunae With Enhanced-Once Basic Atk',
        imbibitor_with_enhanced_once_basic_atk
    )
    CharacterTable().migrate_to_character_table(
        'ImbibitorLunae',
        'ImbibitorLunae With Enhanced-Twice Basic Atk',
        imbibitor_with_enhanced_twice_basic_atk
    )
    CharacterTable().migrate_to_character_table(
        'ImbibitorLunae',
        'ImbibitorLunae With Enhanced-Thrice Basic Atk',
        imbibitor_with_enhanced_thrice_basic_atk
    )