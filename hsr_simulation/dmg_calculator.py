#    Copyright 2024 Sakan Nirattisaykul
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from hsr_simulation.configure_logging import main_logger


def calculate_base_dmg(
        skill_multiplier: float = 1,
        extra_multipliers: list[float] = None,
        atk: float = 1,
        extra_dmg: float = 0) -> float:
    """
    Calculates base damage
    :param skill_multiplier: This is the percentage value stated in the skill description, indicating the damage dealt.
    :param extra_multipliers: This additional percentage value applies to some skills.
    :param atk: Character's Attack.
    :param extra_dmg: A flat additional damage value that is included in some skills.
    :return: Base damage
    """
    main_logger.info('Calculating base damage...')

    extra_multipliers_sum = 0
    if extra_multipliers is not None:
        extra_multipliers_sum = sum(extra_multipliers)

    return (skill_multiplier + extra_multipliers_sum) * atk + extra_dmg


def calculate_dmg_multipliers(
        crit_dmg: float = 0,
        dot_dmg: list[float] = None,
        dmg_multipliers: list[float] = None) -> float:
    """
    Calculates base damage multipliers.
    :param crit_dmg: Critical damage multiplier
    :param dot_dmg: List of DoT damage multipliers
    :param dmg_multipliers: List of damage multipliers
    :return: Final damage multiplier
    """
    main_logger.info('Calculating damage multipliers...')

    dot_dmg_sum = 0 if dot_dmg is None else sum(dot_dmg)
    dmg_multipliers_sum = 0 if dmg_multipliers is None else sum(dmg_multipliers)

    damage_multiplier = (1 + crit_dmg) * (1 + dot_dmg_sum + dmg_multipliers_sum)

    return damage_multiplier


def calculate_universal_dmg_reduction(weakness_broken: bool) -> float:
    """
    Calculates universal dmg reduction
    :param weakness_broken: Whether the weakness broken.
    :return: Damage Reduction Multiplier
    """
    main_logger.info('Returning universal dmg reduction multiplier...')

    if weakness_broken:
        main_logger.debug('No damage reduction')
        return 1
    else:
        main_logger.debug('Reduce dmg')
        return 0.9

def calculate_res_multipliers(res_pen: list[float] = None) -> float:
    """
    Calculates RES multipliers.

    :param res_pen: Resistance penetration multiplier
    :type res_pen: list[float], optional
    :return: Res multiplier
    :rtype: float
    """
    return 1 if res_pen is None else 1 + sum(res_pen)


def calculate_def_multipliers(def_reduction_multiplier: list[float] = None) -> float:
    """
    Calculates DEF multipliers.

    :param def_reduction_multiplier: List of DEF reduction multipliers
    :type def_reduction_multiplier: list[float], optional
    :return: Final DEF reduction multiplier
    :rtype: float
    """
    return 1 if def_reduction_multiplier is None else 1 + sum(def_reduction_multiplier)


def calculate_break_effect(break_amount: int, break_effect: float) -> float:
    """
    Calculates break effect
    :param break_amount: Break amount.
    :param break_effect: Break effect.
    :return: Break amount
    """
    main_logger.info('Calculating break effect...')
    return break_amount * break_effect


def calculate_total_damage(
        base_dmg: float,
        dmg_multipliers: float,
        res_multipliers: float,
        dmg_reduction: float,
        def_reduction_multiplier: float) -> float:
    """
    Calculates total damage
    :param base_dmg: Base DMG.
    :param dmg_multipliers: DMG% Multipliers.
    :param res_multipliers: RES Multipliers.
    :param dmg_reduction: DMG Reduction Multipliers.
    :param def_reduction_multiplier: DEF Reduction Multipliers.
    :return: Total damage
    """
    main_logger.info('Calculating total damage...')
    return base_dmg * dmg_multipliers * def_reduction_multiplier * res_multipliers * dmg_reduction


def calculate_break_damage(break_type: str, target_max_toughness: int) -> float:
    """
    Calculates break damage
    :param break_type: Break DMG type, e.g., Physical, Fire, etc.
    :param target_max_toughness: Max toughness of the target.
    :return: Break DMG
    """
    main_logger.info('Calculating break damage...')
    level_80_multiplier = 3767

    if break_type == 'Physical' or break_type == 'Fire':
        base_multiplier = 2
    elif break_type == 'Ice' or break_type == 'Lightning':
        base_multiplier = 1
    elif break_type == 'Wind':
        base_multiplier = 1.5
    elif break_type == 'Quantum' or break_type == 'Imaginary':
        base_multiplier = 0.5
    else:
        base_multiplier = 1

    target_max_toughness_multiplier = 0.5 + (target_max_toughness / 40)
    return base_multiplier * level_80_multiplier * target_max_toughness_multiplier


def calculate_super_break_dmg(
        base_toughness_reduce: float,
        break_effect: float = 1) -> float:
    """
    Calculates super_break dmg
    :param base_toughness_reduce: Base toughness reduction.
    :param break_effect: Break Effect
    :return: Super Break dmg
    """
    main_logger.info('Calculating super_break dmg...')
    lvl_multiplier = 3767.5533
    return lvl_multiplier * (base_toughness_reduce / 10) * (1 + break_effect)


if __name__ == '__main__':
    pass
