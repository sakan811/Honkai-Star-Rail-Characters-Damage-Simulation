# Simulation Disclaimers
**_This simulation aims to provide a simplified model for comparing character damage output. 
Actual in-game performance may vary due to additional factors not included in this simulation._**

This simulation **focuses exclusively** on the **elements** that **directly impact** character **damage** output, 
as a result, **not all** aspects of character behavior, interactions, or game mechanics were simulated.

Some elements may behave differently from actual in-game mechanics. For example:
- Yunli and Clara will always get hit by an enemy, which triggers their Follow-up Attack.
- Enemy effect resistances were not considered. 
  Any ability with a chance to inflict a debuff will do so based solely on its base chance.
  - If the **Effect Hit Rate** is important to the character's damage, 
    debuff-inflicting abilities had their base chance increased by the **Effect Hit Rate**. 

Certain elements were simulated with a 50/50 chance of maximum or minimum effect:
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