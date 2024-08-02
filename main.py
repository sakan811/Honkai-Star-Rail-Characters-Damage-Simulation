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

from hunt_main import start_sim_hunt
from nihility_main import start_sim_nihility


if __name__ == '__main__':
    simulation_num = 100
    max_cycles = 10

    start_sim_hunt(simulation_num, max_cycles)
    start_sim_nihility(simulation_num, max_cycles)

