# Honkai Star Rail Characters' Damage Simulation

**Simulate** 10-cycles for 1,000 battles to find the **average damage** of Honkai Star Rail's **Characters**.

## Status
[![CodeQL](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/codeql.yml)

[![Python application](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/python-app.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/python-app.yml)

## Visualizations
[Click here](docs/VISUALS.md) for visualizations.

## Simulation Disclaimers
**_The result of this simulation might not reflect the actual in-game damage._**

This simulation **focuses exclusively** on the **elements** that **directly impact** character **damage** output, 
as a result, **not all** aspects of character behavior, interactions, or game mechanics were simulated.

Certain behaviors, interactions, or mechanics were simplified and may not exactly reflect their in-game counterparts 
for the sake of easier simulation.

Simulate each character for 1,000 battles, 10 cycles each.

Simulated single-target damage except for Erudition characters as multi-target damage was also simulated.

[Click here](docs/DISCLAIMERS.md) to read more about the simulation details.

## How to Run a Simulation
### Setup a Project
- Clone this repo: https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios.git
- Create **.env** file with the following variables:
  ```
  DB_NAME=hsr_char_action_dmg
  DB_PASSWORD=
  ```

### Setup a Database
- Install **[PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)**
  - Make sure that PostgreSQL server is installed
  - Setup your superuser's **password** as instructed.
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
[![CodeQL](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/codeql.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/codeql.yml)

[![Python application](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/python-app.yml/badge.svg)](https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios/actions/workflows/python-app.yml)

### Brief Codebase Documents
[Click here](docs/DOCS.md) to read a brief docs of this codebase.
