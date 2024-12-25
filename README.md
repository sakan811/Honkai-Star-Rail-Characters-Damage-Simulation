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

- Clone this repo: <https://github.com/sakan811/Honkai-Star-Rail-Characters-Damage-By-Scenarios.git>
- Rename **.env.example** to **.env**

### Setup a Database

- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Run:

  ```bash
  docker compose up -d
  ```

  - The container is mapped to port 6000 by default, change it if needed, for example:

    - ```bash
      export HOST_POSTGRES_PORT=5432
      ```

  - The container is mapped to a volume `postgres_data` to store the data.
    It will be inside your current working directory, change it if needed, for example:

    - ```bash
      export POSTGRES_DATA_PATH=/path/to/your_new_postgres_data
      ```

### Run a Simulation

- Make sure Docker Desktop and Postgres container are running.
- Run:

  ```bash
  python main.py
  ```
