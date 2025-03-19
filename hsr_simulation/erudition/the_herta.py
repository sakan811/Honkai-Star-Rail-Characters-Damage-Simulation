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


class TheHerta(Character):
    # Skill constants - Normal
    SKILL_MULTIPLIER = 0.7
    SKILL_BREAK_AMOUNT = 15
    SKILL_ADJACENT_BREAK = 5
    SKILL_ENERGY_GAIN = 30

    # Skill constants - Enhanced
    ENHANCED_SKILL_MULTIPLIER = 0.8
    ENHANCED_SKILL_BREAK_AMOUNT = 20
    ENHANCED_SKILL_ADJACENT_BREAK = 5
    ENHANCED_SKILL_AOE_MULTIPLIER = 0.4

    # Ultimate constants
    ULT_MULTIPLIER = 2.0
    ULT_BREAK_AMOUNT = 20
    ULT_ENERGY_COST = 220
    ULT_ENERGY_GAIN = 5
    MAX_INSPIRATION_STACKS = 4
    ULT_ATK_BOOST = 0.8  # 80% ATK boost
    ULT_ATK_BOOST_DURATION = 3

    # Talent constants
    MAX_INTERPRETATION_STACKS = 42
    INITIAL_WAVE_INTERPRETATION_STACKS = 25
    INTERPRETATION_DMG_BOOST_PRIMARY = 0.08  # 8% per stack
    INTERPRETATION_DMG_BOOST_OTHERS = 0.04  # 4% per stack
    ERUDITION_PATH_BONUS_PRIMARY = 0.08  # Additional 8% per stack
    ERUDITION_PATH_BONUS_OTHERS = 0.04  # Additional 4% per stack

    # A2 Trace constants
    A2_ENERGY_PER_TARGET = 3
    A2_MAX_ENERGY_TARGETS = 5
    A2_ICE_DMG_BOOST = 0.5  # 50% Ice DMG boost

    # A4 Trace constants
    A4_MIN_TARGETS = 3
    A4_EXTRA_INTERPRETATION_STACKS = 2

    # A6 Trace constants
    MAX_ANSWER_STACKS = 99
    ANSWER_DMG_BOOST_PER_STACK = 0.01  # 1% per stack

    def __init__(self, speed: float = 99, ult_energy: int = ULT_ENERGY_COST):
        super().__init__(speed=speed, ult_energy=ult_energy)
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.inspiration = 0
        self.interpretation = 0
        self.atk_boost_turns_remaining = 0
        self.erudition_chars_in_team = random.choice([1, 2])
        self.enemy_interpretation_stacks = {}  # Dictionary to track interpretation stacks per enemy
        self.elite_enemy_id = None  # Will be set when wave starts if elite enemy exists
        self.has_elite_enemy = False
        self.ice_dmg_boost_active = False  # Track if Ice DMG boost is active
        self.answer_stacks = 0  # Track Answer stacks for A6

    def reset_character_data_for_each_battle(self) -> None:
        """
        Reset character's stats and battle-related data.
        :return: None
        """
        main_logger.info(f"Resetting {self.__class__.__name__} data...")
        super().reset_character_data_for_each_battle()
        self.enemy_on_field = random.choice([1, 2, 3, 4, 5])
        self.erudition_chars_in_team = random.choice([1, 2])
        self.inspiration = 0
        self.interpretation = 0
        self.atk_boost_turns_remaining = 0
        self.enemy_interpretation_stacks = {}
        self.elite_enemy_id = None
        self.has_elite_enemy = False
        self.ice_dmg_boost_active = False
        self.answer_stacks = 0

    def start_wave(self) -> None:
        """
        Handle start of wave effects.
        50% chance to have an elite enemy. If present, applies 25 interpretation stacks to it.
        If there were existing stacks from previous wave, transfers them to the elite enemy.
        Otherwise, applies to a random enemy.
        All previous enemies are considered defeated when starting a new wave.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} starting wave...")

        # Store total existing stacks before clearing
        total_existing_stacks = sum(self.enemy_interpretation_stacks.values())

        # Clear previous wave's data since all enemies are defeated
        self.enemy_interpretation_stacks.clear()
        self.elite_enemy_id = None
        self.has_elite_enemy = False

        # Determine if there's an elite enemy (50% chance)
        self.has_elite_enemy = random.random() < 0.5
        if self.has_elite_enemy and self.enemy_on_field > 0:
            self.elite_enemy_id = 0  # First enemy is elite if exists
            main_logger.debug("Elite enemy present in new wave")
        else:
            self.elite_enemy_id = None
            main_logger.debug("No elite enemy in new wave")

        # Apply initial interpretation stack to all enemies in new wave
        for enemy_id in range(self.enemy_on_field):
            self.enemy_interpretation_stacks[enemy_id] = 1

        # Apply stacks to elite enemy or random enemy
        if self.enemy_on_field > 0:
            if self.has_elite_enemy:
                target_enemy = self.elite_enemy_id
                main_logger.debug(f"Applying stacks to elite enemy {target_enemy}")
                # Transfer existing stacks if any, otherwise use initial stacks
                final_stacks = (
                    min(
                        total_existing_stacks + self.INITIAL_WAVE_INTERPRETATION_STACKS,
                        self.MAX_INTERPRETATION_STACKS,
                    )
                    if total_existing_stacks > 0
                    else self.INITIAL_WAVE_INTERPRETATION_STACKS
                )
            else:
                target_enemy = random.randint(0, self.enemy_on_field - 1)
                main_logger.debug(f"Applying stacks to random enemy {target_enemy}")
                final_stacks = self.INITIAL_WAVE_INTERPRETATION_STACKS

            self.enemy_interpretation_stacks[target_enemy] = final_stacks
            main_logger.debug(
                f"Applied {final_stacks} interpretation stacks to enemy {target_enemy}"
            )

    def _get_priority_target(self) -> int:
        """
        Get the priority target for skills.
        Returns elite enemy if present, otherwise returns a random enemy.
        :return: Enemy ID of the priority target
        """
        if (
            self.has_elite_enemy
            and self.elite_enemy_id in self.enemy_interpretation_stacks
        ):
            return self.elite_enemy_id
        return (
            random.randint(0, self.enemy_on_field - 1) if self.enemy_on_field > 0 else 0
        )

    def _calculate_interpretation_multiplier(
        self, enemy_id: int, is_primary_target: bool = False
    ) -> float:
        """
        Calculate damage multiplier from interpretation stacks.
        Returns the additional multiplier (without base 1.0).
        :param enemy_id: ID of the enemy
        :param is_primary_target: Whether this is the primary target
        :return: Additional damage multiplier from interpretation
        """
        stacks = self.enemy_interpretation_stacks.get(enemy_id, 0)

        if is_primary_target:
            base_boost = self.INTERPRETATION_DMG_BOOST_PRIMARY
            path_bonus = self.ERUDITION_PATH_BONUS_PRIMARY
        else:
            base_boost = self.INTERPRETATION_DMG_BOOST_OTHERS
            path_bonus = self.ERUDITION_PATH_BONUS_OTHERS

        # Calculate total boost per stack (returns only the additional multiplier)
        boost_per_stack = base_boost
        if self.erudition_chars_in_team >= 2:
            boost_per_stack += path_bonus

        return boost_per_stack * stacks

    def take_action(self) -> None:
        """
        Simulate taking actions.
        :return: None.
        """
        main_logger.info(f"{self.__class__.__name__} is taking actions...")

        if random.random() < 0.5:
            self.start_wave()

        # simulate enemy turn
        self._simulate_enemy_weakness_broken()

        if self.battle_start:
            if self.erudition_chars_in_team >= 2:
                self.crit_dmg = self.default_crit_dmg + 0.8

            self.battle_start = False

        if self.skill_points > 0:
            self._use_skill()
        else:
            self._use_basic_atk()

        if self.ult_energy > 0:
            self._use_ult()

            # take action again after using Ultimate
            if self.skill_points > 0:
                self._use_skill()
            else:
                self._use_basic_atk()

        self.end_turn()

    def _use_basic_atk(self) -> None:
        """
        Simulate basic atk damage.
        Deals Ice DMG equal to 100% of The Herta's ATK to one designated enemy.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using basic attack...")
        # Basic attack is single target, 100% ATK ratio
        dmg = self._calculate_damage(skill_multiplier=1.0, break_amount=10)
        self._update_skill_point_and_ult_energy(skill_points=1, ult_energy=20)
        self._record_damage(dmg=dmg, dmg_type="Basic ATK")

    def _use_skill(self) -> None:
        """
        Simulate skill damage. Uses enhanced skill if inspiration is available,
        otherwise uses normal skill.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} is using skill...")

        if self.inspiration > 0:
            self._use_enhanced_skill()
        else:
            self._use_normal_skill()

        # Common effects for both skill versions
        self.interpretation += 1

    def _use_normal_skill(self) -> None:
        """
        Simulate normal skill "Big Brain Energy" damage.
        Deals Ice DMG equal to 70% of The Herta's ATK to target and adjacent,
        repeating 2 times.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} using normal skill...")
        total_dmg = 0
        primary_target = self._get_priority_target()
        hit_enemies = set()

        # Skill hits 2 times
        for _ in range(2):
            # Primary target hit
            total_dmg += self._calculate_damage(
                skill_multiplier=self.SKILL_MULTIPLIER,
                break_amount=self.SKILL_BREAK_AMOUNT,
            )
            self._apply_interpretation_on_hit(primary_target)
            hit_enemies.add(primary_target)

            # Adjacent targets (up to 2)
            adjacent_count = min(self.enemy_on_field - 1, 2)
            for _ in range(adjacent_count):
                adjacent_target = random.randint(0, self.enemy_on_field - 1)
                if adjacent_target != primary_target:
                    total_dmg += self._calculate_damage(
                        skill_multiplier=self.SKILL_MULTIPLIER,
                        break_amount=self.SKILL_ADJACENT_BREAK,
                    )
                    self._apply_interpretation_on_hit(adjacent_target)
                    hit_enemies.add(adjacent_target)

        # Apply A2 energy regen
        self._apply_a2_energy_regen(len(hit_enemies))

        # Apply A4 interpretation stacks
        self._apply_a4_interpretation_stacks(list(hit_enemies))

        self._update_skill_point_and_ult_energy(
            skill_points=-1, ult_energy=self.SKILL_ENERGY_GAIN
        )
        self._record_damage(dmg=total_dmg, dmg_type="Skill")

    def _use_enhanced_skill(self) -> None:
        """
        Simulate enhanced skill "Hear Me Out" damage.
        Deals Ice DMG equal to 80% ATK to primary target and adjacent 2 times,
        then 40% ATK to all enemies.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} using enhanced skill...")
        total_dmg = 0
        primary_target = self._get_priority_target()
        hit_enemies = set()

        # Check for Ice DMG boost before damage calculation
        self._check_and_apply_ice_dmg_boost(primary_target)
        # Ice DMG boost is additional multiplier
        ice_boost = self.A2_ICE_DMG_BOOST if self.ice_dmg_boost_active else 0

        # First two hits (80% ATK)
        for _ in range(2):
            # Primary target
            primary_multiplier = self._calculate_interpretation_multiplier(
                primary_target, True
            )
            total_dmg += self._calculate_damage(
                skill_multiplier=self.ENHANCED_SKILL_MULTIPLIER,
                break_amount=self.ENHANCED_SKILL_BREAK_AMOUNT,
                dmg_multipliers=[
                    primary_multiplier,
                    ice_boost,
                ],  # Pass both additional multipliers
            )
            self._apply_interpretation_on_hit(primary_target)
            hit_enemies.add(primary_target)

            # Adjacent targets
            adjacent_count = min(self.enemy_on_field - 1, 2)
            for _ in range(adjacent_count):
                adjacent_target = random.randint(0, self.enemy_on_field - 1)
                if adjacent_target != primary_target:
                    other_multiplier = self._calculate_interpretation_multiplier(
                        adjacent_target, False
                    )
                    total_dmg += self._calculate_damage(
                        skill_multiplier=self.ENHANCED_SKILL_MULTIPLIER,
                        break_amount=self.ENHANCED_SKILL_ADJACENT_BREAK,
                        dmg_multipliers=[
                            other_multiplier,
                            ice_boost,
                        ],  # Pass both additional multipliers
                    )
                    self._apply_interpretation_on_hit(adjacent_target)
                    hit_enemies.add(adjacent_target)

        # Final AOE hit (40% ATK to all)
        for enemy_id in range(self.enemy_on_field):
            other_multiplier = self._calculate_interpretation_multiplier(
                enemy_id, False
            )
            total_dmg += self._calculate_damage(
                skill_multiplier=self.ENHANCED_SKILL_AOE_MULTIPLIER,
                break_amount=0,
                dmg_multipliers=[
                    other_multiplier,
                    ice_boost,
                ],  # Pass both additional multipliers
            )
            self._apply_interpretation_on_hit(enemy_id)
            hit_enemies.add(enemy_id)

        # Apply A2 energy regen
        self._apply_a2_energy_regen(len(hit_enemies))

        # Apply A4 interpretation stacks
        self._apply_a4_interpretation_stacks(list(hit_enemies))

        # Reset interpretation stacks on primary target to 1
        self.enemy_interpretation_stacks[primary_target] = 1

        # Reset Ice DMG boost and consume inspiration
        self.ice_dmg_boost_active = False
        self.inspiration -= 1

        self._update_skill_point_and_ult_energy(
            skill_points=-1, ult_energy=self.SKILL_ENERGY_GAIN
        )
        self._record_damage(dmg=total_dmg, dmg_type="Enhanced Skill")

    def _use_ult(self) -> None:
        """
        Simulate ultimate damage "Told Ya! Magic Happens".
        Rearranges Interpretation stacks, deals 200% ATK Ice DMG to all enemies,
        boosts ATK by 80% for 3 turns, gains Inspiration, and takes another action.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} using ultimate...")

        # Rearrange Interpretation stacks
        self._rearrange_interpretation_stacks()

        # Apply ATK boost (80% for 3 turns)
        self._apply_atk_boost()

        # Calculate A6 damage boost from Answer stacks (returns only the additional multiplier)
        answer_multiplier = self.answer_stacks * self.ANSWER_DMG_BOOST_PER_STACK
        main_logger.debug(
            f"A6: Ultimate boosted by {self.answer_stacks}% from Answer stacks"
        )

        # Deal AoE damage to all enemies (200% ATK)
        total_dmg = 0
        for enemy_id in range(self.enemy_on_field):
            total_dmg += self._calculate_damage(
                skill_multiplier=self.ULT_MULTIPLIER,
                break_amount=self.ULT_BREAK_AMOUNT,
                dmg_multipliers=[
                    answer_multiplier
                ],  # Only pass the additional multiplier
            )

        # Record damage
        self._record_damage(dmg=total_dmg, dmg_type="Ultimate")

        # Add Inspiration stack (capped at 4)
        self.inspiration = min(self.inspiration + 1, self.MAX_INSPIRATION_STACKS)
        main_logger.debug(
            f"Added Inspiration stack, current stacks: {self.inspiration}"
        )

        # Set energy after ultimate
        self.current_ult_energy = self.ULT_ENERGY_GAIN

    def _apply_atk_boost(self) -> None:
        """
        Apply ATK boost from ultimate.
        Increases ATK by 80% for 3 turns.
        If used while boost is active, refreshes the duration.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} applying ATK boost...")
        # Reset ATK to base value before applying boost
        self.atk = self.default_atk
        # Apply 80% ATK boost
        self.atk *= 1 + self.ULT_ATK_BOOST
        # Set/refresh duration
        self.atk_boost_turns_remaining = self.ULT_ATK_BOOST_DURATION
        main_logger.debug(
            f"ATK boosted to {self.atk} for {self.atk_boost_turns_remaining} turns"
        )

    def _rearrange_interpretation_stacks(self) -> None:
        """
        Rearrange Interpretation stacks, prioritizing the transfer to Elite-level targets.
        All other enemies' stacks are reset to 1 after rearrangement.
        :return: None
        """
        main_logger.info(
            f"{self.__class__.__name__} rearranging interpretation stacks..."
        )

        if not self.enemy_interpretation_stacks:
            return

        total_stacks = sum(self.enemy_interpretation_stacks.values())

        # Reset all stacks to 1 first
        for enemy_id in self.enemy_interpretation_stacks:
            self.enemy_interpretation_stacks[enemy_id] = 1

        # Determine target for stack transfer
        if (
            self.has_elite_enemy
            and self.elite_enemy_id in self.enemy_interpretation_stacks
        ):
            target_enemy = self.elite_enemy_id
            main_logger.debug(f"Transferring stacks to elite enemy {target_enemy}")
        else:
            # If no elite enemy, choose random target
            target_enemy = random.choice(list(self.enemy_interpretation_stacks.keys()))
            main_logger.debug(f"Transferring stacks to random enemy {target_enemy}")

        # Transfer stacks to target (capped at max)
        self.enemy_interpretation_stacks[target_enemy] = min(
            total_stacks, self.MAX_INTERPRETATION_STACKS
        )
        main_logger.debug(
            f"Transferred {self.enemy_interpretation_stacks[target_enemy]} interpretation stacks to enemy {target_enemy}"
        )

    def end_turn(self) -> None:
        """
        Handle end of turn effects.
        Manages ATK boost duration and resets ATK when boost expires.
        Also resets per-turn attributes.
        :return: None
        """
        main_logger.info(f"{self.__class__.__name__} ending turn...")
        # Handle ATK boost duration
        if self.atk_boost_turns_remaining > 0:
            self.atk_boost_turns_remaining -= 1
            main_logger.debug(
                f"ATK boost remaining turns: {self.atk_boost_turns_remaining}"
            )
            if self.atk_boost_turns_remaining == 0:
                self.atk = self.default_atk
                main_logger.debug(f"ATK boost expired, reset to {self.atk}")

    def _apply_a2_energy_regen(self, targets_hit: int) -> None:
        """
        Apply A2 trace energy regeneration based on targets hit.
        With A4 trace, minimum target count is 3 if team has 2+ Erudition characters.
        :param targets_hit: Number of targets hit by the attack
        :return: None
        """
        # Apply minimum target count if A4 is active
        if self.erudition_chars_in_team >= 2:
            targets_hit = max(targets_hit, self.A4_MIN_TARGETS)

        energy_targets = min(targets_hit, self.A2_MAX_ENERGY_TARGETS)
        energy_gain = energy_targets * self.A2_ENERGY_PER_TARGET
        self.current_ult_energy += energy_gain
        main_logger.debug(
            f"A2: Regenerated {energy_gain} energy from hitting {energy_targets} targets"
        )

    def _apply_a4_interpretation_stacks(
        self, hit_enemies: list[int], is_erudition_attacker: bool = True
    ) -> None:
        """
        Apply A4 trace interpretation stacks to enemy with highest stacks among hit targets.
        Also adds Answer stacks for each Interpretation stack applied.
        Ensures interpretation stacks don't exceed maximum.
        :param hit_enemies: List of enemy IDs that were hit
        :param is_erudition_attacker: Whether the attacker follows Path of Erudition
        :return: None
        """
        if not hit_enemies or self.erudition_chars_in_team < 2:
            return

        # Find enemy with highest interpretation stacks
        max_stacks = -1
        target_enemy = None
        for enemy_id in hit_enemies:
            if enemy_id in self.enemy_interpretation_stacks:
                stacks = self.enemy_interpretation_stacks[enemy_id]
                if stacks > max_stacks:
                    max_stacks = stacks
                    target_enemy = enemy_id

        if target_enemy is not None:
            current_stacks = self.enemy_interpretation_stacks[target_enemy]
            extra_stacks = 1

            # Apply 2 additional stacks if attacker is Erudition
            if is_erudition_attacker:
                extra_stacks += self.A4_EXTRA_INTERPRETATION_STACKS

            self.enemy_interpretation_stacks[target_enemy] = min(
                current_stacks + extra_stacks, self.MAX_INTERPRETATION_STACKS
            )
            main_logger.debug(
                f"A4: Applied {extra_stacks} interpretation stacks to enemy {target_enemy}"
            )

            # Add Answer stacks for each Interpretation stack
            for _ in range(extra_stacks):
                self._add_answer_stack()

    def _apply_interpretation_on_hit(self, enemy_id: int) -> None:
        """
        Apply 1 interpretation stack to hit enemy and gain Answer stack.
        Ensures interpretation stacks don't exceed maximum.
        :param enemy_id: ID of the enemy hit
        :return: None
        """
        if enemy_id in self.enemy_interpretation_stacks:
            current_stacks = self.enemy_interpretation_stacks[enemy_id]
            self.enemy_interpretation_stacks[enemy_id] = min(
                current_stacks + 1, self.MAX_INTERPRETATION_STACKS
            )
            main_logger.debug(f"A2: Applied interpretation stack to enemy {enemy_id}")
            self._add_answer_stack()  # Add Answer stack from A6

    def _check_and_apply_ice_dmg_boost(self, primary_target: int) -> None:
        """
        Check if primary target has max interpretation stacks and apply Ice DMG boost if true.
        :param primary_target: ID of the primary target
        :return: None
        """
        if primary_target in self.enemy_interpretation_stacks:
            if (
                self.enemy_interpretation_stacks[primary_target]
                >= self.MAX_INTERPRETATION_STACKS
            ):
                self.ice_dmg_boost_active = True
                main_logger.debug("A2: Activated 50% Ice DMG boost")

    def _add_answer_stack(self) -> None:
        """
        Add one Answer stack from A6 trace.
        Called whenever an Interpretation stack is applied.
        :return: None
        """
        if self.answer_stacks < self.MAX_ANSWER_STACKS:
            self.answer_stacks += 1
            main_logger.debug(
                f"A6: Added Answer stack, current stacks: {self.answer_stacks}"
            )
