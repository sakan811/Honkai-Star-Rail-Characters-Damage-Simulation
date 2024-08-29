# Codebase Details
## [hsr_simulation](..%2Fhsr_simulation) Package
[character.py](..%2Fhsr_simulation%2Fcharacter.py)
- Contain base class for Character

[configure_logging.py](..%2Fhsr_simulation%2Fconfigure_logging.py)
- Contain function to configure logging
- You can set the log level in this script:
    ```
    main_logger = configure_logging_with_file(log_dir='logs', log_file='main.log',
                                              logger_name='main', level='WARNING')  # set log level here
    ```

[data_transformer.py](..%2Fhsr_simulation%2Fdata_transformer.py)
- Contain functions to transform data

[dmg_calculator.py](..%2Fhsr_simulation%2Fdmg_calculator.py)
- Contain functions for calculating damage

[postgre.py](..%2Fhsr_simulation%2Fpostgre.py)
- Contain function to connect to PostgreSQL

[simulate_battles.py](..%2Fhsr_simulation%2Fsimulate_battles.py)
- Contain functions to simulate battles

[simulate_cycles.py](..%2Fhsr_simulation%2Fsimulate_cycles.py)
- Contain functions to simulate cycles for each battle

[simulate_turns.py](..%2Fhsr_simulation%2Fsimulate_turns.py)
- Contain functions to simulate characters' turns within the given cycles

[utils.py](..%2Fhsr_simulation%2Futils.py)
- Contain utility functions

## [hunt](..%2Fhsr_simulation%2Fhunt) Package
Contain Python scripts that represent Hunt characters.

Each character is a subclass of Character class.


## [nihility](..%2Fhsr_simulation%2Fnihility) Package
Contain Python scripts that represent Nihility characters.

Each character is a subclass of Character class.

## [destruction](..%2Fhsr_simulation%2Fdestruction) Package
Contain Python scripts that represent Destruction characters.

Each character is a subclass of Character class.