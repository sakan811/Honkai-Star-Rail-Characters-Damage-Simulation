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

from hsr_simulation.configure_logging import configure_logging_with_file, main_logger
from hsr_simulation.character import Character
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, calculate_res_multipliers, \
    calculate_total_damage, calculate_universal_dmg_reduction

script_logger = configure_logging_with_file(log_dir='logs', log_file='sushang.log',
                                            logger_name='sushang', level='DEBUG')


class Sushang(Character):
    def __init__(self, atk=2000, crit_rate=0.5, crit_dmg=1, speed=107, ult_energy=120):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.talent_spd_buff = 0
        self.starting_spd = speed
        self.ult_buff = 0
        self.a4_trace_buff = 0

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')

        # reset stats when begins a new action
        self.speed = self.starting_spd
        self.a4_trace_buff = 0
        self.char_action_value = []
        self.atk = 2000

        # talend speed buff only lasts for 2 turns
        if self.talent_spd_buff > 0:
            self.speed = self.starting_spd * 1.2
            self.talent_spd_buff -= 1
        else:
            self.speed = self.starting_spd

        if self.ult_buff > 0:
            self.atk *= 1.3
            self.ult_buff -= 1

        if self.skill_points > 0:
            self._use_skill()

            # simulate ultimate buff
            if self.ult_buff > 0:
                self._handle_sword_stance()

                # extra Sword Stance
                for _ in range(2):
                    self._handle_sword_stance(is_extra=True)
            else:
                self._handle_sword_stance()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

            self.current_ult_energy = 5

            self.ult_buff = 2

            # action again
            self.char_action_value.append(self.simulate_action_forward(action_forward_percent=1))

    def _handle_a4_trace(self, sword_stance_dmg) -> float:
        script_logger.info('Handling A4 Trace buff...')
        if sword_stance_dmg > 0:
            self.a4_trace_buff += 1
            sword_stance_dmg *= (1 + (0.025 * self.a4_trace_buff))
        return sword_stance_dmg

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        script_logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(is_basic_atk=True, skill_multiplier=1, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info("Using skill...")
        dmg, break_amount = self._calculate_damage(is_skill=True, skill_multiplier=2.1, break_amount=20)
        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Skill')

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        script_logger.info('Using ultimate...')
        ult_dmg, break_amount = self._calculate_damage(skill_multiplier=3.2, break_amount=30)

        self.enemy_toughness -= break_amount

        self.data['DMG'].append(ult_dmg)
        self.data['DMG_Type'].append('Ultimate')

    def _handle_sword_stance(self, is_extra: bool = False) -> None:
        """
        Simulate sword stance damage.
        :param is_extra: Whether the sword stance is an extra trigger.
        :return: None
        """
        script_logger.info("Using sword stance...")
        if self.is_enemy_weakness_broken():
            dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=0)
            sword_stance_dmg = self._handle_a4_trace(dmg)

            self.enemy_toughness -= break_amount
        else:
            if random.random() < 0.33:
                if is_extra:
                    dmg, break_amount = self._calculate_damage(skill_multiplier=0.5, break_amount=0)
                    sword_stance_dmg = self._handle_a4_trace(dmg)

                    self.enemy_toughness -= break_amount
                else:
                    dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=0)
                    sword_stance_dmg = self._handle_a4_trace(dmg)

                    self.enemy_toughness -= break_amount
            else:
                sword_stance_dmg = 0

        self.data['DMG'].append(sword_stance_dmg)
        self.data['DMG_Type'].append('Talent')

    def _calculate_damage(
            self,
            is_skill: bool = False,
            is_basic_atk: bool = False,
            skill_multiplier: float = 0,
            break_amount: int = 0,
            dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None,
            can_crit: bool = True) -> tuple[float, int]:
        """
        Calculates damage based on multipliers.
        :param is_skill: Whether the skill is the trigger.
        :param is_basic_atk: Whether the basic atk is the trigger.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage and break amount.
        """
        script_logger.info(f'{self.__class__.__name__}: Calculating damage...')
        weakness_broken = self.is_enemy_weakness_broken()

        # simulate Talent Speed buff
        if weakness_broken:
            self.speed *= 1.2
            self.talent_spd_buff = 2

        # simulate A6 trace
        if is_skill or is_basic_atk:
            if weakness_broken:
                self.char_action_value.append(self.simulate_action_forward(action_forward_percent=0.15))

        if random.random() < self.crit_rate and can_crit:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(crit_dmg=self.crit_dmg, dmg_multipliers=dmg_multipliers)
        else:
            base_dmg = calculate_base_dmg(atk=self.atk, skill_multiplier=skill_multiplier)
            dmg_multiplier = calculate_dmg_multipliers(dmg_multipliers=dmg_multipliers)

        dmg_reduction = calculate_universal_dmg_reduction(weakness_broken)
        res_multiplier = calculate_res_multipliers(res_multipliers)
        total_dmg = calculate_total_damage(base_dmg, dmg_multiplier, res_multiplier, dmg_reduction)

        return total_dmg, break_amount
