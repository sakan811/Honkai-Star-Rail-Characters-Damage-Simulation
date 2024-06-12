# Honkai Star Rail Characters' Damage By Scenarios

Compare damage from each scenario of the given character.

Lastest Update: 12th June, 2024.

## Visualizations
[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid02DEEFBR5ixWvyvnr1rdLW5GnBLvkE26e7ZEkxLWKtaM2EupnGWdeiGe4Gx77GcvBrl&id=61553626169836)   
[Instagram](https://www.instagram.com/p/C6RPV1Ivttu/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

## Damage Simulation Disclaimers
Calculate characters' **Average Damage** based on 1,000 battles, with 30 cycles each.

Damage was calculated by considering only Skill, Ultimate, Talent, and Trace.
Basic ATK was simulated for some Characters with an Enhanced Basic ATK.

The effect of Speed buff/debuff from abilities was not simulated.
Action Forward buff/debuff from abilities were roughly simulated if the character's damage depended on it.

Simulation of enemies or allies were done only to create scenarios 
that could possibly trigger Skill, Ultimate, Talent, and Trace of the given Character.
AoE Skill, Ultimate, or Talent was simulated as if they were applied to a single enemy, 
considering only DMG dealt to the targeted enemy, not adjacent enemies.

Critical damage was also considered and simulated.

The Damage from this calculation is only theoretical.
It might not reflect Damage in real-game scenarios.

Every simulated character has 3,000 ATK, 50% Crit Rate, 100% Crit Damage, and 46.6% Elemental Damage Bonus.
Skill, Ultimate, Talent, and Trace are at level 10.
Characters' Speed is at level 80.

## [main.py](main.py)
- Run characters' average damage calculation by scenario.
- Migrate the data to SQLite database.

**To run the calculation:**
- Run [main.py](main.py)
- 'hsr_dmg_calculation.db' SQLite database will be created, along with the migrated data

## [sql_lite_pipeline.py](sql_lite_pipeline.py)
- Migrate data to SQLite database
- Create 'hsr_dmg_calculation.db' SQLite database if not exist
  