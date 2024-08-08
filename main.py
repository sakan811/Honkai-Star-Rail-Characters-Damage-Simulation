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
from hsr_simulation.character import Character
from hsr_simulation.configure_logging import main_logger
from hunt_main import start_sim_hunt
from nihility_main import start_sim_nihility


if __name__ == '__main__':
    base_char = Character()
    simulation_num = 1000
    max_cycles = 10

    try:
        start_sim_hunt(base_char, simulation_num, max_cycles)
        start_sim_nihility(base_char, simulation_num, max_cycles)
    except Exception as e:
        main_logger.error(e, exc_info=True)
        main_logger.error("Unexpected error occurred.")

