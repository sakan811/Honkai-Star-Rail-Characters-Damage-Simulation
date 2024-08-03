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
from hsr_simulation.dmg_calculator import calculate_base_dmg, calculate_dmg_multipliers, \
    calculate_universal_dmg_reduction, calculate_total_damage, calculate_res_multipliers

script_logger = configure_logging_with_file(log_dir='logs', log_file='march7th_hunt.log',
                                          logger_name='march7th_hunt', level='DEBUG')


class March7thHunt(Character):
    def __init__(
            self,
            atk: int = 2000,
            crit_rate: float = 0.5,
            crit_dmg: float = 1.0,
            speed: float = 102,
            ult_energy: int = 110
    ):
        super().__init__(atk, crit_rate, crit_dmg, speed, ult_energy)
        self.has_shifu = False
        self.charge = 0
        self.ult_buff = False
        self.talent_buff = False
        self.battle_start = True
        self.shifu = None

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f'{self.__class__.__name__} is taking actions...')
        self._sim_shifu()

        # reset stats
        self.speed = 102
        self.char_action_value = []

        # simulate A2 Trace
        if self.battle_start:
            self.battle_start = False
            self.speed *= 1.25

        if self.skill_points > 0 and not self.has_shifu:
            self._use_skill()
        elif self.has_shifu and self.charge >= 7:
            self.talent_buff = True

            # simulate immediate action
            self.char_action_value.append(self.simulate_action_forward(action_forward_percent=1))

            # check if ult can be used
            if self._can_use_ult():
                self._use_ult()
                self.current_ult_energy = 5

            self.charge = 0
            self._enhanced_basic_atk()

            self.talent_buff = False
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()
            self.current_ult_energy = 5

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        :return: None
        """
        script_logger.info("Using basic attack...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=1, break_amount=10)

        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Basic ATK')

        if self.shifu == 'DMG':
            self._additional_dmg()
        else:
            break_amount *= 2

        self.enemy_toughness -= break_amount

        self.charge += 1

    def _use_skill(self) -> None:
        """
        Simulate skill damage.
        :return: None
        """
        script_logger.info("Using skill...")
        self.has_shifu = True

        self._update_skill_point_and_ult_energy(skill_points=-1, ult_energy=30)

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage.
        :return: None
        """
        script_logger.info('Using ultimate...')
        if self.talent_buff:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.4, break_amount=30, dmg_multipliers=[0.8])
            self.enemy_toughness -= break_amount
        else:
            dmg, break_amount = self._calculate_damage(skill_multiplier=2.4, break_amount=30)
            self.enemy_toughness -= break_amount

        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Ultimate')

        self.ult_buff = True

    def _additional_dmg(self) -> None:
        """
        Simulate additional damage from SKill.
        :return: None
        """
        script_logger.info("Simulating additional damage from skill...")
        dmg, break_amount = self._calculate_damage(skill_multiplier=0.2, break_amount=0)
        self.data['DMG'].append(dmg)
        self.data['DMG_Type'].append('Additional DMG')

    def _enhanced_basic_atk(self) -> None:
        """
        Use enhanced basic ATK
        :return: None
        """
        script_logger.info("Using enhanced basic ATK...")
        extra_hit_chance = 0.6
        if self.ult_buff:
            self.ult_buff = False
            initial_hit_num = 5
            extra_hit_chance = 0.8
        else:
            initial_hit_num = 3

        for _ in range(initial_hit_num):
            dmg, break_amount = self._calculate_damage(skill_multiplier=0.8, break_amount=5, dmg_multipliers=[0.8])

            self.data['DMG'].append(dmg)
            self.data['DMG_Type'].append('Enhanced Basic ATK')

            if self.shifu == 'DMG':
                self._additional_dmg()
            else:
                break_amount *= 2

            self.enemy_toughness -= break_amount

        # Attempt to deal extra hits
        max_extra_hits = 3
        extra_hits = 0
        while extra_hits < max_extra_hits:
            if random.random() < extra_hit_chance:
                dmg, break_amount = self._calculate_damage(skill_multiplier=0.8, break_amount=5, dmg_multipliers=[0.8])

                self.data['DMG'].append(dmg)
                self.data['DMG_Type'].append('Enhanced Basic ATK')

                if self.shifu == 'DMG':
                    self._additional_dmg()
                else:
                    break_amount *= 2

                self.enemy_toughness -= break_amount

                extra_hits += 1
            else:
                break

        self._update_skill_point_and_ult_energy(skill_points=0, ult_energy=30)

    def _sim_shifu(self) -> None:
        """
        Simulate March 7th's Shifu.
        :return: None
        """
        script_logger.info("Simulating Shifu...")
        self.charge += 1

        # random break amount
        break_amount = random.choice([10, 20])
        self.enemy_toughness -= break_amount

        # simulate Shifu using Ultimate
        if random.random() < 0.25:
            self.charge += 1
            self.enemy_toughness -= 30

    def set_shifu(self) -> None:
        """
        Set March 7th's Shifu
        :return: None
        """
        script_logger.info('Setting Shifu...')
        choice = random.choice(['DMG', 'SUPPORT'])
        self.shifu = choice
        script_logger.debug(f'Current Shifu is {self.shifu} Type')

    def _calculate_damage(
            self,
            skill_multiplier: float,
            break_amount: int,
            dmg_multipliers: list[float] = None,
            res_multipliers: list[float] = None,
            can_crit: bool = True) -> tuple[float, int]:
        """
        Calculates damage based on multipliers.
        :param skill_multiplier: Skill multiplier.
        :param break_amount: Break amount that the attack can do.
        :param dmg_multipliers: DMG multipliers.
        :param res_multipliers: RES multipliers.
        :param can_crit: Whether the DMG can CRIT.
        :return: Damage and break amount.
        """
        script_logger.info(f'{self.__class__.__name__}: Calculating damage...')
        weakness_broken = self.is_enemy_weakness_broken()
        if weakness_broken:
            self.do_break_dmg(break_type='Imaginary')

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