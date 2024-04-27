import random

from Character import Character


class Seele(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=115,
                 skill_multiplier=2.2,
                 ult_multiplier=4.25,
                 ult_energy=120
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
        if skill:
            dmg = self.atk * self.skill_multiplier
        else:
            dmg = self.atk * self.ult_multiplier

        if crit:
            dmg *= self.crit_dmg

        dmg *= self.elemental_dmg
        if self.talent > 0:
            dmg *= 1.8

        #  simulate A4 Trace
        if self.resurgence:
            dmg *= 1.2

        if skill:
            self.current_ult_energy += 30
        elif ult:
            self.current_ult_energy = 5
        self.results.append(dmg)

    def _simulate_actions_during_each_turn(self):
        crit = random.random() < self.crit_rate
        self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

        #  simulate Resurgence state
        if self.seele_with_resurgence:
            if not self.resurgence:
                self.resurgence = random.random() < 0.5
            else:
                self.resurgence = False
            if self.resurgence:
                talent_duration = 1
                #  +1 as the buff should last to the next turn
                self.talent = talent_duration + 1
                self.current_ult_energy += 10
                self._simulate_actions_during_each_turn()

        if self.current_ult_energy >= 120:
            self._simulate_skill_and_ult(skill=False, ult=True, crit=crit)

    def _simulate_total_turns_from_given_cycles(self, cycles: int):
        char_action_value = 10000 / self.speed
        cycles_action_value = 150 + (100 * (cycles - 1))
        turns = cycles_action_value / char_action_value
        turns = int(turns)
        for turn in range(1, turns + 1):
            self._simulate_actions_during_each_turn()
            if self.talent > 0:
                self.talent -= 1

    def _reset_variables(self):
        self.talent = 0
        self.resurgence = False

    def _set_scenario(self, with_resurgence):
        # set Resurgence scenarios
        self.seele_with_resurgence: bool = with_resurgence[0]


class DanHeng(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=110,
                 skill_multiplier=2.6,
                 ult_multiplier=4,
                 ult_energy=120
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
        talent = False

        if self.talent_buff > 0:
            self.talent_buff -= 1
        else:
            if self.support_ally:
                talent = random.choice([True, False])

        ult_multiplier = self.ult_multiplier

        if self.enemy_debuff > 0:
            ult_multiplier += 1.2
            self.enemy_debuff -= 1

        if skill:
            dmg = self.atk * self.skill_multiplier
        else:
            dmg = self.atk * ult_multiplier

        if crit:
            dmg *= self.crit_dmg
            self.enemy_debuff = 2

        result = self.elemental_dmg * dmg

        if talent:
            result *= 1.36
            self.talent_buff = 2

        if skill:
            self.current_ult_energy += 30
        elif ult:
            self.current_ult_energy = 5
        self.results.append(result)

    def _reset_variables(self):
        self.enemy_debuff = 0
        self.talent_buff = 0

    def _simulate_enter_battle_effect(self):
        self.support_ally = random.random() < 0.5


class SuShang(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=107,
                 skill_multiplier=2.1,
                 ult_multiplier=3.2,
                 ult_energy=120,
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
        atk = self.atk
        if self.buff > 0:
            atk = self.atk * 1.3
            self.buff -= 1

        total_follow_up_dmg = 0
        if skill:
            #  simulate Sword Stance
            follow_up_dmg = random.random() < 0.33
            if follow_up_dmg:
                self.a4_trace_buff += 1
                if self.a4_trace_buff > 10:
                    self.a4_trace_buff = 10
                dmg = atk * self.skill_multiplier
                follow_up_dmg = atk
                follow_up_crit = random.random() < self.crit_rate
                if follow_up_crit:
                    follow_up_dmg *= self.crit_dmg
                follow_up_dmg *= self.elemental_dmg

                #  simulate A4 Trace
                if self.a4_trace_buff > 0:
                    follow_up_dmg *= 1 + (0.025 * self.a4_trace_buff)
                total_follow_up_dmg = follow_up_dmg

                #  simulate extra Sword Stance
                if self.buff > 0:
                    for _ in range(2):
                        follow_up_dmg = random.random() < 0.33
                        if follow_up_dmg:
                            follow_up_dmg = atk
                            follow_up_crit = random.random() < self.crit_rate
                            if follow_up_crit:
                                follow_up_dmg *= self.crit_dmg
                            follow_up_dmg *= self.elemental_dmg
                            follow_up_dmg /= 2
                            total_follow_up_dmg += follow_up_dmg
            else:
                dmg = atk * self.skill_multiplier
        else:
            dmg = atk * self.ult_multiplier
            self.buff = 2

        if crit:
            dmg *= self.crit_dmg

        result = self.elemental_dmg * dmg
        result += total_follow_up_dmg

        if skill:
            self.current_ult_energy += 30
        elif ult:
            self.current_ult_energy = 5
        self.results.append(result)

    def _simulate_actions_during_each_turn(self):
        crit = random.random() < self.crit_rate
        self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

        if self.current_ult_energy >= self.ult_energy:
            self._simulate_skill_and_ult(skill=False, ult=True, crit=crit)
            self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

    def _reset_variables(self):
        self.buff = 0
        self.a4_trace_buff = 0


class YanQing(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=109,
                 skill_multiplier=2.2,
                 ult_multiplier=3.5,
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
        self.soulsteel_sync -= 1
        crit_rate = self.crit_rate
        crit_dmg = self.crit_dmg
        crit = random.random() < self.crit_rate
        dmg = 0

        if skill:
            dmg = self.atk * self.skill_multiplier
            freeze_enemy = random.random() < 0.65
            if freeze_enemy:
                freeze_duration = 1
                #  +1 as it should last to the enemy's next turn
                self.freeze_enemy = freeze_duration + 1
        else:
            dmg = self.atk * self.ult_multiplier
            ult_buff_duration = 1
            #  +1 as it should last to the next turn
            self.ult_buff = ult_buff_duration + 1

        if self.ult_buff > 0:
            crit_rate += 0.6
            crit = random.random() < crit_rate
            crit_dmg += 0.5
            self.ult_buff -= 1

        follow_up_dmg = 0
        if self.soulsteel_sync > 0:
            crit_rate += 0.2
            crit = random.random() < crit_rate
            crit_dmg += 0.3
            follow_up = random.random() < 0.6
            if follow_up:
                follow_up_dmg = self.atk * 0.5
                if crit:
                    follow_up_dmg *= crit_dmg
                follow_up_dmg *= self.elemental_dmg

                self.current_ult_energy += 10

        if crit:
            dmg *= self.crit_dmg

        dmg *= self.elemental_dmg

        #  simulate extra damage from A2 Trace
        extra_dmg = 0
        if self.attack_ice_weakness_enemy:
            extra_dmg = self.atk * 0.3
            crit = random.random() < crit_rate
            if crit:
                extra_dmg *= crit_dmg
            extra_dmg *= self.elemental_dmg

        result = dmg + follow_up_dmg + extra_dmg

        if skill:
            soulsteel_sync_duration = 1
            #  +1 as it should last to the next turn
            self.soulsteel_sync = soulsteel_sync_duration + 1
            self.current_ult_energy += 30
        elif ult:
            self.current_ult_energy = 5

        self.results.append(result)

    def _simulate_actions_during_each_turn(self):
        #  simulate A2 Trace
        ice_enemy = random.random() < 0.5
        if ice_enemy:
            self.attack_ice_weakness_enemy = True

        self._simulate_skill_and_ult(skill=True, ult=False, crit=False)

        #  simulate A2 Trace
        ice_enemy = random.random() < 0.5
        if ice_enemy:
            self.attack_ice_weakness_enemy = True

        if self.current_ult_energy >= self.ult_energy:
            self._simulate_skill_and_ult(skill=False, ult=True, crit=False)

    def _reset_variables(self):
        self.ult_buff = 0
        self.soulsteel_sync = 0
        self.attack_ice_weakness_enemy = False
        self.freeze_enemy = 0

    def _simulate_enemy_turn(self):
        if self.freeze_enemy > 0:
            dmg = self.atk * 0.5 * self.elemental_dmg
            self.results.append(dmg)
            self.freeze_enemy -= 1
        else:
            if not self.with_shield:
                #  simulate scenario where Yanqing receive DMG
                enemy_attack = random.random() < 0.5
                if enemy_attack:
                    self.soulsteel_sync = 0

    def _simulate_enter_battle_effect(self):
        self.with_shield = random.random() < 0.5


class Numby(Character):
    def __init__(self,
                 atk=3000 * 1.5,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=80,
                 skill_multiplier=1.5,
                 ult_multiplier=0,
                 ult_energy=0,
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
        crit = random.random() < self.crit_rate

        if self.ult_buff:
            crit_dmg = self.crit_dmg + 0.25
            multiplier = self.skill_multiplier * 1.5
            numby_dmg = self.atk * multiplier

            if crit:
                numby_dmg *= crit_dmg

            result = self.elemental_dmg * numby_dmg

            #  simulate A4 Trace
            if self.attack_enemy_with_fire_weakness:
                result *= 1.15
        else:
            multiplier = self.skill_multiplier
            numby_dmg = self.atk * multiplier

            if crit:
                numby_dmg *= self.crit_dmg

            result = self.elemental_dmg * numby_dmg

            #  simulate A4 Trace
            if self.attack_enemy_with_fire_weakness:
                result *= 1.15

        self.results.append(result)

    def _reset_variables(self):
        self.attack_enemy_with_fire_weakness = False

    def _set_scenario(self, ult_buff):
        # set scenario where Numby has Ult buff
        # and scenario where Numby does not
        self.ult_buff: bool = ult_buff[0]


class DrRatio(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=103,
                 skill_multiplier=1.5,
                 ult_multiplier=2.4,
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
        follow_up_dmg = 0
        crit_rate = 0
        crit_dmg = 0
        enemy_debuff = 0

        if skill:
            dmg = self.atk * self.skill_multiplier

            enemy_debuff = self.enemy_with_debuff

            follow_up_chance = 0.4
            if enemy_debuff > 0:
                follow_up_chance = 0.4 + (0.2 * enemy_debuff)

                #  simulate A2 Trace
                crit_rate = self.crit_rate + (0.025 * enemy_debuff)
                crit_dmg = self.crit_dmg + (0.05 * enemy_debuff)

            follow_up = random.random() < follow_up_chance
            if follow_up:
                follow_up_dmg = self.atk * 2.7
                crit = random.random() < crit_rate
                if crit:
                    follow_up_dmg *= crit_dmg
                follow_up_dmg *= self.elemental_dmg

                #  simulate A6 Trace
                if enemy_debuff >= 3:
                    follow_up_dmg *= 1 + (0.1 * enemy_debuff)

                dmg += follow_up_dmg
                self.current_ult_energy += 5

        else:
            dmg = self.atk * self.ult_multiplier
            self.ult_buff = 2

        if crit:
            dmg *= self.crit_dmg

        if self.ult_buff > 0:
            follow_up_dmg = self.atk * 2.7
            crit = random.random() < crit_rate
            if crit:
                follow_up_dmg *= crit_dmg
            follow_up_dmg *= self.elemental_dmg
            self.current_ult_energy += 5
            self.ult_buff -= 1

        dmg *= self.elemental_dmg

        #  simulate A6 Trace
        if enemy_debuff >= 3:
            dmg *= 1 + (0.1 * enemy_debuff)

        result = dmg + follow_up_dmg

        if skill:
            self.current_ult_energy += 30
        elif ult:
            self.current_ult_energy = 5
        self.results.append(result)

    def _reset_variables(self):
        self.ult_buff = 0

    def _set_scenario(self, debuff):
        # set how many debuff are there on an enemy
        self.enemy_with_debuff: int = debuff[0]
