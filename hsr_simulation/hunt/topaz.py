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
import random

from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, \
    calculate_universal_dmg_reduction, calculate_def_multipliers, calculate_res_multipliers, calculate_total_damage


class Topaz(Character):
    def __init__(
            self,
            speed: float = 110,
            ult_energy: int = 130
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.windfall_bonanza = 0
        self.numby = None

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} data...')
        super().reset_character_data_for_each_battle()
        self.numby = None
        self.windfall_bonanza = 0

    def summon_numby(self, topaz: 'Topaz', speed: int = 80) -> 'Numby':
        """
        Summon Numby.
        :param topaz: Topaz character.
        :param speed: Numby's speed.
        :return: Numby object.
        """
        main_logger.info('Summon Numby...')
        self.numby = Numby(topaz=topaz, speed=speed, ult_energy=0)
        return self.numby

    @staticmethod
    def enemy_has_fire_weakness() -> bool:
        main_logger.info('Whether the enemy has fire weakness...')
        if random.random() < 0.5:
            return True
        else:
            return False

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.enemy_has_fire_weakness()

            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None.
        """
        main_logger.info("Using basic attack...")
        if self.enemy_has_fire_weakness():
            dmg = self._calculate_damage(skill_multiplier=1, break_amount=10, dmg_multipliers=[0.15])
        else:
            dmg = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        # Numby action forward
        self.numby.summon_action_value_for_action_forward.append(
            self.numby.simulate_action_forward(action_forward_percent=0.5)
        )

        self._record_damage(dmg, 'Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        main_logger.info("Using skill...")
        if self.enemy_has_fire_weakness():
            dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                         dmg_multipliers=[0.5, 0.15])
        else:
            dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20, dmg_multipliers=[0.5])
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        # Numby action forward
        self.numby.summon_action_value_for_action_forward.append(
            self.numby.simulate_action_forward(action_forward_percent=0.5)
        )

        self._record_damage(dmg, 'Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: Damage and break amount.
        """
        main_logger.info('Using ultimate...')
        self.windfall_bonanza = 2


def random_ally_follow_up_atk() -> bool:
    """
    Simulate random follow-up atk from ally.
    :return: Whether an ally does follow-up attack
    """
    main_logger.info('Random ally follow-up atk...')
    # random number of allies that can do follow up attack
    follow_up_atk_ally_num = random.choice([0, 1])

    if random.random() < (0.33 * follow_up_atk_ally_num):
        main_logger.debug('Ally does follow-up atk')
        return True
    else:
        return False


class Numby(Character):
    def __init__(
            self,
            topaz: Topaz,
            speed: float = 80,
            ult_energy: int = 0
    ):
        super().__init__(
            atk=topaz.atk,
            crit_rate=topaz.crit_rate,
            crit_dmg=topaz.crit_dmg,
            speed=speed,
            ult_energy=ult_energy
        )
        self.windfall_bonanza_attacks = 0
        self.topaz = topaz
        self.is_test = False

    def set_test(self, is_test: bool) -> None:
        """
        Set whether the test is running.
        :param is_test: Whether the test is running.
        :return: None
        """
        self.is_test = is_test

    def _numby_attack(self, with_ult_buff: bool = False) -> None:
        """
        Simulate Numby's attack
        :param with_ult_buff: Whether Numby has Ult buff.
        :return: None
        """
        if with_ult_buff:
            main_logger.info('Numby attacking with Ult buff...')
            if self.topaz.enemy_has_fire_weakness():
                dmg = self._calculate_damage(skill_multiplier=3, break_amount=20,
                                             dmg_multipliers=[0.15])

                dmg = self._calculate_damage(skill_multiplier=3, break_amount=20)

                self._record_damage(dmg, 'Numby with Ult Buff')
        else:
            main_logger.info('Numby attacking...')
            if self.topaz.enemy_has_fire_weakness():
                dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20,
                                             dmg_multipliers=[0.15])

                self._record_damage(dmg, 'Numby')
            else:
                dmg = self._calculate_damage(skill_multiplier=1.5, break_amount=20)

                self._record_damage(dmg, 'Numby')

    def take_action(self) -> None:
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        if self.topaz.windfall_bonanza > 0:
            self.crit_dmg += 0.25

            self._numby_attack(with_ult_buff=True)

            self.topaz.windfall_bonanza -= 1
            self.topaz.current_ult_energy += 15
        else:
            self._numby_attack()

            self.topaz.current_ult_energy += 5

        # Simulate ally's follow-up attacks
        if self.topaz.windfall_bonanza > 0:
            # random number of allies to attack
            follow_up_atk_ally_num = random.choice([1, 2])

            # Numby action forward
            self.summon_action_value_for_action_forward.append(
                self.simulate_action_forward(action_forward_percent=0.5 * follow_up_atk_ally_num)
            )
        else:
            if random_ally_follow_up_atk():
                # Numby action forward
                self.summon_action_value_for_action_forward.append(
                    self.simulate_action_forward(action_forward_percent=0.5)
                )

        # for testing turn count
        if self.is_test:
            self.summon_action_value_for_action_forward = []

    def reset_summon_stat_for_each_turn(self) -> None:
        """
        Reset Numby stats
        :return: None
        """
        main_logger.info(f'Resetting {self.__class__.__name__} stats ...')
        super().reset_summon_stat_for_each_turn()
        self.crit_dmg = 1

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            dot_dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None,
            def_reduction_multiplier: list[float] = None,
            can_crit: bool = True) -> float:
        """
        Calculates damage based on multipliers.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param dot_dmg_multipliers: Dot DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param def_reduction_multiplier: DEF reduction multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage.
        """
        main_logger.info(f'{self.__class__.__name__}: Calculating damage...')
        # reduce enemy toughness
        self.topaz.current_enemy_toughness -= break_amount

        self.topaz.check_if_enemy_weakness_broken()

        base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)

        if random.random() < self.crit_rate and can_crit:
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
        else:
            dmg_multiplier = calculate_dmg_multipliers(dmg_multipliers=dmg_multipliers, dot_dmg=dot_dmg_multipliers)

        dmg_reduction = calculate_universal_dmg_reduction(self.topaz.enemy_weakness_broken)
        def_reduction = calculate_def_multipliers(def_reduction_multiplier=def_reduction_multiplier)
        res_multiplier = calculate_res_multipliers(res_multipliers)

        total_dmg = calculate_total_damage(base_dmg=base_dmg, dmg_multipliers=dmg_multiplier,
                                           res_multipliers=res_multiplier, dmg_reduction=dmg_reduction,
                                           def_reduction_multiplier=def_reduction)

        return total_dmg


if __name__ == '__main__':
    pass
