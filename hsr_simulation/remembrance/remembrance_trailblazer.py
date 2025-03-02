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


class RemembranceTrailblazer(Character):
    TRUE_DMG_MULTIPLIER: float = 0.28

    ULT_MULTIPLIER: float = 2.4
    ULT_BREAK_AMOUNT: int = 20
    ULT_MEM_CHARGE_GAIN: int = 40

    A2_TRACE_CHARGE_GAIN: int = 40
    A4_TRACE_CHARGE_GAIN: int = 5

    SKILL_MEM_CHARGE_GAIN: int = 10

    MEM_CRIT_DMG_BUFF_MULTIPLIER: float = 0.12
    MEM_CRIT_DMG_BUFF_PLUS: float = 0.24

    def __init__(self, speed: float = 103, ult_energy: int = 160):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.mem = None
        self.mem_buff = 0
        self.additional_true_dmg_multiplier = self._apply_a6_trace()

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats, along with all battle-related data,
        and the dictionary that store the character's actions' data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.mem = None
        self.mem_buff = 0
        self.additional_true_dmg_multiplier = self._apply_a6_trace()

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        # enemy's turn
        self._simulate_enemy_weakness_broken()

        if self.battle_start:
            # apply Mem's talent
            self.crit_dmg = self.default_crit_dmg + (
                (self.default_crit_dmg * self.MEM_CRIT_DMG_BUFF_MULTIPLIER)
                + self.MEM_CRIT_DMG_BUFF_PLUS
            )
            self._apply_a2_trace()
            self.battle_start = False

        # Trailblazer's turn
        if self.skill_points > 0 and self.mem is None:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self._can_use_ult():
            self._use_ult()

        # Mem's turn
        if self.mem is not None:
            if not self._mem_can_use_ult():
                hit_num = random.randint(1, 4)
                if self.mem.mem_buff > 0:
                    dmg = self.mem._use_skill(hit_num)
                    self._apply_a4_trace()
                    self._record_damage(dmg, "Mem Skill")
                    true_dmg = self.mem._simulate_true_dmg_from_skill(hit_num)
                    self._record_damage(true_dmg, "Mem True Damage")
                    self.mem.mem_buff -= 1
                else:
                    dmg = self.mem._use_skill(hit_num)
                    self._apply_a4_trace()
                    self._record_damage(dmg, "Mem Skill")
            else:
                self._apply_mem_true_dmg_buff()

    def _use_basic_atk(self) -> None:
        """Simulate basic attack damage."""
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        dmg = self._calculate_damage(
            skill_multiplier=self.BASIC_ATK_MULTIPLIER,
            break_amount=self.BASIC_ATK_BREAK_AMOUNT,
        )
        self._update_skill_point_and_ult_energy(1, self.BASIC_ATK_ENERGY_GAIN)
        self._record_damage(dmg, "Basic ATK")

        self._use_talent(self.BASIC_ATK_ENERGY_GAIN)  # 2% Charge

        if self.mem_buff > 0:
            self.mem_buff -= 1
            original_dmg = (
                self.atk
                * self.BASIC_ATK_MULTIPLIER
                * (self.TRUE_DMG_MULTIPLIER + self.additional_true_dmg_multiplier)
            )
            self._record_damage(original_dmg, "True Damage")

        if self._mem_can_use_ult():
            self._apply_mem_true_dmg_buff()

    def _use_skill(self) -> None:
        """Simulate skill damage."""
        main_logger.info(f"{self.__class__.__name__} is using skill...")
        if self.mem is None:
            self.mem = Mem(speed=130, ult_energy=100)
            self._gain_charge_to_mem(self.A2_TRACE_CHARGE_GAIN)

            # apply Mem's talent
            charge_gain = 50
            self._gain_charge_to_mem(charge_gain)
        else:
            self._gain_charge_to_mem(self.SKILL_MEM_CHARGE_GAIN)  # 10% Charge

        self._update_skill_point_and_ult_energy(-1, self.SKILL_ENERGY_GAIN)
        self._use_talent(self.SKILL_ENERGY_GAIN)  # 3% Charge

        if self._mem_can_use_ult():
            self._apply_mem_true_dmg_buff()

    def _use_ult(self) -> None:
        """Simulate ultimate damage."""
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        self._gain_charge_to_mem(self.ULT_MEM_CHARGE_GAIN)  # 40% Charge
        dmg = self._calculate_damage(
            skill_multiplier=self.ULT_MULTIPLIER, break_amount=self.ULT_BREAK_AMOUNT
        )
        self._record_damage(dmg, "Ultimate")

        if self.mem_buff > 0:
            self.mem_buff -= 1
            original_dmg = (
                self.atk
                * self.ULT_MULTIPLIER
                * (self.TRUE_DMG_MULTIPLIER + self.additional_true_dmg_multiplier)
            )
            self._record_damage(original_dmg, "True Damage")

        if self._mem_can_use_ult():
            self._apply_mem_true_dmg_buff()

        self.current_ult_energy = self.DEFAULT_ULT_ENERGY_AFTER_ULT

    def _use_talent(self, energy_gain: int) -> None:
        """
        Simulate talent effect, which gain charge to Mem based on energy_gain.
        :param energy_gain: Energy gain from ability
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using talent...")
        self.mem.ult_energy += energy_gain // 10
        if self.mem.ult_energy >= self.mem.MEM_CHARGE:
            self.mem_buff = self.mem._use_ult()

    def _gain_charge_to_mem(self, charge_gain: int) -> None:
        """
        Simulate gaining charge to Mem based on charge_gain.
        :param charge_gain: Charge gain
        :return: None
        """
        self.mem.ult_energy += charge_gain
        if self.mem.ult_energy >= self.mem.MEM_CHARGE:
            self.mem_buff = self.mem._use_ult()

    def _apply_a2_trace(self) -> None:
        """Simulate applying A2 Trace."""
        main_logger.info(f"{self.__class__.__name__} is applying A2 Trace...")
        self.char_action_value_for_action_forward.append(
            self.simulate_action_forward(0.3)
        )

    def _apply_a4_trace(self) -> None:
        """Simulate applying A4 Trace."""
        main_logger.info(f"{self.__class__.__name__} is applying A4 Trace...")
        self._gain_charge_to_mem(self.A4_TRACE_CHARGE_GAIN)

    def _apply_a6_trace(self) -> None:
        """Simulate applying A6 Trace."""
        main_logger.info(f"{self.__class__.__name__} is applying A6 Trace...")
        exceed_ult_energy = self.ult_energy - 100
        additional_true_dmg_multiplier = (exceed_ult_energy // 10) * 0.02
        return additional_true_dmg_multiplier

    def _mem_can_use_ult(self) -> bool:
        """Check if Mem can use ult."""
        return self.mem.ult_energy >= self.mem.MEM_CHARGE

    def _apply_mem_true_dmg_buff(self) -> None:
        """
        Apply Mem's True Damage Buff.
        If Trailblazer already has Mem's buff, then give Mem's buff to Mem itself.
        """
        main_logger.info(
            f"{self.__class__.__name__} is applying Mem's True Damage Buff..."
        )
        if self.mem_buff <= 0:
            self.mem_buff = self.mem._use_ult()
            self.char_action_value_for_action_forward.append(
                self.simulate_action_forward(1)
            )
        else:
            self.mem.mem_buff = self.mem._use_ult()


class Mem(Character):
    SKILL_MULTIPLIER: float = 0.36
    SKILL_MULTIPLIER_FINAL_HIT: float = 0.9
    SKILL_BREAK_AMOUNT: int = 5

    MEM_BUFF_DURATION: int = 3

    MEM_SPEED: int = 130
    MEM_CHARGE: int = 100

    TRUE_DMG_MULTIPLIER: float = 0.28

    def __init__(
        self,
        speed: float = MEM_SPEED,
        ult_energy: int = MEM_CHARGE,  # 100% Charge
    ):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.mem_buff = 0

    def _use_skill(self, hit_num: int) -> float:
        """
        Simulate skill damage.
        :param hit_num: Number of hits to simulate
        :return: Skill Damage
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")

        dmg = 0
        for _ in range(hit_num):
            dmg += self._calculate_damage(
                skill_multiplier=self.SKILL_MULTIPLIER,
                break_amount=self.SKILL_BREAK_AMOUNT,
            )

        dmg += self._calculate_damage(
            skill_multiplier=self.SKILL_MULTIPLIER_FINAL_HIT,
            break_amount=self.SKILL_BREAK_AMOUNT,
        )
        return dmg

    def _simulate_true_dmg_from_skill(self, hit_num: int) -> float:
        """
        Simulate True Damage from skill.
        :param hit_num: Number of hits to simulate
        :return: True Damage
        """
        main_logger.info(
            f"{self.__class__.__name__} is simulating True Damage from skill..."
        )

        dmg = 0
        for _ in range(hit_num):
            dmg += self.atk * self.SKILL_MULTIPLIER * (self.TRUE_DMG_MULTIPLIER)

        dmg += self.atk * self.SKILL_MULTIPLIER_FINAL_HIT * (self.TRUE_DMG_MULTIPLIER)
        return dmg

    def _use_ult(self) -> int:
        """
        Simulate Mem's Lemme! Help You!
        :return: 3 which means Mem's buff is active for 3 turns
        """
        main_logger.info(f"{self.__class__.__name__} is using ultimate...")
        self.ult_energy = 0
        return self.MEM_BUFF_DURATION
