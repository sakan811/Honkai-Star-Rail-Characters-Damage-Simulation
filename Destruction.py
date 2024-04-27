import random

from Character import Character


class ImbibitorLunae(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=102,
                 skill_multiplier=0,
                 ult_multiplier=3.0,
                 ult_energy=140,
                 ):
        super().__init__(
            atk,
            crit_rate,
            crit_dmg,
            elemental_dmg,
            speed,
            skill_multiplier,
            ult_multiplier,
            ult_energy
        )

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        dmg = 0

        if skill:
            if self.enhancement_amount == 1:
                self.righteous_heart += 3
                if self.enhancement_amount > 6:
                    self.righteous_heart = 6
                dmg = self.atk * 2.6
                self.current_ult_energy += 30
            elif self.enhancement_amount == 2:
                self.righteous_heart += 5
                if self.enhancement_amount > 6:
                    self.righteous_heart = 6
                dmg = self.atk * 3.8
                self.outroar += 1
                if self.outroar > 4:
                    self.outroar = 4
                self.current_ult_energy += 35
            elif self.enhancement_amount == 3:
                self.righteous_heart += 7
                if self.enhancement_amount > 6:
                    self.righteous_heart = 6
                dmg = self.atk * 5
                self.outroar += 3
                if self.outroar > 4:
                    self.outroar = 4
                self.current_ult_energy += 40

            if crit:
                crit_dmg = self.crit_dmg
                if self.outroar > 0:
                    crit_dmg += (0.12 * self.outroar)
                    dmg *= crit_dmg
                else:
                    dmg *= crit_dmg

                attack_imaginary_weakness_enemy = random.random() < 0.5
                if attack_imaginary_weakness_enemy:
                    crit_dmg += 0.24
                    dmg *= crit_dmg

            dmg *= self.elemental_dmg

            if self.righteous_heart > 0:
                dmg *= 1 + (0.1 * self.righteous_heart)

            self.results.append(dmg)
        else:
            self.righteous_heart += 3
            if self.enhancement_amount > 6:
                self.righteous_heart = 6

            dmg = self.atk * self.ult_multiplier

            if crit:
                crit_dmg = self.crit_dmg
                if self.outroar > 0:
                    crit_dmg += (0.12 * self.outroar)
                    dmg *= crit_dmg
                else:
                    dmg *= crit_dmg

                attack_imaginary_weakness_enemy = random.random() < 0.5
                if attack_imaginary_weakness_enemy:
                    crit_dmg += 0.24
                    dmg *= crit_dmg

            dmg *= self.elemental_dmg

            if self.righteous_heart > 0:
                dmg *= 1 + (0.1 * self.righteous_heart)

            self.results.append(dmg)

            self.current_ult_energy = 5

    def _reset_variables(self):
        self.outroar = 0
        self.righteous_heart = 0

    def _simulate_buff_duration_on_character(self):
        self.outroar = 0
        self.righteous_heart = 0

    def _set_scenario(self, enhancement_amount):
        # set a scenario when using only the given version of Enhanced Basic ATK
        self.enhancement_amount = enhancement_amount[0]

    def _simulate_enter_battle_effect(self):
        self.current_ult_energy += 15
