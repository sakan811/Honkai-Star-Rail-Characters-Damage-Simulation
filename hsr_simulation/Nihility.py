import random

from hsr_simulation.character import Character


class Kafka(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=100,
                 skill_multiplier=1.6,
                 ult_multiplier=0.8,
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

        result = self.elemental_dmg * dmg

        if skill:
            if self.shock > 0:
                shock_dmg = self.atk * 2.9 * 0.75 * self.elemental_dmg
                shock_dmg *= self.shock
                result += shock_dmg
            self.current_ult_energy += 30
        elif ult:
            self.shock = 1
            if self.shock > 0:
                shock_dmg = self.atk * 2.9 * self.elemental_dmg
                shock_dmg *= self.shock
                result += shock_dmg
            self.current_ult_energy = 5

        #  simulate Basic ATK from an ally that triggers Kafka's talent
        basic_atk = random.choice([True, False])
        if basic_atk:
            follow_up_atk = self.atk * 1.4
            crit = random.random() < self.crit_rate
            if crit:
                follow_up_atk *= self.crit_dmg
            follow_up_atk *= self.elemental_dmg
            result += follow_up_atk
            self.shock = 1
            self.current_ult_energy += 10

        self.total_dmg.append(result)

    def _reset_variables(self):
        self.shock = 0
        self.shock_duration = 0

    def _simulate_enemy_turn(self):
        shock_dmg = 0
        if self.shock > 0:
            shock_dmg = self.atk * 2.9 * self.elemental_dmg
            shock_dmg *= self.shock
            #  simulate killing enemy with Shock
            enemy_killed = random.choice([True, False])
            if enemy_killed:
                self.current_ult_energy += 5

        self.total_dmg.append(shock_dmg)

    def _simulate_debuff_duration_on_enemy(self):
        #  simulate Shock debuff duration
        if self.shock > 0:
            self.shock_duration += 1
            if self.shock_duration >= 2:
                self.shock -= 1
                self.shock_duration = 0


class BlackSwan(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=102,
                 skill_multiplier=0.9,
                 ult_multiplier=1.2,
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

    def _simulate_ally_turn(self):
        #  simulate A4 Trace
        ally_attack = random.choice([True, False])
        if ally_attack:
            arcana = random.random() < 0.65 * (1 + self.effect_hit_rate)
            if arcana:
                arcana_stack = random.choice([1, 2, 3])
                self.arcana_stack += arcana_stack
                if self.arcana_stack > 50:
                    self.arcana_stack = 50

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        if skill:
            #  simulate Def reduction debuff from Skill
            if self.def_reduce > 0:
                dmg = self.atk * self.skill_multiplier * 1.208
            else:
                dmg = self.atk * self.skill_multiplier

            #  simulate Arcana inflicting chance from Skill
            self.arcana_stack += 1
            if self.arcana_stack > 50:
                self.arcana_stack = 50

            #  simulate A2 Trace
            enemy_dot_debuffed = random.choice([True, False])
            if enemy_dot_debuffed:
                arcana = random.random() < 0.65 * (1 + self.effect_hit_rate)
                if arcana:
                    self.arcana_stack += 1
                    if self.arcana_stack > 50:
                        self.arcana_stack = 50

            #  simulate Arcana's Def reduction debuff's inflicting chance from Skill
            self.def_reduce = 3
        else:
            self.epiphany = 2
            self.arcana_reset = 1
            dmg = self.atk * self.ult_multiplier

        if crit:
            dmg *= self.crit_dmg

        result = self.elemental_dmg * dmg

        if skill:
            self.current_ult_energy += 30
        elif ult:
            self.current_ult_energy = 5

        self.total_dmg.append(result)

    def _simulate_enemy_turn(self):
        if self.arcana_stack > 50:
            self.arcana_stack = 50

        arcana_dmg = self.atk * (2.4 + (self.arcana_stack * 0.12)) * self.elemental_dmg

        #  simulate Ult effect
        if self.epiphany > 0:
            arcana_dmg *= self.arcana_stack

        #  simulate Talent effect
        if self.arcana_stack >= 7:
            arcana_dmg *= 1.2

        #  simulate Ult effect
        if self.epiphany > 0:
            arcana_dmg *= 1.25
            self.epiphany -= 1

        #  simulate Ult effect
        if self.arcana_reset > 0:
            self.arcana_reset -= 1
        else:
            self.arcana_stack = 1

        #  simulate Skill effect
        if self.def_reduce > 0:
            arcana_dmg *= 1.208
            self.def_reduce -= 1

        self.current_ult_energy += 5

        arcana_dmg *= self.increased_dmg_from_effect_hit_rate

        self.total_dmg.append(arcana_dmg)

        if self.arcana_stack > 0:
            arcana = random.random() < 0.65 * (1 + self.effect_hit_rate)
            if arcana:
                self.arcana_stack += 1

    def _reset_variables(self):
        self.arcana_stack = 0
        self.def_reduce = 0
        self.epiphany = 0
        self.arcana_reset = 0

    def _simulate_enter_battle_effect(self):
        #  simulate Black Swan's Effect Hit Rate
        self.effect_hit_rate = random.uniform(0.1, 1.2)

        #  simulate A4 Trace
        arcana = random.random() < 0.65 * (1 + self.effect_hit_rate)
        if arcana:
            self.arcana_stack += 1

        #  simulate A6 Trace
        self.increased_dmg_from_effect_hit_rate = self.effect_hit_rate * 0.6


class Acheron(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=102,
                 skill_multiplier=1.6,
                 ult_multiplier=0,
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

    def _simulate_crimson_knot(self) -> None:
        #  simulate Crimson Knot damage
        crimson_knot_dmg = self.atk * (0.15 + (0.15 * self.crimson_knot_removed))
        crit = random.random() < self.crit_rate

        if crit:
            crimson_knot_dmg *= self.crit_dmg
        crimson_knot_dmg *= self.elemental_dmg

        #  simulate A6 Trace buff
        if self.a6_buff_stack > 0:
            crimson_knot_dmg *= (1 + (0.3 * self.a6_buff_stack))

        #  simulate Talent effect
        crimson_knot_dmg *= 1.2

        self.crimson_knot_dmg_list.append(crimson_knot_dmg)

    def _simulate_rainblade(self) -> None:
        #  simulate Rainblade 3 times
        for _ in range(3):
            #  simulate Rainblade
            rainblade_dmg = self.atk * 0.24
            crit = random.random() < self.crit_rate
            if crit:
                rainblade_dmg *= self.crit_dmg
            rainblade_dmg *= self.elemental_dmg
            #  simulate A6 Trace buff
            if self.a6_buff_stack > 0:
                rainblade_dmg *= (1 + (0.3 * self.a6_buff_stack))

            #  simulate A6 Trace buff
            if self.crimson_knot > 0:
                self.a6_buff_stack += 1
                if self.a6_buff_stack > 3:
                    self.a6_buff_stack = 3

            #  simulate Talent effect
            rainblade_dmg *= 1.2

            #  simulate removing Crimson Knot after Rainblade
            if self.crimson_knot >= 3:
                self.crimson_knot -= 3
                self.crimson_knot_removed = 3
            else:
                self.crimson_knot_removed = self.crimson_knot
                self.crimson_knot = 0

    def _simulate_stygian_resurge(self) -> float:
        #  simulate Stygian Resurge
        stygian_resurge = self.atk * 1.2
        crit = random.random() < self.crit_rate
        if crit:
            stygian_resurge *= self.crit_dmg
        stygian_resurge *= self.elemental_dmg

        self.crimson_knot_removed = self.crimson_knot
        self.crimson_knot = 0

        #  simulate A6 Trace buff
        if self.a6_buff_stack > 0:
            stygian_resurge *= (1 + (0.3 * self.a6_buff_stack))

        #  simulate Talent effect
        stygian_resurge *= 1.2

        return stygian_resurge

    def _simulate_extra_stygian_resurge(self) -> float:
        #  simulate A6 Trace additional damage
        extra_stygian_resurge_list = []
        for _ in range(6):
            extra_stygian_resurge = self.atk * 0.25
            crit = random.random() < self.crit_rate
            if crit:
                extra_stygian_resurge *= self.crit_dmg
            extra_stygian_resurge *= self.elemental_dmg

            #  simulate A6 Trace buff
            if self.a6_buff_stack > 0:
                extra_stygian_resurge *= (1 + (0.3 * self.a6_buff_stack))

            #  simulate Talent effect
            extra_stygian_resurge *= 1.2

            extra_stygian_resurge_list.append(extra_stygian_resurge)

        extra_stygian_resurge = sum(extra_stygian_resurge_list)

        return extra_stygian_resurge

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        if skill:
            dmg = self.atk * self.skill_multiplier
            if crit:
                dmg *= self.crit_dmg
            dmg *= self.elemental_dmg
            #  simulate A6 Trace buff
            if self.a6_buff_stack > 0:
                dmg *= (1 + (0.3 * self.a6_buff_stack))
            self.crimson_knot += 1
        else:
            ult_dmg_list = []
            rainblade_dmg = 0
            crimson_knot_dmg = 0

            self._simulate_rainblade()
            self._simulate_crimson_knot()
            stygian_resurge = self._simulate_stygian_resurge()
            self._simulate_crimson_knot()
            extra_stygian_resurge = self._simulate_extra_stygian_resurge()

            total_crimson_knot_dmg = sum(self.crimson_knot_dmg_list)

            stygian_resurge += extra_stygian_resurge

            ult_dmg_list.append(rainblade_dmg + total_crimson_knot_dmg + stygian_resurge)

            dmg = sum(ult_dmg_list)

            #  simulate Ult damage limit
            if dmg > (self.atk * 3.72):
                dmg = self.atk * 3.72
                crit = random.random() < self.crit_rate
                if crit:
                    dmg *= self.crit_dmg
                dmg *= self.elemental_dmg
                #  simulate A6 Trace buff
                if self.a6_buff_stack > 0:
                    dmg *= (1 + (0.3 * self.a6_buff_stack))
                #  simulate Talent effect
                dmg *= 1.2

        result = dmg

        if skill:
            self.current_ult_energy += 1
        elif ult:
            #  simualte A2 Trace
            if self.current_ult_energy >= 9:
                self.current_ult_energy -= 9
                self.excessive_current_ult_energy = self.current_ult_energy
                if self.excessive_current_ult_energy > 3:
                    self.current_ult_energy = 3
                else:
                    self.current_ult_energy = self.excessive_current_ult_energy
            else:
                self.current_ult_energy = 0

        #  simulate A4 Trace
        if self.nihiliy_allies == 1:
            result *= 1.15
        elif self.nihiliy_allies == 2:
            result *= 1.6

        self.total_dmg.append(result)

    def _simulate_ally_turn(self):
        debuff = random.choice([1, 2, 3, 4])
        self.current_ult_energy += debuff
        self.crimson_knot += debuff

    def _simulate_actions_during_each_turn(self):
        crit = random.random() < self.crit_rate
        self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

        if self.current_ult_energy >= 9:
            self._simulate_skill_and_ult(skill=False, ult=True, crit=crit)

    def _reset_variables(self):
        self.current_ult_energy = 0
        self.crimson_knot = 0
        self.crimson_knot_removed = 0
        self.excessive_current_ult_energy = 0
        self.a6_buff_stack = 0
        self.a6_trace_buff_duration = 0
        self.crimson_knot_dmg_list = []

    def _simulate_enter_battle_effect(self):
        #  simulate A2 Trace
        self.current_ult_energy = 5
        self.crimson_knot = 5

    def _set_scenario(self, nihiliy_allies):
        #  simulate Nihility teammate count
        self.nihiliy_allies = nihiliy_allies[0]

    def _simulate_buff_duration_on_character(self):
        #  simulate A6 Trace buff duration
        if self.a6_buff_stack > 0:
            self.a6_trace_buff_duration += 1
            if self.a6_trace_buff_duration >= 4:
                self.a6_buff_stack -= 1
                if self.a6_buff_stack < 0:
                    self.a6_buff_stack = 0
                self.a6_trace_buff_duration = 0


class Welt(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=102,
                 skill_multiplier=0.72,
                 ult_multiplier=1.5,
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
        dmg = 0
        total_skill_dmg = 0
        if skill:
            for _ in range(3):
                dmg = self.atk * self.skill_multiplier
                crit = random.random() < self.crit_rate
                if crit:
                    dmg *= self.crit_dmg
                dmg *= self.elemental_dmg

                talent_dmg = 0
                slowed_enemy = random.random() < 0.5
                if slowed_enemy:
                    talent_dmg = self.atk * 0.6 * self.elemental_dmg

                # simulate A2 Trace buff
                if self.a2_trace_buff > 0:
                    dmg *= 1.12
                    talent_dmg *= 1.12

                # simulate A6 Trace
                weakness_broken_enemy = random.random() < 0.5
                if weakness_broken_enemy:
                    dmg *= 1.20
                    talent_dmg *= 1.20

                total_skill_dmg += dmg + talent_dmg
        else:
            dmg = self.atk * self.ult_multiplier

        if crit:
            dmg *= self.crit_dmg

        result = self.elemental_dmg * dmg

        if skill:
            result = total_skill_dmg
            self.current_ult_energy += 30
        elif ult:
            # simulate A2 Trace buff
            if self.a2_trace_buff > 0:
                result *= 1.12

            # simulate A6 Trace
            weakness_broken_enemy = random.random() < 0.5
            if weakness_broken_enemy:
                result *= 1.20

            self.current_ult_energy = 5

            # simulate A4 Trace
            self.current_ult_energy += 10

            a2_trace_buff_duration = 2
            # +1 as the buff should last to the next 2 turns
            self.a2_trace_buff = a2_trace_buff_duration + 1

        self.total_dmg.append(result)

    def _simulate_buff_duration_on_character(self):
        if self.a2_trace_buff > 0:
            self.a2_trace_buff -= 1

    def _reset_variables(self):
        self.a2_trace_buff = 0


class Luka(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=103,
                 skill_multiplier=1.2,
                 ult_multiplier=3.3,
                 ult_energy=130
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

    def _reset_variables(self):
        self.bleed = 0
        self.bleed_duration = 0
        self.ult_buff = 0
        self.fighting_will_stack = []

    def _simulate_skill_and_ult(self, skill: bool, ult: bool, crit: bool):
        if skill:
            dmg = self.atk * self.skill_multiplier
            self.bleed = 1
            self.current_ult_energy += 30
            if self.fighting_will_stack.count('skill') < 4:
                self.fighting_will_stack.append('skill')
                self.current_ult_energy += 3
        else:
            dmg = 0
            ult_buff_duration = 3
            for _ in range(2):
                self.fighting_will_stack.append('ult')
                self.current_ult_energy += 3
            #  +1 as should last for the next 3 turns
            self.ult_buff = ult_buff_duration + 1
            if self.ult_buff > 0:
                dmg = self.atk * self.ult_multiplier * 1.2
            else:
                dmg = self.atk * self.ult_multiplier
            self.current_ult_energy = 5

        if crit:
            dmg *= self.crit_dmg

        total_dmg = self.elemental_dmg * dmg

        self.total_dmg.append(total_dmg)

    def _simulate_actions_during_each_turn(self):
        #  simulate Enhanced Basic Atk if there are Fighting Will stacks, else simulate Skill
        if len(self.fighting_will_stack) >= 2:
            #  simulate using 2 Fighting Will stacks
            for _ in range(2):
                self.fighting_will_stack.pop(-1)

            #  simulate Sky-Shatter Fist
            enhanced_basic_atk_dmg_list = []
            for _ in range(3):
                dmg = self.atk * 0.2
                crit = random.random() < self.crit_rate
                if crit:
                    dmg *= self.crit_dmg
                dmg *= self.elemental_dmg
                if self.ult_buff > 0:
                    dmg *= 1.2

                #  simulate A6 Trace
                additional_hit = random.random() < 0.5
                additional_hit_dmg = 0
                if additional_hit:
                    additional_hit_dmg = self.atk * 0.2
                    crit = random.random() < self.crit_rate
                    if crit:
                        additional_hit_dmg *= self.crit_dmg
                    additional_hit_dmg *= self.elemental_dmg
                    if self.ult_buff > 0:
                        additional_hit_dmg *= 1.2

                enhanced_basic_atk_dmg_list.append(dmg + additional_hit_dmg)

            enhanced_basic_atk_dmg = sum(enhanced_basic_atk_dmg_list)

            #  simulate Rising Uppercut
            uppercut = self.atk * 0.8
            crit = random.random() < self.crit_rate
            if crit:
                uppercut *= self.crit_dmg
            uppercut *= self.elemental_dmg
            if self.ult_buff > 0:
                uppercut *= 1.2

            #  simulate Talent effect
            if self.bleed > 0:
                bleed_dmg = self.atk * self.bleed_multipier * 0.85
            else:
                bleed_dmg = 0

            total_dmg = enhanced_basic_atk_dmg + uppercut + bleed_dmg

            self.current_ult_energy += 20

            self.total_dmg.append(total_dmg)
        else:
            crit = random.random() < self.crit_rate
            self._simulate_skill_and_ult(skill=True, ult=False, crit=crit)

        if self.current_ult_energy >= self.ult_energy:
            crit = random.random() < self.crit_rate
            self._simulate_skill_and_ult(skill=False, ult=True, crit=crit)

    def _simulate_buff_duration_on_character(self):
        if self.ult_buff > 0:
            self.ult_buff -= 1

    def _simulate_debuff_duration_on_enemy(self):
        #  simulate Bleed duration from Skill
        if self.bleed > 0:
            self.bleed_duration += 1
            if self.bleed_duration >= 3:
                self.bleed -= 1
                self.bleed_duration = 0

    def _simulate_enemy_turn(self):
        #  simulate Bleed damage from Skill
        if self.bleed > 0:
            bleed_dmg = self.atk * self.bleed_multipier * self.elemental_dmg

            self.total_dmg.append(bleed_dmg)

    def _simulate_enter_battle_effect(self):
        self.fighting_will_stack.append('talent')
        self.current_ult_energy += 3
        self.bleed_multipier = random.uniform(1.0, 3.38)


class Sampo(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=102,
                 skill_multiplier=0.56,
                 ult_multiplier=1.6,
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
        dmg = 0
        total_skill_dmg = 0
        if skill:
            # simulate Skill hits
            for _ in range(5):
                dmg = self.atk * self.skill_multiplier
                crit = random.random() < self.crit_rate
                if crit:
                    dmg *= self.crit_dmg
                dmg *= self.elemental_dmg
                total_skill_dmg += dmg

                # simulate inflicting Wind Shear
                wind_shear = random.random() < 0.65
                if wind_shear:
                    if len(self.wind_shear_stack) < 5:
                        wind_shear_duration = 3
                        talent_effect = 1
                        self.wind_shear_stack.append(wind_shear_duration + talent_effect)

            self.current_ult_energy += 30
            self.total_dmg.append(total_skill_dmg)
        else:
            dmg = self.atk * self.ult_multiplier
            if crit:
                dmg *= self.crit_dmg
            dmg *= self.elemental_dmg

            # simulate debuff from Ultimate
            dot_amplifier_duration = 2
            self.dot_amplifier.append(dot_amplifier_duration)

            self.total_dmg.append(dmg)

            self.current_ult_energy = 5

            # simulate A4 Trace
            self.current_ult_energy += 10

    def _reset_variables(self):
        self.wind_shear_stack = []
        self.dot_amplifier = []

    def _simulate_debuff_duration_on_enemy(self):
        if self.wind_shear_stack:
            self.wind_shear_stack[0] -= 1
            if self.wind_shear_stack[0] == 0:
                self.wind_shear_stack.pop(0)

        if self.dot_amplifier:
            self.dot_amplifier[0] -= 1
            if self.dot_amplifier[0] == 0:
                self.dot_amplifier.pop(0)

    def _simulate_enemy_turn(self):
        if self.wind_shear_stack:
            dmg = self.atk * 0.52 * self.elemental_dmg
            if self.dot_amplifier:
                dmg *= 1.3
            dmg *= len(self.wind_shear_stack)
            self.total_dmg.append(dmg)


class Guinanfei(Character):
    def __init__(self,
                 atk=3000,
                 crit_rate=0.5,
                 crit_dmg=2,
                 elemental_dmg=1.466,
                 speed=106,
                 skill_multiplier=1.2,
                 ult_multiplier=1.2,
                 ult_energy=130
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
            if crit:
                dmg *= self.crit_dmg
            dmg *= self.elemental_dmg

            # simulate A6 Trace
            if self.burn_stack:
                dmg *= 1.2

            # simulate inflicting Burn to enemy
            burn_duration = 2
            self.burn_stack.append(burn_duration)

            self.total_dmg.append(dmg)

            self.current_ult_energy += 30
        else:
            dmg = self.atk * self.ult_multiplier
            if crit:
                dmg *= self.crit_dmg
            dmg *= self.elemental_dmg

            # simulate A6 Trace
            if self.burn_stack:
                dmg *= 1.2

            burn_dmg = 0
            if self.burn_stack:
                burn_dmg = self.atk * 2.182 * self.elemental_dmg * 0.92

                # simulate A6 Trace
                if self.burn_stack:
                    burn_dmg *= 1.2

            self.total_dmg.append(dmg + burn_dmg)

            self.current_ult_energy = 5

    def _simulate_enemy_turn(self):
        if self.burn_stack:
            dmg = self.atk * 2.182 * self.elemental_dmg

            # simulate A6 Trace
            if self.burn_stack:
                dmg *= 1.2

            self.burn_stack[0] -= 1
            if self.burn_stack[0] == 0:
                self.burn_stack.pop(0)

            self.total_dmg.append(dmg)

    def _reset_variables(self):
        self.burn_stack = []