# Honkai Star Rail Characters' Damage Simulation

**Simulate** 10-cycles for 100 times to find the **average damage** of Honkai Star Rail's **Characters**.

Latest Update: 27 July 2024.

## Visualizations
[Power BI](https://app.powerbi.com/view?r=eyJrIjoiYmM2MDQxNDMtZGEwNy00NGU2LWJkNjItNmI3MTAwNDMwOGRkIiwidCI6ImZlMzViMTA3LTdjMmYtNGNjMy1hZDYzLTA2NTY0MzcyMDg3OCIsImMiOjEwfQ%3D%3D) 

[Facebook](https://www.facebook.com/permalink.php?story_fbid=pfbid025cHVzSokmryctRRaGtreiF4wbyCpeSQtyCcJYVSYqo9oZq4r8MRaGKDLz2rZPQjnl&id=61553626169836)  

[Instagram](https://www.instagram.com/p/C8ZMHSixVJE/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==)

## Simulation Disclaimers
**_The result of this simulation might not reflect the actual in-game damage._**

This simulation **focuses exclusively** on the **elements** that **directly impact** character **damage** output. 
As a result, **not all** aspects of character behavior, interactions, or game mechanics were simulated.

Simulate each character for 100 times, 10 cycles each.

Every simulated character has 2,000 ATK, 50% Crit Rate, and 100% Crit Damage.

Basic ATK, Skill, Ultimate, Talent, and Trace are at level 10.

Character's level is 80.

Eidolons, Light Cones, and Relics were not considered.

## To Run a Simulation
### Setup a Project
- Clone this repo:
- Create **.env** file with the following variables:
  ```
  DB_NAME=hsr_char_action_dmg
  DB_PASSWORD=
  ```

### Setup a Database
- Install **[PostgreSQL](https://www.postgresql.org/)**
- install **[pgAdmin](https://www.pgadmin.org/)**
- Enter your superuser's **password** in **.env** file for **DB_PASSWORD** variable. 
- Run **pgAdmin**
- Open **SQL** console in **pgAdmin**
- Execute:
  ```
  create database hsr_char_action_dmg;
  ```

## Codebase Details
### Test Status

