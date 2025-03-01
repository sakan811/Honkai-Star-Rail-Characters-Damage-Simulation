# Simulation Disclaimers

**_This simulation aims to provide a simplified model for comparing character damage output and their damage distribution.
Actual in-game performance may vary due to additional factors not included in this simulation._**

This simulation **focuses exclusively** on the **elements** that **directly impact** character **damage** output,
as a result, **not all** aspects of character behavior, interactions, or game mechanics were simulated.

The averaged damage output came from the character alone,
except for some characters whose damage output is influenced by allies or enemies; hence,
some elements may behave differently from actual in-game mechanics for ease of simulation.
For example:

- Yunli and Clara will always get hit by an enemy, which triggers their Follow-up Attack.
- Enemy effect resistances were not considered.
  Any ability with a chance to inflict a debuff will do so based solely on its base chance.
  - If the **Effect Hit Rate** is important to the character's damage,
    debuff-inflicting abilities had their base chance increased by the **Effect Hit Rate**.
- The number of enemies being hit by Argenti was randomized between 1 and 5 enemies to simulate the randomness of his Talent.
  - Argenti's Ultimate has a 20% chance of using the Normal version and an 80% chance of using the Enhanced version,
    reflecting the assumption that players are more likely to opt for the Enhanced version.
- For Himeko, the number of enemies that got defeated by her Ultimate
  or weakness-broken by allies was randomized between 0 - 5 enemies.

Certain elements of most characters were simulated with a 50/50 chance of maximum or minimum effect:

- Seele was simulated with a 50% chance to get Resurgence buff
- Jingliu was simulated with a 50% chance to get 180% ATK buff otherwise she got a 6% ATK increased
  - 6% ATK increased come from ```((4% x HIGHEST_FREQ_MAX_BASE_HP_LVL_80) x NUMBER_Of_ALLY) + DEFAULT_ATK``` where:
    - DEFAULT_ATK = 2000
    - HIGHEST_FREQ_MAX_BASE_HP_LVL_80 = 1000
      - This number comes from [this project](https://github.com/sakan811/Honkai-Star-Rail-A-Few-Fun-Insights-with-Data-Analysis)
      - It is the highest frequency of the base Max HP of all characters at level 80
    - NUMBER_Of_ALLY = 3
- Dr. Ratio was simulated with a 50% chance to get 3 debuffs on an enemy otherwise he got 0 debuff
- Luka was simulated with a 50% chance to fight with an enemy whose Max HP made Bleed dealt the highest DMG,
  otherwise he fought an enemy that made Bleed dealt the least DMG
- Yanqing was simulated with a 50% chance to fight an Ice-weakness enemy, which trigger his Trace ability.
- Boothill was simulated with a 50 % chance to get Break Effect% that resulted in the highest Talent's break DMG;
  otherwise he got Break Effect% that made Talent's break DMG dealt the least DMG
- _And so on_

In case that the HP affects the character's damage, their HP was set to an average value
based on [PrydwenGG](https://www.prydwen.gg/) data

When an enemy is weakness-broken, 1 turn delays its turn;
hence the character can deal more damage to it for at least 1 turn, which simulates what happens in the game.

Every simulated character has 2,000 ATK, 50% Crit Rate, and 100% Crit Damage.

Basic ATK, Skill, Ultimate, Talent, and Trace are at level 10.

Character's level is 80.

Eidolons, Light Cones, and Relics were not considered.

Each character starts with 1 skill point.

## Erudition Characters

For **ease** of **Erudition** character **simulation**, **toughness reduction** for **AoE** attacks was applied
as if all the damage was **concentrated** on a **single** enemy.
For example:

- If an AoE attack reduces the main target's toughness by 20 and adjacent targets' toughness by 10,
  the simulation combines this, reducing the main target's toughness by 30.
  - This simplification reflects the increased damage to all enemies when multiple targets are broken in the game.

Erudition characters' were simulated to fight against 1 - 5 enemies which randomized each battle.

## Harmony Characters

**_This calculation was simplified for ease of simulation and might not reflect the actual in-game situation._**

- Simulate the potential damage increased of Physical Trailblazer's attacks in 1 cycle.
- Harmony characters share the same CRIT RATE, CRIT DMG, and ATK as Physical Trailblazer, which are 50%, 100%, and 2000 respectively, except in case that the stats of the Harmony character are used to calculate the buff.
- Assume that all possible buffs were applied to the Physical Trailblazer's attacks, but only once in 1 cycle.
- If DMG from Harmony character is based on the number of enemies, the DMG is averaged.
- If the DMG buff varies by situations, the buff is averaged.
  - Sunday's buff from Skill varies by ally's Summon, so his buff is averaged.
- Buff related to Skill point were ignored.
- Energy Regen-related buffs were evaluated using this formular: `total_ult_energy_gain / trailblazer_ult_energy`
  - This formular represents the potential DMG increased from Energy Regen, accounting for both non-ult and ult hits.
- If the buff is based on a stat of a Harmony character, that stat is based on average value from **PRYDWEN.GG**.
- If the buff has a maximum value, the maximum value is used.
- DMG from Basic ATK, SKill, Ultimate, Talent, or Trace of some Harmony characters was not simulated as it seems not to contribute to the potential damage increased.
- Enemy toughness is set to 100.

### Trailblazer

- The potential damage increased is calculated using Physical Trailblazer stats as a baseline.
- DMG of Basic ATK, Skill, and Ultimate are summed up to get the total damage.
  - Assume that the DMG happens in 1 hit in the 1st cycle.  
- The Physical Trailblazer's damage is based on fighting with 1 enemy.
